from ..error_handler.type_tool import *


def k_holiday():
    holiday = pd.read_csv('./date_handler/korea_holiday.csv'
                          , index_col=0
                          , encoding='CP949')
    holiday.index = pd.to_datetime(holiday.index)
    not_weekend = pd.date_range('2009-01-01'
                                , '2020-12-31'
                                , freq='B')
    weekend = pd.date_range('2009-01-01'
                            , '2020-12-31').drop(not_weekend)

    return holiday.index.union(weekend)

korea_holiday = k_holiday()
in_data = pd.DataFrame(range(len(korea_holiday))
                       , index=korea_holiday)

def _before_date_setting(date):
    """
    :param date: string or DateTime, 날짜
    :return: datetime
    """

    if date in korea_holiday:
        order_num = in_data.loc[date][0]
        prev_order_num = order_num - 1
        prev_date = pd.date_range(end=date
                                  , periods=2
                                  , freq='B')[0]

        if prev_date == in_data[in_data[0] == prev_order_num].index:
            prev_order_num = prev_order_num - 1
            prev_date = pd.date_range(end=prev_date
                                      , periods=2
                                      , freq='B')[0]
            if prev_date == in_data[in_data[0] == prev_order_num].index:
                prev_order_num = prev_order_num - 1
                prev_date = pd.date_range(end=prev_date
                                          , periods=2
                                          , freq='B')[0]

                if prev_date == in_data[in_data[0] == prev_order_num].index:
                    prev_order_num = prev_order_num - 1
                    prev_date = pd.date_range(end=prev_date
                                              , periods=2
                                              , freq='B')[0]

                    if prev_date == in_data[in_data[0] == prev_order_num].index:
                        prev_order_num = prev_order_num - 1
                        prev_date = pd.date_range(end=prev_date
                                                  , periods=2
                                                  , freq='B')[0]

                        if prev_date == in_data[in_data[0] == prev_order_num].index:
                            prev_order_num = prev_order_num - 1
                            prev_date = pd.date_range(end=prev_date
                                                      , periods=2
                                                      , freq='B')[0]
                            raise print("함수 Error.........")
                        else:
                            return prev_date
                    else:
                        return prev_date
                else:
                    return prev_date
            else:
                return prev_date
        else:
            return prev_date
    else:
        return date

def _after_date_setting(date):
    """
    :param date: string or DateTime, 날짜
    :return: datetime
    """

    if date in korea_holiday:
        order_num = in_data.loc[date][0]
        after_order_num = order_num + 1
        after_date = pd.date_range(start=date
                                   , periods=2
                                   , freq='B')[-1]

        if after_date == in_data[in_data[0] == after_order_num].index:
            after_order_num = after_order_num - 1
            after_date = pd.date_range(start=after_date
                                       , periods=2
                                       , freq='B')[-1]
            if after_date == in_data[in_data[0] == after_order_num].index:
                after_order_num = after_order_num - 1
                prev_date = pd.date_range(start=after_date
                                          , periods=2
                                          , freq='B')[-1]

                if after_date == in_data[in_data[0] == after_order_num].index:
                    after_order_num = after_order_num - 1
                    after_date = pd.date_range(start=after_date
                                               , periods=2
                                               , freq='B')[-1]

                    if after_date == in_data[in_data[0] == after_order_num].index:
                        after_order_num = after_order_num - 1
                        after_date = pd.date_range(start=after_date
                                                   , periods=2
                                                   , freq='B')[-1]

                        if after_date == in_data[in_data[0] == after_order_num].index:
                            after_order_num = after_order_num - 1
                            after_date = pd.date_range(start=after_date
                                                       , periods=2
                                                       , freq='B')[-1]
                            raise print("함수 Error.........")
                        else:
                            return after_date
                    else:
                        return after_date
                else:
                    return after_date
            else:
                return after_date
        else:
            return after_date
    else:
        return date

def _freq_b_end_date_range(end
                           , periods):
    """
    :param end: DateTime, 끝 날짜
    :param periods: int, 추출할 날짜 개수
    :return: list(DateTime)
    """
    origin = pd.date_range(end=end
                           , periods=periods+50
                           , freq='B')

    collect = [i for i in origin if i not in korea_holiday]
    return collect[-periods:]

def _freq_b_start_date_range(start
                             , periods):
    """
    :param start: DateTime, 시작 날짜
    :param periods: int, 추출할 날짜 개수
    :return: list(DateTime)
    """

    origin = pd.date_range(start=start
                           , periods=periods + 50
                           , freq='B')

    collect = [i for i in origin if i not in korea_holiday]
    return collect[:periods]

def _freq_b_start_end_date_range(start
                                 , end):
    """
    :param start: DateTime, 시작 날짜
    :param end: DateTime, 끝 날짜
    :return: list(DateTime)
    """

    origin = pd.date_range(start=start
                           , end=end
                           , freq='B')

    collect = [i for i in origin if i not in korea_holiday]
    return collect

