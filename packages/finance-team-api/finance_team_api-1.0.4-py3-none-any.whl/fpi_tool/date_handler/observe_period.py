from .monthly_adjust import *


# observe_window = skip_term = 'Daily Setting'
def window_sub_daily_daily(date
                           , observe_window
                           , skip_term=None
                           , coin_market=None):
    # 최근 제외되는 날에 따른 데이터 관측 기간의 끝을 설정
    if skip_term is not None:
        if coin_market is not None:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term)[0]
        else:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term
                                             , freq='B')[0]
    else:
        observe_end_date = date

    # 데이터 관측 시작 시점 설정
    if coin_market is not None:
        observe_start_date = pd.date_range(end=observe_end_date
                                           , periods=observe_window)[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date)
    else:
        observe_start_date = pd.date_range(end=observe_end_date
                                           , periods=observe_window
                                           , freq='B')[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date
                             , freq='B')

# observe_window = 'Daily Setting'
# skip_term = 'Monthly Setting'
def window_sub_daily_monthly(date
                             , observe_window
                             , skip_term=None
                             , coin_market=None):
    # 데이터 관측 기간의 끝을 설정
    if (skip_term is not None) & (coin_market is not None):
        #   skip_term   coin_market   bm_date==date
        #       o           o               o
        if date == pd.date_range(end=date
                                 , periods=1
                                 , freq='M')[0]:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term + 1
                                             , freq='M')[0]

        #   skip_term   coin_market   bm_date==date
        #       o           o               x
        else:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term
                                             , freq='M')[0]
            adj_len = monthly_adjust(date=date
                                     , coin_market=True)
            observe_end_date = pd.date_range(end=observe_end_date
                                             , periods=adj_len)[0]

    elif (skip_term is not None) & (coin_market is None):
        #   skip_term   coin_market   bm_date==date
        #       o           x               o
        if date == pd.date_range(end=date
                                 , periods=1
                                 , freq='BM')[0]:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term +1
                                             , freq='BM')[0]

        #   skip_term   coin_market   bm_date==date
        #       o           x               x
        else:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term
                                             , freq='BM')[0]
            adj_len = monthly_adjust(date=date)
            observe_end_date = pd.date_range(end=observe_end_date
                                             , periods=adj_len
                                             , freq='B')[0]

    # skip_term   coin_market   bm_date==date
    #       x         N/A            N/A
    else:
        observe_end_date = date

    # 데이터 관측 시작 시점 설정
    # skip_term   coin_market   bm_date==date
    #     N/A          o            N/A
    if coin_market is not None:
        observe_start_date = pd.date_range(end=observe_end_date
                                           , periods=observe_window)[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date)
    # skip_term   coin_market   bm_date==date
    #     N/A          x            N/A
    else:
        observe_start_date = pd.date_range(end=observe_end_date
                                           , periods=observe_window
                                           , freq='B')[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date
                             , freq='B')

# observe_window = 'Monthly Setting'
# skip_term = 'Daily Setting'
def window_sub_monthly_daily(date
                             , observe_window
                             , skip_term=None
                             , coin_market=None):
    # 데이터 관측 기간의 끝을 설정
    if (skip_term is not None) & (coin_market is not None):
        #   skip_term   coin_market
        #       o           o
        observe_end_date = pd.date_range(end=date
                                         , periods=skip_term + 1)[0]

    elif (skip_term is not None) & (coin_market is None):
        #   skip_term   coin_market
        #       o           x
        observe_end_date = pd.date_range(end=date
                                         , periods=skip_term + 1
                                         , freq='B')[0]
    else:
        # skip_term   coin_market
        #       x         N/A
        observe_end_date = date

    # 데이터 관측 시작 시점 설정
    if coin_market is not None:
        # skip_term   coin_market   bm_date==observe_end_date
        #     N/A          o                o
        if observe_end_date == pd.date_range(end=observe_end_date
                                             , periods=1
                                             , freq='M')[0]:
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window + 1
                                               , freq='M')[0]
        else:
            # skip_term   coin_market   bm_date==observe_end_date
            #     N/A          o            x
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window
                                               , freq='M')[0]
            adj_len = monthly_adjust(date=observe_end_date
                                     , coin_market=True)
            observe_start_date = pd.date_range(end=observe_start_date
                                               , periods=adj_len)[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date)
    else:
        # skip_term   coin_market   bm_date==observe_end_date
        #     N/A          x                o
        if observe_end_date == pd.date_range(end=observe_end_date
                                             , periods=1
                                             , freq='BM')[0]:
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window + 1
                                               , freq='BM')[0]
        else:
            # skip_term   coin_market   bm_date==observe_end_date
            #     N/A          x                x
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window + 1
                                               , freq='BM')[0]
            adj_len = monthly_adjust(date=observe_end_date)
            observe_start_date = pd.date_range(end=observe_start_date
                                               , periods=adj_len
                                               , freq='B')[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date
                             , freq='B')

