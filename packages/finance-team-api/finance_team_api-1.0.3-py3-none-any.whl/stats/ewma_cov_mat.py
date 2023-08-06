import os
import pandas as pd
import numpy as np
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
from rpy2 import robjects
os.environ['R_HOME'] = r'C:\Program Files\R\R-3.5.3'
os.environ['R_USER'] = r'C:\ProgramData\Anaconda3\envs\common_version\Lib\site-packages\rpy2'


def ewma_cov_mat(ret_table, lamb=None, mode=None):
    """
    :param ret_table : DataFrame, 수익률 테이블
    :param mode : None or 'R', default 값은 직접 계산이며 R의 패키지를 이용한 연산 가능
    :param lamb : None or float, EWMA 계수
    :return: covariance matrix

    최근의 수익률 변동을 더 반영하는 EWMA Covariance Matrix는 기본적으로 근사 추정을 이용하는 방식이
    사용되지만 Python 패키지에는 이를 지원하는 Function이 없기 때문에 연산을 통해 직접 추정하는 방식과
    연산이 아닌 R 패키지를 이용하는 방식을 지원한다.
    """

    ret_table = ret_table.astype(float)

    if mode == 'R':
        pandas2ri.activate()
        robjects.globalenv['simple_ret_data'] = ret_table
        r("library('RiskPortfolios')")
        r("simple_ret_data <- as.matrix(simple_ret_data)")
        r("x <- covEstimation(simple_ret_data, control=list(type='ewma',lambda=0.94))")
        ewma_cov = r('x')
        return ewma_cov

    elif mode is None:
        for location in range(len(ret_table)):
            V = ret_table.iloc[location]  # .fillna(0) #- simple_ret_data.mean().mean()

            FF_matrix = pd.DataFrame([], index=V.index, columns=V.index)

            k = 0

            for i in FF_matrix.index:
                a = 0
                for j in FF_matrix.columns:
                    FF_matrix.loc[i][j] = V.iloc[k] * V.iloc[a]
                    a += 1
                k += 1

            if location == 0:
                adj_cov_matrix = 0.94 * ret_table.cov() + 0.06 * FF_matrix
            else:
                adj_cov_matrix = 0.94 * adj_cov_matrix + 0.06 * FF_matrix
        return adj_cov_matrix


def ewma_corr_mat(ewma_cov_mat, annualize_constant):
    """
    :param ewma_cov_mat: DataFrame, EWMA Covariance Matrix
    :param annualize_constant: Float, EWMA Covariance Matrix를 연율화 하기 위한 승수
    :return: correlation matrix
    """
    ewma_cov_mat = annualize_constant * ewma_cov_mat
    corr_mat = pd.DataFrame([], index=ewma_cov_mat.index, columns=ewma_cov_mat.columns)
    for i in corr_mat.index:
        for j in corr_mat.columns:
            corr_mat.loc[i][j] = ewma_cov_mat.loc[i][j] / (
                    np.sqrt(ewma_cov_mat.loc[i][i]) * np.sqrt(ewma_cov_mat.loc[j][j]))
    return corr_mat