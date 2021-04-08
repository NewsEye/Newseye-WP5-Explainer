from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This action was taken because the original collection was relatively small, limiting the available analyses that could provide meaningful results.
fi: Tämä tehtiin koska alkuperäinen kokoelma oli suhteellisen pieni, mikä rajoittaa käytettävissä olevia analyysityökaluja.
de: Diese Aktion wurde gemacht, weil die originale Kollektion relativ klein war, was die verfügbaren Analysen einschränkt, die sinnvolle Resultate liefern könnten.
fr: Cette mesure a été entreprise car la collection originale était relativement petite, limitant les analyses disponibles pouvant fournir des résultats significatifs.
| name = small_collection
"""  # noqa: E501


class SmallCollectionResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "small_collection":
            return []

        return [Message(Fact("reason", "small_collection", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
