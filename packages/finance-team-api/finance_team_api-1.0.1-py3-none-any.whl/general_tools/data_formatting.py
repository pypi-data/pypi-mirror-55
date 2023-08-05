import numpy as np
import pandas as pd
from error_handler.type_tool import *
import time

# 2차원 시계열 데이터(Pandas or ndArray)를 3차원 ndArray로 변환하는 Tool
def convert_frame_to_numpy(data, seq_len, timestep, use_columns=None):
    """
    :param data: TimeSeries DataFrame or ndArray, 자료형 변환을 하려는 TimeSeries Data(Price, Vol, Return,....)
    :param seq_len: int, 하나의 Array에 포함될 Time Step
    :param timestep: int, Array를 나눌 step
                    : 만일 seq_len = 10, timestep=1 이라면 10일의 2d_array를 1일 간격으로 쌓는다.
    :param use_columns: list(If not None), 목적 Column
    :return: batch_set(numpy array), time_batch_set(numpy array)

    전체 데이터에 대해 일정한 Sequence로 연산을 하고자 하는 경우 Vectorize지원을 위해
    기존 DataFrame형태를 Numpy로 변환.
    """

    # 오류 검사
    # input data는 DataFrame혹은 Series 이어야 합니다.
    input_data_type = data.__class__
    pandas_available_type = [pd.DataFrame([]).__class__]
    series_available_type = [pd.Series([]).__class__]
    numpy_available_type = [np.array([]).__class__]
    if input_data_type not in pandas_available_type + series_available_type + numpy_available_type:
        raise InputDataSettingError('지원하지 않는 Input Data형식 입니다. 지원 형식 : DataFrame, Series, ndArray')

    # set_mode variable setting
    # Input Data 자료형에 따른 mode 설정
    if input_data_type in pandas_available_type:
        set_mode = 'DataFrame'
    if input_data_type in series_available_type:
        set_mode = 'Series'
    elif input_data_type in numpy_available_type:
        set_mode = 'Numpy'

    # 오류 검사
    # seq_len은 int type이어야 합니다.
    if seq_len.__class__ != int:
        raise VariableSettingError('seq_len 변수는 Int이어야 합니다.')

    # 오류 검사
    # timestep은 int type이어야 합니다.
    if timestep.__class__ != int:
        raise VariableSettingError('timestep 변수는 Int이어야 합니다.')

    # 오류 검사
    # use_columns를 설정할 경우 dataframe의 column안에 존재해야 함.
    if (use_columns is not None) & (set_mode=='DataFrame'):
        for usable_columns in use_columns:
            if usable_columns not in data.columns:
                raise VariableSettingError('{}의 데이터가 존재하지 않습니다.'.format(usable_columns))

        # use_columns정의된 경우 해당 자산들 데이터만 설정
        dataframe = data[use_columns]


    # batch size 결정
    if set_mode == 'DataFrame':
        row_num, col_num =  len(data), len(data.columns)
    elif set_mode =='Series':
        row_num, col_num = len(data), 1
    elif set_mode == 'Numpy':
        (row_num, col_num) = data.shape
    num_of_batch = int((row_num - seq_len) / timestep + 1)

    # array 미리 선정
    reformat_value_array = np.zeros((num_of_batch, seq_len, col_num))
    reformat_index_array = np.zeros((num_of_batch, seq_len)).astype(int)
    forward_constant = 0

    if set_mode == 'DataFrame':
        indexer = np.array(range(len(data.index)))
        data = np.array(data, dtype=float)
    elif set_mode == 'Series':
        indexer = np.array(range(len(data.index)))
        data = np.array(data, dtype=float).reshape(-1, 1)


    # 3차원 Array로 dataframe 변형
    for batch_num in range(num_of_batch):
        if batch_num == 0:
            reformat_value_array[batch_num, :, :] = data[forward_constant: seq_len]
            if set_mode == 'DataFrame' or set_mode == 'Series':
                reformat_index_array[batch_num, :] = indexer[forward_constant: seq_len]
        else:
            reformat_value_array[batch_num, :, :] = data[forward_constant: seq_len + (batch_num * timestep)]
            if set_mode == 'DataFrame' or set_mode == 'Series':
                reformat_index_array[batch_num, :] = indexer[forward_constant: seq_len + (batch_num * timestep)]

        forward_constant += timestep
    return reformat_value_array, reformat_index_array

# 2차원 시계열 데이터(ndArray)를 3차원 ndArray로 변환하는 Tool
def convert_numpy_to_numpy(array, seq_len, timestep,):
    # 오류 검사
    # input data는 DataFrame혹은 Series 이어야 합니다.
    if array.__class__ not in [np.array([]).__class__, pd.Series([]).__class__]:
        raise DataFrameSettingError('Input Data의 형식이 ndArray이어야 합니다.')

    # 오류 검사
    # seq_len은 int type이어야 합니다.
    if seq_len.__class__ != int:
        raise VariableSettingError('seq_len 변수는 Int이어야 합니다.')

    # 오류 검사
    # timestep은 int type이어야 합니다.
    if timestep.__class__ != int:
        raise VariableSettingError('timestep 변수는 Int이어야 합니다.')


class data_format_check:
    def __init__(self, data):
        self.data = data         # Check 하고자 하는 data
        self.need_convert = None # 데이터 타입 변환 필요 여부

    # numpy array일 경우 3차원 행렬인지 Check
    def array_shape_check(self, data):
        """
        가격 데이터 및 수익률 데이터의 분석은 시간 효율성을 위해 3차원을 지원하며
        앞으로 이는 필요 여부에 따라 업데이트 될 수 있음.
        :param data: ndArray
        """
        try:
            shape_test = data[0,0,0]
        except IndexError as e:
            ArraySettingError("Input Data는 3차원 Array이어야 합니다."
                              "만일 2차원 Array를 반드시 사용해야 한다면 reshape(-1, rows, columns)를 이용하세요.")

    # Input Data의 자료형을 Check하며 DataFrame, Series 혹은 2차원 Array일 경우 변환 필요
    def check_type(self):
        data_frame_check = self.data.__class__ == pd.DataFrame([]).__class__
        series_check = self.data.__class__ == pd.Series([]).__class__
        numpy_check = self.data.__class__ == np.array([]).__class__
        if data_frame_check ==  True:
            self.need_convert = True
        elif series_check == True:
            self.need_convert = True
        elif numpy_check == True:
            self.array_shape_check(self.data)
            self.need_convert = False
        return self.need_convert
