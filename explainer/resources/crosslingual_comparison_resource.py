from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This step was taken to compare datasets that are of different languages, thus limiting the available options.
fi: Tämä tehtiin koska haluttiin verrata kahta eri kielistä aineistoa, mikä rajoittaa käytettävissä olevia analyysityökaluja.
de: Dieser Schritt wurde unternommen zum Vergleich von Datensätzen, die in verschiedenen Sprachen vorliegen, was die verfügbaren Optionen eingrenzt.
fr: Cette étape a été entreprise pour comparer des ensembles de données de langues différentes, limitant ainsi les options disponibles.
| name = crosslingual_comparison
"""  # noqa: E501


class CrosslingualcomparisonResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "crosslingual comparison":
            return []

        return [Message(Fact("reason", "crosslingual_comparison", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
