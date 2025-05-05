from typing import List, Union

class StringSplitter:
    def __init__(self, splitters: Union[str, List[str]], quote: str, trim: bool = False):
        if isinstance(splitters, str):
            self._splitters = [splitters]
        else:
            self._splitters = splitters
        self._quote = quote
        self._trim = trim

    def split(self, string_to_split: str, ignore_empty: bool) -> List[str]:
        position = -1
        first_string = None
        at_end = False
        s = string_to_split.strip() if self._trim else string_to_split
        if s.startswith(self._quote):
            for splitter in self._splitters:
                splitter_pos = s.find(self._quote + splitter, 1)
                if splitter_pos > -1 and (position == -1 or splitter_pos < position):
                    position = splitter_pos
            if position == -1:
                at_end = True
                first_string = s[1:-1]
            else:
                first_string = s[1:position]
                position += 1
        else:
            for splitter in self._splitters:
                splitter_pos = s.find(splitter)
                if splitter_pos > -1 and (position == -1 or splitter_pos < position):
                    position = splitter_pos
            if position == -1:
                at_end = True
                first_string = s
            else:
                first_string = s[:position]
            if self._trim:
                first_string = first_string.strip()
        result = []
        if not (ignore_empty and first_string == ""):
            result.append(first_string)
        if not at_end:
            second_string = s[position + 1:]
            result.extend(self.split(second_string, ignore_empty))
        return result 