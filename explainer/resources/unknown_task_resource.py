from typing import List, Type

from explainer.core.models import Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: A task called {name} was completed with the paramaters {parameters}. This task is not familiar to the Explainer and should be reporter.
| name = UNKNOWN_TASK:.*
"""  # noqa: E501


class UnknownTaskResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        return []

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [UnknownTaskNameRealizer]


class UnknownTaskNameRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"UNKNOWN_TASK:(.*)", (1), "'{}'",
        )
