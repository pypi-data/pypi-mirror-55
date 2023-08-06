from ..date_handler.observe_period import *
import numpy as np
from scipy.optimize import minimize

def reformat_data(data):
    # 오류검사
    # data에는 Asset_Class가 명시되어야 함.
    try:
        asset_class = data.loc['Asset_Class']
    except KeyError as e:
        raise AttributeError("Raw Price Data에 'Asset_Class'가 없습니다.")

    # 오류검사
    # Asset명과 Asset Class의 명칭은 달라야 함(Cash제외)
    if (len(asset_class[asset_class.index == asset_class]) == 1) \
            & (asset_class[asset_class.index == asset_class].index[0] != 'Cash'):
        raise AttributeError("자산명과 Asset_Class 명은 'Cash'를 제외하고 모두 달라야 합니다.")
    elif len(asset_class[asset_class.index == asset_class]) > 1:
        raise AttributeError("자산명과 Asset_Class 명은 'Cash'를 제외하고 모두 달라야 합니다.")

    # Asset_Class명에 따른 정렬 후 위치 Vector 추출
    # 이때 자산명이 Cash이고 Asset Class도 Cash일 경우
    # Asset Class는 cash로 인식할 것임.
    arrange = asset_class.sort_values().to_frame()

    data = data[arrange.index].drop(index=['Asset_Class'])
    data.index = pd.to_datetime(data.index)

    arrange['num'] = range(len(arrange))

    num_to_dict = {}
    for a_c in arrange['Asset_Class'].drop_duplicates():
        obj_set = arrange[arrange['Asset_Class']==str(a_c)]['num'].values
        min_val = np.min(obj_set)
        max_val = np.max(obj_set)

        if a_c == 'Cash':
            a_c = 'cash'
        num_to_dict[str(a_c)] = [min_val, max_val]

    return data.astype(float)\
        , num_to_dict\
        , arrange['Asset_Class']


def constraints_setting_error(message):
    raise BaseException('Constraints Setting Error : {}'.format(message))


