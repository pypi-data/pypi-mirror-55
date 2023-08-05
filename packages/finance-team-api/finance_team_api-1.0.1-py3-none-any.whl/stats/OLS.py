import time
import pandas as pd
import numpy as np



def OLS(data, estimation_window):

    estimation_window_set = range(1300, len(data) - estimation_window, 1)

    collect = np.array([]).reshape(-1, estimation_window, 2)
    st_point = estimation_window
    # for i in range(100):
    for i in range(int(len(data)/10000)):
        end_point = st_point + estimation_window

        obj_data = data.iloc[st_point: end_point]
        obj_data = np.array(obj_data, dtype=np.float32).reshape(-1, estimation_window, 2)

        collect = np.concatenate((collect, obj_data), axis=0)
        print(collect.shape)

        st_point += 1
    n = len(collect)
    hedge = []

    st = time.time()
    for i in range(len(collect)):
        m_x, m_y = collect[i].mean(axis=0)
        ss_xy = np.prod(collect[i], axis=1).sum() - n * m_y * m_x
        x = []
        for j in range(len(collect[i])):
            x.append(collect[i][j][0])

        x = np.array(x)
        ss_xx = np.sum(x * x) - n * m_x * m_x

        hedge.append(ss_xy / ss_xx)
    hedge_df = pd.DataFrame(hedge, index = estimation_window_set)
    end = time.time() - st
    print(end)
    return hedge_df

if __name__ == '__main__':
    data = pd.read_csv('./LTC_ETH_dataset.csv', index_col=0)

    estimation_window = 1300

    hedge_list = OLS(data, estimation_window)