# observe_window = 'Monthly Setting'
# skip_term = 'Monthly Setting'
def window_sub_monthly_monthly(date
                               , observe_window
                               , skip_term=None
                               , coin_market=None):
    # 데이터 관측 기간의 끝을 설정
    if (skip_term is not None) & (coin_market is not None):
        #   skip_term   coin_market   bm_date
        #       o           o            o
        if date == pd.date_range(end=date
                                 , periods=1
                                 , freq='M')[0]:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term + 1
                                             , freq='M')[0]
        else:
            #   skip_term   coin_market   bm_date
            #       o           o            x
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term
                                             , freq='M')[0]
            adj_len = monthly_adjust(date=date
                                     , coin_market=True)
            observe_end_date = pd.date_range(end=observe_end_date
                                             , periods=adj_len)[0]

    elif (skip_term is not None) & (coin_market is None):
        #   skip_term   coin_market   bm_date
        #       o           x            o
        if date == pd.date_range(end=date
                                 , periods=1
                                 , freq='BM')[0]:
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term + 1
                                             , freq='BM')[0]
        else:
            # skip_term   coin_market   bm_date
            #       o           x          x
            observe_end_date = pd.date_range(end=date
                                             , periods=skip_term
                                             , freq='BM')[0]
            adj_len = monthly_adjust(date=date)
            observe_end_date = pd.date_range(end=observe_end_date
                                             , periods=adj_len
                                             , freq='B')[0]
    else:
        # skip_term   coin_market
        #       x         N/A
        observe_end_date = date

    # 데이터 관측 시작 시점 설정
    if coin_market is not None:
        # skip_term   coin_market   bm_date==observe_end_date
        #     N/A          o                o
        if observe_end_date == pd.date_range(end=observe_end_date
                                             , periods=1
                                             , freq='M')[0]:
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window + 1
                                               , freq='M')[0]
        else:
            # skip_term   coin_market   bm_date==observe_end_date
            #     N/A          o            x
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window
                                               , freq='M')[0]
            adj_len = monthly_adjust(date=observe_end_date
                                     , coin_market=True)
            observe_start_date = pd.date_range(end=observe_start_date
                                               , periods=adj_len)[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date)
    else:
        # skip_term   coin_market   bm_date==observe_end_date
        #     N/A          x                o
        if observe_end_date == pd.date_range(end=observe_end_date
                                             , periods=1
                                             , freq='BM')[0]:
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window + 1
                                               , freq='BM')[0]
        else:
            # skip_term   coin_market   bm_date==observe_end_date
            #     N/A          x                x
            observe_start_date = pd.date_range(end=observe_end_date
                                               , periods=observe_window + 1
                                               , freq='BM')[0]
            adj_len = monthly_adjust(date=observe_end_date)
            observe_start_date = pd.date_range(end=observe_start_date
                                               , periods=adj_len
                                               , freq='B')[0]
        return pd.date_range(start=observe_start_date
                             , end=observe_end_date
                             , freq='B')


