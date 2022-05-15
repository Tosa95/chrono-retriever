import re
from abc import abstractmethod, ABC
from typing import List

from src.chrono.model.window_info import WindowInfo, BrowserWindowInfo, IdeWindowInfo


class BaseWindowSpecializer(ABC):

    @abstractmethod
    def applies_to(self, window_info: WindowInfo) -> bool:
        ...

    @abstractmethod
    def specialize(self, window_info: WindowInfo) -> WindowInfo:
        ...


class CompoundWindowSpecializer(BaseWindowSpecializer):

    def __init__(self, specializers: List[BaseWindowSpecializer]):
        self._specializers = specializers

    def applies_to(self, window_info: WindowInfo) -> bool:
        return any(s.applies_to(window_info) for s in self._specializers)

    def specialize(self, window_info: WindowInfo) -> WindowInfo:
        for specializer in self._specializers:
            if specializer.applies_to(window_info):
                window_info = specializer.specialize(window_info)
        return window_info


class ChromeWindowSpecializer(BaseWindowSpecializer):

    def __init__(self, separator: str = "___"):
        self._separator = separator

    def applies_to(self, window_info: WindowInfo) -> bool:
        return "chrome" in window_info.process_name.lower()

    def specialize(self, window_info: WindowInfo) -> WindowInfo:
        pattern = f"{self._separator}(.*){self._separator}"
        url = re.search(pattern, window_info.name)
        if url is not None:
            data = window_info.dict()
            del data["type_"]
            return BrowserWindowInfo(**data, url=url.groups()[0])
        else:
            return window_info


class IdeaWindowSpecializer(BaseWindowSpecializer):

    def __init__(self, separator: str = "–"):
        self._separator = separator

    def applies_to(self, window_info: WindowInfo) -> bool:
        return "idea" in window_info.process_name.lower() or "pycharm" in window_info.process_name.lower()

    def specialize(self, window_info: WindowInfo) -> WindowInfo:
        name_split = window_info.name.split(self._separator)

        if len(name_split) == 2:
            data = window_info.dict()
            del data["type_"]
            return IdeWindowInfo(**data, project=name_split[0].strip(), file=name_split[1].strip())
        else:
            return window_info


ALL_SPECIALIZERS = CompoundWindowSpecializer([
    ChromeWindowSpecializer(),
    IdeaWindowSpecializer()
])

if __name__ == "__main__":
    pattern = f"aaa(.*)aaa"
    name = " aaastackoverflow.comaaa"
    url = re.search(pattern, name)

    print(url.groups()[0])
