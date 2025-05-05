import pandas as pd
from typing import List, Optional, Dict, Any, Callable, Union
from .string_splitter import StringSplitter

class HeadersNotFoundException(Exception):
    pass

class ParsingException(Exception):
    def __init__(self, failed_at, type_):
        super().__init__(f'Error: "{failed_at}" is not a valid {type_}. Check the format of the csv file')
        self.failed_at = failed_at
        self.type_ = type_

class DataNotRectangularException(Exception):
    def __init__(self, error_line=None, expecting=None, found=None):
        if error_line is None:
            super().__init__('Data not in rectangular form')
        else:
            super().__init__(f'Error:  Expecting {expecting} lines, found {found} lines, in line "{error_line}"')
        self.error_line = error_line
        self.expecting = expecting

class CSVReader:
    def __init__(self, filepath_or_buffer: Union[str, Any], contains_column_headers: bool = True, encoding: Optional[str] = None, splitter: Optional[StringSplitter] = None):
        self.splitter = splitter or StringSplitter(',', '"', True)
        self._headers: Optional[List[str]] = None
        self._data: Optional[pd.DataFrame] = None
        self._column_cache: Dict[int, List[str]] = {}
        self._read(filepath_or_buffer, contains_column_headers, encoding)

    def _read(self, filepath_or_buffer, contains_column_headers, encoding):
        # pandas로 읽고, splitter로 헤더/데이터 분리
        if encoding:
            with open(filepath_or_buffer, encoding=encoding) as f:
                lines = f.readlines()
        else:
            if hasattr(filepath_or_buffer, 'read'):
                lines = filepath_or_buffer.read().splitlines()
            else:
                with open(filepath_or_buffer, encoding='utf-8') as f:
                    lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines if line.strip() != '']
        if contains_column_headers:
            self._headers = self.splitter.split(lines[0], False)
            data_lines = lines[1:]
        else:
            self._headers = [str(i) for i in range(len(self.splitter.split(lines[0], False)))]
            data_lines = lines
        data = [self.splitter.split(line, False) for line in data_lines]
        # 데이터가 직사각형인지 확인
        expected = len(self._headers)
        for row in data:
            if len(row) != expected:
                raise DataNotRectangularException(','.join(row), expected, len(row))
        self._data = pd.DataFrame(data, columns=self._headers)

    @property
    def headers(self) -> List[str]:
        return self._headers

    @property
    def row_count(self) -> int:
        return len(self._data)

    def __getitem__(self, key: Union[int, str]) -> List[str]:
        if isinstance(key, int):
            col = self._data.iloc[:, key]
            return col.tolist()
        elif isinstance(key, str):
            if key not in self._headers:
                raise Exception(f'{key} not found in collection')
            return self._data[key].tolist()
        else:
            raise KeyError(key)

    def get_double_list(self, column: Union[int, str]) -> List[float]:
        col = self[column]
        result = []
        for v in col:
            try:
                if v == '' or v is None:
                    result.append(float('nan'))
                else:
                    result.append(float(v))
            except Exception:
                raise ParsingException(v, float)
        return result

    def get_int_list(self, column: Union[int, str]) -> List[int]:
        col = self[column]
        result = []
        for v in col:
            try:
                result.append(int(v))
            except Exception:
                raise ParsingException(v, int)
        return result

    def get_datetime_list(self, column: Union[int, str]) -> List[pd.Timestamp]:
        col = self[column]
        result = []
        for v in col:
            try:
                result.append(pd.to_datetime(v))
            except Exception:
                raise ParsingException(v, 'datetime')
        return result

    def get_custom_type_list(self, parser: Callable[[str], Any], column: Union[int, str]) -> List[Any]:
        col = self[column]
        return [parser(v) for v in col] 