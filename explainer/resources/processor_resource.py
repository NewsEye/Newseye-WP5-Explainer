from abc import ABC, abstractmethod
from typing import List, Type

from explainer.core.models import Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event


class ProcessorResource(ABC):

    EPSILON = 0.00000001

    @abstractmethod
    def templates_string(self) -> str:
        pass

    @abstractmethod
    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        pass


class TaskResource(ProcessorResource):
    @abstractmethod
    def parse_task(self, event: Event) -> List[Message]:
        pass


class ReasonResource(ProcessorResource):
    @abstractmethod
    def parse_reason(self, event: Event) -> List[Message]:
        pass
