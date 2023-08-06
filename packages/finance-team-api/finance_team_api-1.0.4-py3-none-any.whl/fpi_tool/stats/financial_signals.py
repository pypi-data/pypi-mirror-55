import numpy as np
from ..general_tools.data_formatting import convert_frame_to_numpy, data_format_check

class momentum_signals:
    def __init__(self
                 , price_data
                 , seq_len
                 , timestep
                 , use_columns=None):
        self.price_data = price_data
        self.seq_len = seq_len
        self.timestep = timestep
        self.use_columns = use_columns

        # Input Data가 DataFrame형식일 경우 계산하고자 하는 자산명 지정 가능
        if self.use_columns is not None:
            self.price_data = self.price_data[use_columns]

        # Input_data가 형태 변환이 필요한지 Check할 수 있음
        self.input_data_type_check = data_format_check(self.price_data).check_type()


        self.price_data[self.price_data == 0] = np.nan

    # 일반적인 수익률 측정 방식
    def periodic_return(self
                        , method='hpr'):
        """
        Default는 HPR(Holding Period Return)

        Annualized HPR = (기말가치 / 기초가치) ** (1 / Annualize_constant) - 1
        Geometric Return = product(1 + HPR(i)) ** (1 / Annualize_constant) - 1
        Average Return = summation(HPR(i)) / num_of_period * Annualize_constant

        :param method: string, 'hpr', 'geometric', 'average'
        :return: ndArray
        """

        # 형태 변화가 필요한 DataFrame계열의 경우 형태 변환
        if self.input_data_type_check == True:
            self.convert_price_data, self.datetimeIndex = convert_frame_to_numpy(data=self.price_data
                                                                                 , seq_len=self.seq_len
                                                                                 , timestep=self.timestep
                                                                                 , use_columns=self.use_columns)
            self.convert_price_data[self.convert_price_data == 0] = np.nan

        constant = 253 / self.seq_len
        if method == 'hpr':
            hpr = (self.convert_price_data[:, -1, :]/self.convert_price_data[:, 0, :]) ** constant - 1
            return hpr, self.datetimeIndex[:, -1]

        elif method == 'geometric':
            simple_return = self.convert_price_data[:, 1:, :] / self.convert_price_data[:, :-1, :]
            cumprod = np.cumprod(simple_return, axis=1)
            geomtric_ret = (cumprod[:, -1, :]/cumprod[:, 0, :]) ** constant - 1
            return geomtric_ret\
                , self.datetimeIndex[:, -1]

        elif method == 'average':
            simple_return = self.convert_price_data[:, 1:, :]/self.convert_price_data[:, :-1, :] - 1
            average_ret = np.average(simple_return, axis=1) * constant
            return average_ret, self.datetimeIndex[:, -1]

    # 일반적인 변동성 측정방식
    def periodic_risk(self
                      , freq
                      , mode='std'
                      , ewma_lambda=0.94):
        """
        Default는 std(Standard Deviation)

        Standard Deviation = sqrt(Exp(X- X**2) - Exp(X) ** 2) * sqrt(Annualize_constant)
        Exponential Weighted Moving Avgerage : see docs https://www.investopedia.com/articles/07/ewma.asp
        Downside_Deviation : see docs https://www.investopedia.com/terms/d/downside-deviation.asp

        :param freq: int, freq기간 수익률(simple return) 설정 parameter
        :param mode: string, 'std', 'ewma_vol', 'downside_deviation'
        :param ewma_lambda: float if not None, 'ewma_vol'산출시 lambda값
        :return: ndArray
        """
        constant = 253 / freq

        if self.input_data_type_check == True:
            simple_return = self.price_data / self.price_data.shift(freq) - 1
            simple_return = simple_return.astype(float)
        else:
            array_price = np.array(self.price_data, dtype=float)
            simple_return = array_price[freq:, :] / array_price[:-freq, :] - 1

        # Standard Deviation
        if mode == 'std':
            batch_simple_return, datetime_index = convert_frame_to_numpy(data=simple_return
                                                                         , seq_len=self.seq_len
                                                                         , timestep=self.timestep)
            vol = np.std(batch_simple_return, axis=1) * np.sqrt(constant)
            return vol\
                , datetime_index[:, -1]

        # EWMA Volatility
        elif mode == 'ewma_vol':
            """
            see:
            https://www.investopedia.com/articles/07/ewma.asp
            """
            ewma_lambda_vector = np.ones(self.seq_len) * ewma_lambda
            ewma_lambda_vector_prod = (1-ewma_lambda) * np.cumprod(ewma_lambda_vector)
            ewma_lambda_vector_prod = ewma_lambda_vector_prod[::-1] / ewma_lambda
            ewma_lambda_vector_prod = ewma_lambda_vector_prod.reshape(-1
                                                                      , self.seq_len
                                                                      , 1)

            batch_simple_return, datetime_index = convert_frame_to_numpy(data=simple_return
                                                                         , seq_len=self.seq_len
                                                                         , timestep=self.timestep)

            squared_batch_simple_return = batch_simple_return ** 2

            element_wise_production = np.multiply(squared_batch_simple_return
                                                  , ewma_lambda_vector_prod)
            sumproduct_value = np.sum(element_wise_production, axis=1) * constant
            ewma_vol = np.sqrt(sumproduct_value)
            return ewma_vol\
                , datetime_index[:, -1]

        # Downside Deviation
        elif mode == 'downside_deviation':
            batch_simple_return, datetime_index = convert_frame_to_numpy(data=simple_return
                                                                         , seq_len=self.seq_len
                                                                         , timestep=self.timestep)
            downside_ret = batch_simple_return[batch_simple_return > 0] = 0
            squared_downside_ret = downside_ret ** 2

            downside_ret = np.nanmean(squared_downside_ret, axis=1)
            return downside_ret\
                , datetime_index[:, -1]