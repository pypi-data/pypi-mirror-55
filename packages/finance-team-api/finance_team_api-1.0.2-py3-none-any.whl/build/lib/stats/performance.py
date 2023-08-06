import pandas as pd
import numpy as np
from date_handler.monthly_adjust import *


def cum_ret_dummy(ret_array, MP_array):
    ret_array[0,:] = MP_array
    price = ret_array.cumprod(axis=0)
    return price


def cum_ret_dummy_with_AP(ret_array, MP_array, AP_array, cost):
    """
    :param ret_array: numpy array, 수익률정보
    :param MP_array: numpy array, MP정보
    :param AP_array: numpy array, AP정보
    :param cost: float, 포트폴리오 거래비용
    :return: 누적수익률, 포트폴리오 거래비용
    """
    AP = AP_array / AP_array.sum()
    portfolio_cost_ratio = np.sum(abs(MP_array - AP)) * cost
    principal = AP_array.sum() * (1 - portfolio_cost_ratio)
    ret_array[0,:] = principal * MP_array
    price = ret_array.cumprod(axis=0)
    return price, AP_array.sum() * portfolio_cost_ratio



def cumulative_ret(price_data, MP, cost=0.0015, holding_freq=None):
    """
    :param price_data: DataFrame, price_data dataframe으로 MP와 column명이 일치 해야 함.
    :param MP: DataFrame or Series, Model Portfolio
    :param cost : float, 포트폴리오 거래비용
    :param holding_freq: None or string, required if MP have one portfolio
    :return: 자산별 Accum_retrun, Total Accum_return, Portfolio Cost(only multiple MP)
    """

    # 오류 검사 및 자산 순서 조정 그리고 MP의 자료형 조정(numpy)
    # MP가 하나일 경우 holding freq를 지정해야 하며 MP가 하나 이상일 경우 holding_freq를 지정하면 안됨.
    # 포트폴리오 순서와 price_data 순서를 조정하기 위함.
    if (type(MP) == type(pd.DataFrame([]))) & (len(MP.index) == 1):
        #[오류] 포트폴리오   포트폴리오 구조   holding_freq
        #           단일           DataFrame          x
        if holding_freq is None:
            raise AttributeError('MP가 1개일 경우 holding_freq를 지정해야 합니다.')
        #[정상] 포트폴리오   포트폴리오 구조   holding_freq
        #          단일           DataFrame          o
        else:
            cols = MP.columns
            for i in cols:
                if i not in price_data.columns:
                    raise AttributeError('MP와 price_data의 컬럼명이 일치하지 않습니다.')
            rebal_date = MP.index[0]
            MP = np.array(MP.fillna(0), dtype=float).reshape(-1)

    elif (type(MP) == type(pd.DataFrame([]))) & (len(MP.index) > 1):
        #[오류] 포트폴리오   포트폴리오 구조   holding_freq
        #          멀티           DataFrame          o
        if holding_freq is not None:
            raise AttributeError('MP가 1개 이상일 경우 holding_freq를 지정하면 안됩니다.')
        #[정상] 포트폴리오   포트폴리오 구조   holding_freq
        #          멀티           DataFrame          x
        else:
            cols = MP.columns
            for i in cols:
                if i not in price_data.columns:
                    raise AttributeError('MP와 price_data의 컬럼명이 일치하지 않습니다.')
            rebal_date = MP.index
            MP = np.array(MP.fillna(0), dtype=float)

    elif type(MP) == type(pd.Series([])):
        #[오류] 포트폴리오   포트폴리오 구조   holding_freq
        #          단일           Series            x
        if holding_freq is None:
            raise AttributeError('MP가 1개일 경우 holding_freq를 지정해야 합니다.')
        #[정상] 포트폴리오   포트폴리오 구조   holding_freq
        #         단일           Series             o
        else:
            cols = MP.index
            for i in cols:
                if i not in price_data.columns:
                    raise AttributeError('MP와 price_data의 컬럼명이 일치하지 않습니다.')
            rebal_date = MP.name
            MP = np.array(MP.fillna(0), dtype=float).reshape(-1)

    # 오류검사 및 산출일 결정
    # 단일 포트폴리오에 대해 holding_freq가 결정될 경우 포트폴리오 보유일에 대한
    # price_data는 모두 존재해야 한다.
    if holding_freq is not None:
        holding_freq_num = int(holding_freq[:-1])
        holding_freq_type = holding_freq[-1].upper()

        if holding_freq_type == 'D':
            st = pd.date_range(start=rebal_date,
                               periods=2,
                               freq='B')[-1]
            end = pd.date_range(start=st,
                                periods=holding_freq_num,
                                freq='B')[-1]

            if end > price_data.index[-1]:
                raise AttributeError("가격 데이터로 {}까지의 cumulative return을 구할 수 없습니다.".format(end.strftime("%Y-%m-%d")))
        elif holding_freq_type == 'M':
            st = pd.date_range(start=rebal_date,
                               periods=2,
                               freq='B')[-1]
            end = pd.date_range(start=st,
                                periods=holding_freq_num,
                                freq='BM')[-1]
            adj_len = monthly_adjust(date=st)
            end = pd.date_range(end=end,
                                periods=adj_len,
                                freq='B')[0]
            if end > price_data.index[-1]:
                raise AttributeError("가격 데이터로 {}까지의 cumulative return을 구할 수 없습니다.".format(end.strftime("%Y-%m-%d")))

    price_data = price_data[cols]
    ret_data = price_data / price_data.shift(1)

    # 멀티 포트폴리오일 경우 포트폴리오 보유일과 rebalancing일 결정
    if len(rebal_date) > 1:
        matching_rebal_index = {}
        for k in range(len(rebal_date)):
            if k != len(rebal_date)-1:
                st_holding = pd.date_range(start=rebal_date[k],
                                         periods=2,
                                         freq='B')[-1]
                end_holding = rebal_date[k+1]
                matching_rebal_index[rebal_date[k]] = [st_holding, end_holding]
            else:
                st_holding = pd.date_range(start=rebal_date[k],
                                         periods=2,
                                         freq='B')[-1]
                end_holding = price_data.index[-1]
                # 마지막 포트폴리오의 cum_ret산출일이 사용가능한 price_data의 끝과 동일할 경우 pass
                if st_holding == end_holding:
                    pass
                else:
                    matching_rebal_index[rebal_date[k]] = [st_holding, end_holding]


    # 멀티 포트폴리오 누적수익률 정보 추출
    try:
        asset_num = MP.shape[1]
        MP_const = 0
        cost_collect = []
        for st_applying_rebal in matching_rebal_index.keys():
            if st_applying_rebal == rebal_date[0]:
                [first_point, end_point] = matching_rebal_index[st_applying_rebal]
                obj_return = ret_data.loc[first_point : end_point]
                get_MP = MP[MP_const,:]
                ind_dummy_cum_ret = cum_ret_dummy(ret_array=np.array(obj_return, dtype=float),
                                              MP_array=get_MP)
                dummy_cum_ret = ind_dummy_cum_ret.copy()
                MP_const += 1
            else:
                [st_point, end_point] = matching_rebal_index[st_applying_rebal]
                obj_return = ret_data.loc[st_point: end_point]
                get_MP = MP[MP_const, :]
                ind_dummy_cum_ret, cost = cum_ret_dummy_with_AP(ret_array=np.array(obj_return, dtype=float),
                                                      MP_array=get_MP,
                                                      AP_array=dummy_cum_ret[-1,:],
                                                      cost=cost)
                cost_collect.append(cost)
                dummy_cum_ret = np.concatenate((dummy_cum_ret, ind_dummy_cum_ret))
                MP_const += 1

        indexer = pd.date_range(start=first_point,
                                end=end_point,
                                freq='B')
        cost_to_frame = pd.DataFrame(cost_collect,
                                     index=rebal_date[1:],
                                     columns=['Portfolio_Cost'])
        cum_ret_to_frame = pd.DataFrame(dummy_cum_ret,
                                        index=indexer,
                                        columns=cols)
        total = pd.DataFrame(dummy_cum_ret.sum(axis=1),
                             index=indexer,
                             columns=['Cumulative_Return'])

        return cum_ret_to_frame, total, cost_to_frame

    # 단일 포트폴리오 누적 수익률 정보 추출
    except IndexError as e:
        obj_return = ret_data.loc[st : end]
        obj_return = np.array(obj_return, dtype=float)

        cum_ret = cum_ret_dummy(ret_array=obj_return,
                                MP_array=MP)

        indexer = pd.date_range(start=st,
                                end=end,
                                freq='B')
        cum_ret_to_frame = pd.DataFrame(cum_ret,
                                        index=indexer,
                                        columns=cols)
        total = pd.DataFrame(cum_ret.sum(axis=1),
                             index=indexer,
                             columns=['Cumulative_Return'])

        return cum_ret_to_frame, total


