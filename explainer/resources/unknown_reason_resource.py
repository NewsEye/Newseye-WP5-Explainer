from typing import List, Type

from explainer.core.models import Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This was completed for a reason called {name} with the paramaters {parameters}. This reason is not familiar to the Explainer and should be reported.
| name = UNKNOWN_REASON:.*
"""  # noqa: E501


class UnknownReasonResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        return []

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [UnknownReasonNameRealizer]


class UnknownReasonNameRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"UNKNOWN_REASON:(.*)", (1), "'{}'",
        )
