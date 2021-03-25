from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This action was taken because the original collection was too small for meaningful analysis.
fi: Tämä tehtiin koska alkuperäinen kokoelma oli liian pieni mielekkään analyysin tekemiseen.
| name = not_enough_data
"""  # noqa: E501


class NotEnoughDataResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "not enough data":
            return []

        return [Message(Fact("reason", "not_enough_data", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