if __name__ == '__main__':
    data = pd.read_csv('../asset_allocation/total_price.csv', index_col=0)
    from asset_allocation.kelly_portfolio import reformat_data, kelly_function
    from date_handler.observe_period import *


    new_data, asset_class_boundary, class_frame = reformat_data(data)

    bond = class_frame[class_frame=='Bond']
    stock = class_frame[class_frame=='Stock']
    commodity = class_frame[class_frame=='Commodity']

    bounds = {}
    for i in data.columns:
        bounds[i] = {'Bound' : (0,0.2)}
    bounds['Bond'] = (0.3, 0.8)
    bounds['Stock'] = (0, 0.4)
    bounds['Commodity'] = (0.2, 0.5)
    bounds['cash'] = (0, 0.8)

    ret_table = new_data / new_data.shift(1) - 1

    collect = pd.DataFrame([])

    for i in pd.date_range('2011-01-01', '2019-01-01', freq='BM'):
        observe_period = get_observe_period(date=i, observe_window='100D')
        if len(collect) == 0:
            get_optim = kelly_function(ret_table.loc[observe_period], asset_class_boundary, class_frame, bounds)
            get_optim.index = [i]
            collect = pd.concat([collect, get_optim])
        else:
            prev = pd.date_range(end=i, periods=2, freq='BM')[0]
            get_optim = kelly_function(ret_table.loc[observe_period], asset_class_boundary, class_frame, bounds, collect.loc[prev], 2)
            get_optim.index = [i]
            collect = pd.concat([collect, get_optim])
    cumulative_ret(price_data=new_data,
                   MP=collect)
