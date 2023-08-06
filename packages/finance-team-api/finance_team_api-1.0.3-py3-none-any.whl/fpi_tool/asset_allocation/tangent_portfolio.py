import pandas as pd
import numpy as np

def CLA(return_data
        , cov_mat
        , target_vol
        , constraints
        , maxiter=1000):
    """
    :param return_data: DataFrame, 수익률 데이터
    :param cov_mat: DataFrame, EWMA Covariance Matrix
    :param target_vol: float, 포트폴리오 target volatility
    :param constraints: Dictionary, 각 자산에 대한 제한조건 설정
                       : {'SPY' : (0, 0.3), ...}
    :param maxiter: Int, 알고리즘 Iteration 횟수
    :return: Series


    Read Docs : https://www.quantopian.com/posts/critical-line-algorithm-for-portfolio-optimization

    기존에 Sharpe Ratio를 극대화 시키기 위한 Portfolio Construction은 Optimization을 기반으로 한다.
    하지만 현재 존재하는 여러 Optimization들은 각자 장단점을 가지게 됨으로써 복잡한 알고리즘일수록
    Local Minimum에 수렴하게 되어 미래 수익률 저하 요인을 만들어 준다.

    CLA(Critical Line Algorithm)방식은 기존의 복잡한 Optimization 방식을 버리고 Random Search와 같은
    단순한 방식으로 다소 선형적인 해 찾기 방식을 제공하며 기존의 방식보다 더 나음을 밝히고 있다.

    """
    rank_return = return_data.rank(ascending=False)

    rebuild_constraints = [constraints[i][-1] for i in rank_return.index]
    rebuild_constraints = pd.Series(rebuild_constraints, index=rank_return.index)

    remaining_weight = 1
    upStatus = pd.Series(np.zeros(cov_mat.shape[0]), index=cov_mat.index)
    inStatus = pd.Series(np.zeros(cov_mat.shape[0]), index=cov_mat.index)

    i = 1
    while remaining_weight > 0:
        obj_asset = rank_return[rank_return == i].index[0]
        securityLimit = constraints[obj_asset][-1]

        if securityLimit < remaining_weight:
            upStatus[obj_asset] = 1
            remaining_weight += - securityLimit
        else:
            inStatus[obj_asset] = 1
            remaining_weight = 0
        i += 1

    add_row = pd.DataFrame(-1 * np.ones(cov_mat.shape[0]), index=cov_mat.index, columns=['add_1'])
    init_w = pd.concat([2 * cov_mat, add_row], axis=1)
    add_col = pd.DataFrame(np.hstack([np.ones(init_w.shape[0]), np.zeros(1)]).reshape(1, -1), index=['add_2'],
                           columns=init_w.columns)
    init_w = pd.concat([init_w, add_col])

    H_vec = np.hstack([np.zeros(cov_mat.shape[0]), np.ones(1)])
    K_vec = np.hstack([np.array(return_data), np.zeros(1)])

    negIdentity = -1 * np.identity(init_w.shape[0])
    negIdentity = negIdentity.astype(np.int)

    identity = np.identity(init_w.shape[0])
    identity = identity.astype(np.int)

    matrixDim = init_w.shape[0]

    weight_limit_mat = np.array(rebuild_constraints)
    weight_limit_mat = np.array([weight_limit_mat for _ in range(matrixDim)])

    outStatus = 1 - inStatus - upStatus

    expVol = np.inf
    lambda_1 = 100
    count = 0
    turningpoints = pd.DataFrame([])

    while lambda_1 > 0 and count < maxiter:
        oldLambda = lambda_1
        oldVol = expVol

        count += 1

        inMat = np.hstack([np.array(inStatus), np.ones(1)])
        inMat = np.array([inMat for _ in range(init_w.shape[0])]).astype(np.int)

        upMat = np.hstack([np.array(upStatus), np.zeros(1)])
        upMat = np.array([upMat for _ in range(init_w.shape[0])]).astype(np.int)

        outMat = np.hstack([np.array(outStatus), np.zeros(1)])
        outMat = np.array([outMat for _ in range(init_w.shape[0])]).astype(np.int)

        W = inMat * init_w + upMat * identity + outMat * negIdentity
        inv_W = np.linalg.inv(np.array(W))

        modified_H = H_vec - np.sum(weight_limit_mat * upMat[:, :-1] * np.array(init_w)[:, :-1], axis=1)
        A_vec = np.dot(inv_W, modified_H)
        B_vec = np.dot(inv_W, K_vec)

        truncA = A_vec[:-1]
        truncB = B_vec[:-1]

        inRatio = np.zeros(cov_mat.shape[0])
        inRatio[truncB > 0] = -truncA[truncB > 0] / truncB[truncB > 0]

        upRatio = np.zeros(cov_mat.shape[0])
        upRatio = pd.Series(upRatio, index=cov_mat.index)
        upRatioIndices = (inStatus == True) & pd.Series(truncB < 0, index=inStatus.index)
        if upRatioIndices.sum() > 0:
            upRatio[upRatioIndices == True] = \
                (rebuild_constraints[upRatioIndices == True] - pd.Series(truncA, index=cov_mat.index)[
                    upRatioIndices == True]) / \
                pd.Series(truncB, index=cov_mat.index)[upRatioIndices == True]

        maxInRatio = inRatio.max()
        maxUpRatio = upRatio.max()
        lambda_1 = np.max([maxInRatio, maxUpRatio])

        wts = inStatus * (truncA + truncB * lambda_1) + upStatus * rebuild_constraints + upStatus * 0

        expRet = np.dot(return_data, wts)
        expVol = np.sqrt(np.dot(np.dot(wts, cov_mat), wts))

        turningPoint = pd.DataFrame([count, expRet, lambda_1, expVol], index=['CP', 'Exp. Ret.', 'Lambda', 'Exp. Vol.'],
                                    columns=[count])
        turningPoint = pd.concat([turningPoint, pd.DataFrame(wts, columns=[count])]).T

        turningpoints = pd.concat([turningpoints, turningPoint])

        if oldVol == np.inf and expVol < target_vol:
            threshWts = turningpoints.iloc[-1]
            return threshWts
        elif oldVol > target_vol and expVol < target_vol:
            upLambda = oldLambda
            dnLambda = lambda_1
            meanLambda = (upLambda + dnLambda) / 2

            while (upLambda - dnLambda) > 0.00001:
                meanLambda = (upLambda + dnLambda) / 2
                wts = inStatus * (truncA + truncB * meanLambda) + upStatus * rebuild_constraints + upStatus * 0

                expRet = np.dot(return_data, wts)
                expVol = np.sqrt(np.dot(np.dot(wts, cov_mat), wts))

                if expVol < target_vol:
                    dnLambda = meanLambda
                else:
                    upLambda = meanLambda

            threshWts = pd.DataFrame([count, expRet, meanLambda, expVol],
                                     index=['CP', 'Exp. Ret.', 'Lambda', 'Exp. Vol.'], columns=[count])
            threshWts = pd.concat([threshWts, pd.DataFrame(wts, columns=[count])]).T

            turningpoints = pd.concat([turningpoints, threshWts])
            return turningpoints.iloc[-1]

        if maxInRatio > maxUpRatio:
            inStatus[inRatio == maxInRatio] = 1 - inStatus[inRatio == maxInRatio]
            upStatus[inRatio == maxInRatio] = 0
        else:
            upStatus[upRatio == maxUpRatio] = 1 - upStatus[upRatio == maxUpRatio]
            inStatus[upRatio == maxUpRatio] = 0

            outStatus = 1 - inStatus - upStatus

    return turningpoints.iloc[-1]
