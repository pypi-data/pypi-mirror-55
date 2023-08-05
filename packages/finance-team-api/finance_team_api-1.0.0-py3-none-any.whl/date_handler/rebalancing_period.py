from date_handler.monthly_adjust import *

# Frequency = Daily
# Weekend = False
def rebal_sub_no_week_daily(start_date, end_date, frequency):
    collect = []
    collect.append(start_date)
    while start_date <= end_date:
        start_date = pd.date_range(start_date,
                                   periods=frequency + 1,
                                   freq='B')[-1]
        if start_date > end_date:
            pass
        else:
            collect.append(start_date)
    return collect

# Frequency = Monthly
# Weekend = False
def rebal_sub_no_week_monthly(start_date, end_date, frequency):

    #start_date가 월 말인 경우

    if start_date == pd.date_range(start_date,
                                   periods=1,
                                   freq='BM')[0]:
        collect = []
        collect.append(start_date)
        while start_date <= end_date:
            start_date = pd.date_range(start_date,
                                       periods=frequency + 1,
                                       freq='BM')[-1]
            if start_date > end_date:
                pass
            else:
                collect.append(start_date)
        return collect

    elif start_date != pd.date_range(start_date,
                                   periods=1,
                                   freq='BM')[-1]:
        collect = []
        collect.append(start_date)
        while start_date <= end_date:
            adj_len_from_bm = monthly_adjust(date=start_date)
            start_date = pd.date_range(start_date,
                                       periods=frequency + 1,
                                       freq='BM')[-1]
            start_date = pd.date_range(end=start_date,
                                       periods=adj_len_from_bm,
                                       freq='B')[0]
            if start_date > end_date:
                pass
            else:
                collect.append(start_date)
        return collect


def rebalancing_point_set(start_date, end_date, frequency, weekend):
    """
    :param start_date: DateTime, 포트폴리오 시작일
    :param end_date : DateTime, 포트폴리오 종료일
    :param frequency: string, MP보유일
    :param weekend : boolean, 주말 포함여부
    :return: list(DateTimeStamp)
    """

    # 오류 검사
    # frequency는 string type
    if type(frequency) is not str:
        raise AttributeError("frequency는 string type 입니다. 5D, 10D, ....")

    # 오류 검사
    # weekend는 string type
    if type(weekend) is not bool:
        raise AttributeError("weekend는 boolean type 입니다.")

    # 오류 검사
    # 주말이 포함되지 않는 경우 rebalancing일은 주말이 될 수 없음
    if pd.date_range(start_date,
                     periods=1,
                     freq='B')[0] != pd.to_datetime(start_date):
        raise AttributeError("rebalancing_date는 주말이 될 수 없습니다.")

    # start_date, end_date 자료형 변환
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)

    # Frequency 자료형 변환
    freq_num = int(frequency[:-1])
    freq_type = frequency[-1]

    if weekend == False:
        if freq_type.upper() == 'D':
            return rebal_sub_no_week_daily(start_date=start_date,
                                           end_date=end_date,
                                           frequency=freq_num)
        elif freq_type.upper() == 'M':
            return rebal_sub_no_week_monthly(start_date=start_date,
                                             end_date=end_date,
                                             frequency=freq_num)
    if weekend == True:
        raise AttributeError("아직 Weekend를 포함한 날짜는 개발하지 않았습니다.")
