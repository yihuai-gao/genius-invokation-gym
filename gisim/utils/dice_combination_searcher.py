from collections import Counter
from typing import Optional, Union

from devtools import debug

from gisim.classes.enums import ElementType


class DiceCombinationSearcher:
    def __init__(
        self,
        current_character_element: ElementType,
        all_character_elements: Union[list[ElementType], set[ElementType]],
    ) -> None:
        self.best_score = 0
        self.best_combination: Optional[Counter[ElementType]] = None

        if isinstance(all_character_elements, list):
            all_character_elements = set(all_character_elements)

        # 计算分数函数
        scores = {
            ElementType.OMNI: 10000,
            current_character_element: 1000,
        }

        for idx, i in enumerate(
            sorted(all_character_elements - {current_character_element})
        ):
            scores[i] = 100 + idx

        all_basic_elements = ElementType.get_basic_elements()
        for idx, i in enumerate(sorted(all_basic_elements - all_character_elements)):
            scores[i] = 10 + idx

        self.scores = scores

    def reset(self):
        self.best_score = 0
        self.best_combination = None

    def score(self, dices: Counter[ElementType]) -> int:
        return sum(dices[i] * self.scores[i] for i in dices)

    def _dfs_with_backtrace(
        self,
        existing: Counter[ElementType],
        required: Counter[ElementType],
    ):
        # 剪枝, 因为每一步分数都只会降低
        score = self.score(existing)
        if score <= self.best_score:
            return

        if all(v == 0 for v in required.values()):
            # 找到了一个更好的组合
            if score > self.best_score:
                self.best_score = score
                self.best_combination = existing.copy()
            return

        if required[ElementType.SAME] > 0:
            # 如果需要处理同种元素
            count = required[ElementType.SAME]
            for existing_element in list(existing):
                if existing[existing_element] > count:
                    existing[existing_element] -= count
                    required[ElementType.SAME] = 0
                    self._dfs_with_backtrace(existing, required)
                    # Backtrace
                    existing[existing_element] += count
                    required[ElementType.SAME] = count

        if required[ElementType.ANY] > 0:
            # Try to use any element
            for existing_element in list(existing):
                if existing[existing_element] > 0:
                    existing[existing_element] -= 1
                    required[ElementType.ANY] -= 1
                    self._dfs_with_backtrace(existing, required)
                    # Backtrace
                    existing[existing_element] += 1
                    required[ElementType.ANY] += 1

        for required_element in list(required):
            # 其实是不需要的
            if required[required_element] == 0:
                continue

            # 正确元素
            if existing[required_element] >= required[required_element]:
                # Try to use this element
                existing[required_element] -= required[required_element]
                required[required_element] = 0
                self._dfs_with_backtrace(existing, required)
                # Backtrace
                existing[required_element] += required[required_element]
                required[required_element] = 0

            # 万能元素
            if existing[ElementType.OMNI] >= required[required_element]:
                # Try to use omni element
                existing[ElementType.OMNI] -= required[required_element]
                required[required_element] = 0
                self._dfs_with_backtrace(existing, required)
                # Backtrace
                existing[ElementType.OMNI] += required[required_element]
                required[required_element] = 0

    def search(
        self,
        existing: Counter[ElementType],
        required: Counter[ElementType],
    ):
        self.reset()

        # 保证 existing 中只包含基础元素和万能元素
        _available_existing = ElementType.get_basic_elements() | {ElementType.OMNI}
        assert all(k in _available_existing for k, v in existing.items() if v > 0)

        # 保证 required 中只包含基础元素和相同元素
        _available_required = ElementType.get_basic_elements() | {
            ElementType.ANY,
            ElementType.SAME,
        }
        assert all(k in _available_required for k, v in required.items() if v > 0)

        self._dfs_with_backtrace(existing, required)

        if self.best_combination is None:
            return None

        return self.best_combination


if __name__ == "__main__":
    # searcher = DiceCombinationSearcher(
    #     ElementType.CRYO, {ElementType.CRYO, ElementType.PYRO}
    # )

    # exisitng_dices = Counter({ElementType.OMNI: 3, ElementType.CRYO: 2, ElementType.PYRO: 1, ElementType.HYDRO: 1, ElementType.GEO: 1})
    # required_dices = Counter({ElementType.ANY: 1})

    # exisitng_dices = searcher.search(exisitng_dices, required_dices)
    # debug(exisitng_dices)

    # required_dices = Counter({ElementType.PYRO: 1, ElementType.ANY: 2})
    # exisitng_dices = searcher.search(exisitng_dices, required_dices)
    # debug(exisitng_dices)

    # required_dices = Counter({ElementType.PYRO: 1, ElementType.ANY: 2})
    # exisitng_dices = searcher.search(exisitng_dices, required_dices)
    # debug(exisitng_dices)

    searcher = DiceCombinationSearcher(
        ElementType.HYDRO, {ElementType.HYDRO, ElementType.GEO, ElementType.ELECTRO}
    )

    exisitng_dices = Counter(
        {ElementType.HYDRO: 4, ElementType.GEO: 1, ElementType.ANEMO: 1}
    )
    required_dices = Counter({ElementType.HYDRO: 1, ElementType.SAME: 2})

    debug(searcher.search(exisitng_dices, required_dices))
