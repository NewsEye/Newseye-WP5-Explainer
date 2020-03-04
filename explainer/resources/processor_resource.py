from abc import ABC, abstractmethod
from typing import List, Type

from explainer.core.realize_slots import SlotRealizerComponent


class ProcessorResource(ABC):

    EPSILON = 0.00000001

    @abstractmethod
    def templates_string(self) -> str:
        pass

    @abstractmethod
    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        pass
