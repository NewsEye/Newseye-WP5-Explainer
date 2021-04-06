from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This step was taken because the Investigator had previously built a new collection of documents and wants to begin analyzing it.
fi: Tämä tehtiin koska järjestelmä halusi tutkia tarkemmin aiemmin rakentamaansa uutta kokoelmaa.
de: Dieser Schritt wurde gemacht, weil der Investigator vorher schon eine neue Kollektion von Dokumenten gebaut hat und beginnen möchte sie zu analysieren.
| name = new_collection
"""  # noqa: E501


class NewCollectionResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "new collection":
            return []

        return [Message(Fact("reason", "new_collection", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