def k_date_range(start=None
                 , end=None
                 , periods=None
                 , freq=None):
    """
    :param start: string or DateTime, 시작 날짜
    :param end: string or DateTime, 끝 날짜
    :param periods: int, 추출할 날짜 개수
    :param freq: string, 'B','BM', 'BMS'
    :return: DateTimeIndex
    """

    # start 변수 지정
    if (start is not None) & (start.__class__ == str):
        start = pd.to_datetime(start)

    # end 변수 지정
    if (end is not None) & (end.__class__ == str):
        end = pd.to_datetime(end)

    # 오류 검사
    # periods는 int type이어야 함
    if (periods is not None) & (periods.__class__ != int):
        raise VariableSettingError("periods 변수는 Int Type이어야 합니다.")

    # 오류 검사
    # freq는 Str type이어야 함
    if (freq is not None) & (freq.__class__ != str):
        raise VariableSettingError("freq 변수는 string Type이어야 합니다.")

    # 오류 검사
    # freq 지원 모드는 'B', 'BM', 'BMS'임
    if (freq is not None) & (freq not in ['B', 'BM', 'BMS']):
        raise VariableSettingError("지원하지 않는 freq형식 입니다.")

    # 오류 검사
    # start, end, periods는 함께 쓸 수 없음.
    if (start is not None) and (end is not None):
        if periods is not None:
            raise VariableSettingError("start, end, periods 변수는 공존할 수 없습니다.")


    ####################################################################################################################
    ##################################################Frequency is 'B'##################################################
    ####################################################################################################################
    #   start   end   periods   freq
    #     o      x       o       'B'
    if (start is not None) & (end is None) & (freq == 'B'):
        if periods is None:
            raise VariableSettingError("periods 변수를 지정하세요.")
        else:
            return _freq_b_start_date_range(start=start
                                            , periods=periods)

    #   start   end   periods   freq
    #     x      o       o       'B'
    if (start is None) & (end is not None) & (freq == 'B'):
        if periods is None:
            raise VariableSettingError("periods 변수를 지정하세요.")
        else:
            return _freq_b_end_date_range(end=end
                                          , periods=periods)

    #   start   end   periods   freq
    #     o      o       x       'B'
    if (start is not None) & (end is not None) & (freq == 'B'):
        if periods is not None:
            raise VariableSettingError("periods 변수를 지정할 수 없습니다.")
        else:
            return _freq_b_start_end_date_range(start=start
                                                , end=end)

    ####################################################################################################################
    ##################################################Frequency is 'BM'#################################################
    ####################################################################################################################
    #   start   end   periods   freq
    #     o      x       o       'BM'
    if (start is not None) & (end is None) & (freq == 'BM'):
        if periods is None:
            raise VariableSettingError("periods 변수를 지정하세요.")
        else:
            origin = pd.date_range(start=start
                                   , periods=periods
                                   , freq='BM')
            return [_before_date_setting(i) for i in origin]

    #   start   end   periods   freq
    #     x      o       o       'BM'
    if (start is None) & (end is not None) & (freq == 'BM'):
        if periods is None:
            raise VariableSettingError("periods 변수를 지정하세요.")
        else:
            origin = pd.date_range(end=end
                                   , periods=periods
                                   , freq='BM')
            return [_before_date_setting(i) for i in origin]

    #   start   end   periods   freq
    #     o      o       x       'B'
    if (start is not None) & (end is not None) & (freq == 'BM'):
        if periods is not None:
            raise VariableSettingError("periods 변수를 지정할 수 없습니다.")
        else:
            origin = pd.date_range(start=start
                                   , end=end
                                   , periods=periods
                                   , freq='BM')
            return [_before_date_setting(i) for i in origin]

    ####################################################################################################################
    ##################################################Frequency is 'BMS'################################################
    ####################################################################################################################
    #   start   end   periods   freq
    #     o      x       o       'BMS'
    if (start is not None) & (end is None) & (freq == 'BMS'):
        if periods is None:
            raise VariableSettingError("periods 변수를 지정하세요.")
        else:
            origin = pd.date_range(start=start
                                   , periods=periods
                                   , freq='BMS')
            return [_after_date_setting(i) for i in origin]

    #   start   end   periods   freq
    #     x      o       o       'BMS'
    if (start is None) & (end is not None) & (freq == 'BMS'):
        if periods is None:
            raise VariableSettingError("periods 변수를 지정하세요.")
        else:
            origin = pd.date_range(end=end
                                   , periods=periods
                                   , freq='BMS')
            return [_after_date_setting(i) for i in origin]

    #   start   end   periods   freq
    #     o      o       x       'BMS'
    if (start is not None) & (end is not None) & (freq == 'BMS'):
        if periods is not None:
            raise VariableSettingError("periods 변수를 지정할 수 없습니다.")
        else:
            origin = pd.date_range(start=start
                                   , end=end
                                   , periods=periods
                                   , freq='BMS')
            return [_after_date_setting(i) for i in origin]

