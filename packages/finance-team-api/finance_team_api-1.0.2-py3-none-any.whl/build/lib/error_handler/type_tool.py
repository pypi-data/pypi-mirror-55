import pandas as pd


class DataFrameSettingError(Exception):
    def __init__(self, *args, **kwargs):
        pass

class VariableSettingError(Exception):
    def __init__(self, *args, **kwargs):
        pass

class ArraySettingError(Exception):
    def __init__(self, *args, **kwargs):
        pass

class InputDataSettingError(Exception):
    def __init__(self, *args, **kwargs):
        pass