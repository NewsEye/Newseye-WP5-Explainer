from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This action was taken because the original collection was too large to analyze in meaningful time.
fi: Tämä tehtiin koska alkuperäinen kokoelma oli liian suuri analysoitavaksi mielekkäässä ajassa.
de: Diese Aktion wurde gemacht, weil die originale Kollektion zu groß zum Analysieren in sinnvoller Zeit war.
fr: Cette action a été entreprise car la collection d'origine était trop volumineuse pour être analysée dans un temps raisonnable.
| name = too_big_collection
"""  # noqa: E501


class TooBigCollectionResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "too_big_collection":
            return []

        return [Message(Fact("reason", "too_big_collection", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
