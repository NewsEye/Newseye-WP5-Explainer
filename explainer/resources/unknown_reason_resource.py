from typing import List, Type

from explainer.core.models import Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This was completed for a reason called {name} with the paramaters {parameters}. Please report how, where, and when you encountered this message by email to leo.leppanen@helsinki.fi.
fi: Tämä tehtiin tuntemattomasta syystä nimeltä {name} (parametreina {parameters} ). Autat järjestelmän kehitystyötä jos kerrot milloin ja missä yhteydessä törmäsit tähän viestiin sähköpostitse osoitteeseen leo.leppanen@helsinki.fi.
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
            registry, "ANY", r"UNKNOWN_REASON:(.*)", (1), "'{}'",
        )