def kelly_function(array
                   , loc_vector
                   , asset_class_table
                   , constraints
                   , prev_AP=None
                   , turnover_constraint=None):
    """

    :param array: DataFrame(return_table, index=TimeStamp, columns=AssetName)
    :param loc_vector : Dictionary
                 {'Stock' : [0,10], 'Bond' : [11,12], ...}
    :param asset_class_table : DataFrame(Asset_Class_Table, index=AssetName)
    :param constraints: Dictionary
                 {'자산명' : {'Bound' : (lb, ub)} ...required
                 'class_name' : (lb, ub) ....required
                 'Turnover' : constant ...optional}
    :param prev_AP: pandas Series, 직전 포트폴리오
    :param turnover_constraint : float, 포트폴리오 턴오버 제한으로 단위는 선택가능
    :return: DataFrame(weight, index=rebalance_date, columns=AssetName)
    """
    # 오류검사
    # array는 DataFrame 형식이어야 함
    if array.__class__ != pd.DataFrame([]).__class__:
        raise AttributeError("Kelly Portfolio의 Input은 Timestamp와 자산명을 가진 DataFrame이어야 합니다.")

    # 오류검사
    # array에는 NaN값이 없어야 함
    if np.isnan(array).sum().sum() > 0:
        raise AttributeError("데이터에 NaN값이 있습니다.")

    # 오류검사
    # constraints는 Dictionary type이어야 함
    if constraints.__class__ != {}.__class__:
        raise AttributeError("Constraints는 Dictionary Type이며 자세한 내용은 Document를 참고하세요.")

    # 오류검사
    # constraints에 모든 asset name이 들어가야 함.
    for name in array.columns:
        if name not in constraints.keys():
            constraints_setting_error(message='자산에 대한 Constraint를 정의하세요.')

    # 오류검사
    # 각 자산명에 대한 Asset Class가 정의되어야 함
    for name in array.columns:
        try:
            asset_class = asset_class_table[name]
        except KeyError as e:
            raise constraints_setting_error(message='자산군을 정의하세요.')

    # 오류검사
    # 자산군에 대한 Constraints가 정의되어야 함.
    for ind_asset_class in asset_class_table.drop_duplicates():
        try:
            ind_asset_class_bounds = constraints[str(ind_asset_class)]
        except KeyError as e:
            raise constraints_setting_error(message='자산군에 대한 Bound를 정의하세요.')

    # 오류검사
    # 포트폴리오 turnover 제한이 있다면 prev_AP는 Required임
    if (turnover_constraint is not None) & (prev_AP is None):
        raise AttributeError("Turnover Ratio 제한시 prev_AP는 반드시 필요합니다.")

    # 각 자산명
    asset = array.columns

    # return table 자료형 조정
    array = np.array(array
                     , dtype=np.float32)

    # 각 자산의 Boundary 정의
    # turnover_constraint가 전달될 경우 prev_AP에 따라 포트폴리오의 제한조건은 변동됨.
    if turnover_constraint is not None:
        bounds = []
        for i in asset:
            lb = constraints[i]['Bound'][0]
            ub = constraints[i]['Bound'][1]
            adj_lb = prev_AP[i] \
                     - turnover_constraint
            adj_ub = prev_AP[i] \
                     + turnover_constraint

            # lb조정
            if adj_lb < lb:
                get_lb = lb
            else:
                get_lb = adj_lb

            # ub조정
            if adj_ub > ub:
                get_ub = ub
            else:
                get_ub = adj_ub

            # lb, ub에 대한 오류검사
            # lb가 ub보단 클 수 없음
            if get_lb > get_ub:
                raise RecursionError("Turnover 제약이 너무 적어 lb > ub의 상황이 발생합니다.")

            bounds.append((get_lb, get_ub))
    else:
        bounds = []
        for i in asset:
            bounds.append(constraints[i]['Bound'])

    # Constraint 정의
    # 특정 자산군의 비중에 대한 Boundary 및 전체 포트폴리오 비중에 대한 정의를 할 수 있다.
    cons = []
    for i in loc_vector.keys():
        lower_bound = constraints[i][0]
        upper_bound = constraints[i][1]

        st_point = loc_vector[i][0]
        end_point = loc_vector[i][1]

        if lower_bound > 0:
            cons.append({'type': 'ineq', 'fun': lambda w: np.sum(w[st_point:end_point]) - lower_bound})

        if upper_bound < 1:
            cons.append({'type': 'ineq', 'fun': lambda w: -np.sum(w[st_point:end_point]) + lower_bound})

    cons.append({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    # prev_AP의 자료형 조정
    # 현재의 자산 순서와 동일하게 순서 조정
    if prev_AP is not None:
        prev_AP = prev_AP.loc[asset_class_table.index]

    # Optimize Inital Point정의
    # 동일 비중으로 우선 배분
    w0 = np.ones(array.shape[1]) \
         * (1 / array.shape[1])


    # Cost 반영 Optimize모델
    # port_weight은 직전 AP(Actual Portfolio)
    def kelly_function_cost_optim(w
                                  , ret_set):
        cost = np.sum(abs(np.array(prev_AP) - w)) \
               * 0.001
        return -(np.log(1 - cost)
               + np.sum(np.log(1 + np.dot(ret_set, w)))) \
               / len(ret_set)

    # Cost 반영x Optimize모델
    def kelly_function(w
                       , ret_set):
        return -(np.sum(np.log(1 + np.dot(ret_set, w)))) \
               / len(ret_set)

    if prev_AP is not None:
        set_function = minimize(kelly_function_cost_optim
                                , w0
                                , array
                                , method='SLSQP'
                                , bounds=bounds
                                , constraints=cons)
    else:
        set_function = minimize(kelly_function
                                , w0
                                , array
                                , method='SLSQP'
                                , bounds=bounds
                                , constraints=cons)

    # 불필요한 비중 제거
    optim_weight = set_function.x
    optim_weight[optim_weight < 0.0001] = 0

    # 자료형 조정
    weight = pd.DataFrame(optim_weight.reshape(1, -1)
                          , columns=asset_class_table.index)

    return weight



    # data = pd.read_csv('./total_price.csv', index_col=0)
    # new_data, asset_class_boundary, class_frame = reformat_data(data)
    #
    # bond = class_frame[class_frame=='Bond']
    # stock = class_frame[class_frame=='Stock']
    # commodity = class_frame[class_frame=='Commodity']
    #
    # bounds = {}
    # for i in data.columns:
    #     bounds[i] = {'Bound' : (0,0.2)}
    # bounds['Bond'] = (0.3, 0.8)
    # bounds['Stock'] = (0, 0.4)
    # bounds['Commodity'] = (0.2, 0.5)
    # bounds['cash'] = (0, 0.8)
    #
    # ret_table = new_data / new_data.shift(1) - 1
    #
    # collect = pd.DataFrame([])
    #
    # for i in pd.date_range('2011-01-01', '2019-01-01', freq='BM'):
    #     observe_period = get_observe_period(date=i,
    #                                         observe_window='100D')
    #     if len(collect) == 0:
    #         get_optim = kelly_function(ret_table.loc[observe_period], asset_class_boundary, class_frame, bounds)
    #     else:
    #         prev = pd.date_range(end=i, periods=2, freq='BM')[0]
    #         get_optim = kelly_function(ret_table.loc[observe_period], asset_class_boundary, class_frame, bounds, collect.loc[prev], 2)
    #     get_optim.index = [i]
    #     collect = pd.concat([collect, get_optim])
    #     print(collect)