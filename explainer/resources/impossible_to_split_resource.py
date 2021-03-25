from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: The investigator tried to split data in meaningful way, but failed.
fi: Aineistoa yritettiin jakaa useaan alijoukkoon, mutta mielekästä jakoa ei löydetty.
| name = impossible_to_split
"""  # noqa: E501


class ImpossibleToSplitResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "impossible to split":
            return []

        return [Message(Fact("reason", "impossible_to_split", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
