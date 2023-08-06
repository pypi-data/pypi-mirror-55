import pandas as pd

def monthly_adjust(date
                   , coin_market=None):
    # 주말 포함한 경우 : 암호화폐시장
    if coin_market is not None:
        end = pd.date_range(start=date
                            , periods=1
                            , freq='M')[0]

        if date == end:
            return 1
        else:
            date_from_end = pd.date_range(start=date
                                          , end=end)
            len_from_end = len(date_from_end)
            return len_from_end

    # 주말을 포함하지 않는 경우 : 증권시장
    else:
        end = pd.date_range(start=date
                            , periods=1
                            , freq='BM')[0]

        if date == end:
            return 1
        else:
            date_from_end = pd.date_range(start=date
                                          , end=end
                                          , freq='B')
            len_from_end = len(date_from_end)
            return len_from_end