def get_observe_period(date
                       , observe_window
                       , skip_term=None
                       , coin_market=None):
    """
    :param date: DateTime object, MP 산출일
    :param observe_window: str, 관측 주기 설정
                          : N(str)일 단위, Month(str)단위
    :param skip_term: str, 최근 데이터 제외 주기 설정
                     : N(str)일 단위, Month(str)단위
    :param coin_market: Boolean, 주말 포함날짜 산출을 위해 필요함
    :return: DateTimeIndex([]), 데이터 관측기간이 되는 날짜

    Example
    2019-09-30기준 과거 30일 데이터 관측 window_date(date='2019-09-30', observe_window='30D')
    2019-09-30기준 과거 1개월 데이터 관측 window_date(date='2019-09-30', observe_window='1M')
    """

    # 자료형 Datetime으로 변환
    c_date = pd.to_datetime(date)

    # 오류 검사
    # observe_window is string type
    if type(observe_window) != str:
        raise AttributeError("observe_window는 string type이어야 합니다.")

    # 오류 검사
    # skip_term is string type or None
    if (skip_term is not None) & (type(skip_term) != str):
        raise AttributeError("skip_term은 string type이어야 합니다.")

    # 오류 검사
    # 증권 시장의 경우 c_date가 weekend의 날짜일 경우 데이터에 문제가 있음
    # 암호화폐 시장의 경우 c_date가 weekend도 가능함
    if coin_market is not None:
        if c_date != pd.date_range(c_date
                                   , periods=1
                                   , freq='B')[0]:
            raise AttributeError("Data have weekend")

    observe_window_num = int(observe_window[:-1])
    observe_window_type = observe_window[-1]
    if skip_term is not None:
        skip_term_num = int(skip_term[:-1])
        skip_term_type = skip_term[-1]

    date_set = None
    if (coin_market is not None) & (observe_window_type=='D') & (skip_term is not None):
        # coin_market   observe_window   skip_term
        #     o            Daily          Daily
        if skip_term_type == 'D':
            date_set = window_sub_daily_daily(date=c_date
                                              , observe_window=observe_window_num
                                              , skip_term=skip_term_num
                                              , coin_market=True)
        # coin_market   observe_window   skip_term
        #     o            Daily          Monthly
        elif skip_term_type == 'M':
            date_set = window_sub_daily_monthly(date=c_date
                                                , observe_window=observe_window_num
                                                , skip_term=skip_term_num
                                                , coin_market=True)

    if (coin_market is None) & (observe_window_type == 'D') & (skip_term is not None):
        # coin_market   observe_window   skip_term
        #     x            Daily          Daily
        if skip_term_type == 'D':
            date_set = window_sub_daily_daily(date=c_date
                                              , observe_window=observe_window_num
                                              , skip_term=skip_term_num)
        # coin_market   observe_window   skip_term
        #     x            Daily          Monthly
        elif skip_term_type == 'M':
            date_set = window_sub_daily_monthly(date=c_date
                                                , observe_window=observe_window_num
                                                , skip_term=skip_term_num)

    if (coin_market is not None) & (observe_window_type=='M') & (skip_term is not None):
        # coin_market   observe_window   skip_term
        #     o            Monthly         Daily
        if skip_term_type == 'D':
            date_set = window_sub_monthly_daily(date=c_date
                                                , observe_window=observe_window_num
                                                , skip_term=skip_term_num
                                                , coin_market=True)
        # coin_market   observe_window   skip_term
        #     o            Monthly         Monthly
        elif skip_term_type == 'M':
            date_set = window_sub_monthly_monthly(date=c_date
                                                  , observe_window=observe_window_num
                                                  , skip_term=skip_term_num
                                                  , coin_market=True)
    if (coin_market is None) & (observe_window_type == 'M') & (skip_term is not None):
        # coin_market   observe_window   skip_term
        #     x            Monthly         Daily
        if skip_term_type == 'D':
            date_set = window_sub_monthly_daily(date=c_date
                                                , observe_window=observe_window_num
                                                , skip_term=skip_term_num)
        # coin_market   observe_window   skip_term
        #     x            Monthly         Daily
        elif skip_term_type == 'M':
            date_set = window_sub_monthly_monthly(date=c_date
                                                  , observe_window=observe_window_num
                                                  , skip_term=skip_term_num)

    if (coin_market is not None) & (observe_window_type == 'D') & (skip_term is None):
        # coin_market   observe_window   skip_term
        #     o            Daily            x
        date_set = window_sub_daily_daily(date=c_date
                                          , observe_window=observe_window_num
                                          , coin_market=True)

    if (coin_market is not None) & (observe_window_type == 'M') & (skip_term is None):
        # coin_market   observe_window   skip_term
        #     o            Monthly            x
        date_set = window_sub_monthly_daily(date=c_date
                                            ,observe_window=observe_window_num
                                            ,coin_market=True)

    if (coin_market is None) & (observe_window_type == 'D') & (skip_term is None):
        # coin_market   observe_window   skip_term
        #     x            Daily             x
        date_set = window_sub_daily_daily(date=c_date
                                          , observe_window=observe_window_num)

    if (coin_market is None) & (observe_window_type == 'M') & (skip_term is None):
        # coin_market   observe_window   skip_term
        #     x            Daily             x
        date_set = window_sub_monthly_daily(date=c_date
                                            , observe_window=observe_window_num)

    return date_set