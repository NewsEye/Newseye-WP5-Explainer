from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This was done as part of initializing a new experiment.
fi: Tämä tehtiin osana uuden koeasetelman alustusta.
| name = initialization
"""


class InitializationResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "initialization":
            return []

        return [Message(Fact("reason", "initialization", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
