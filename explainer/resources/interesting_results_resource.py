from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This step was taken because the preceding step found highly interesting results which the Investigator wants to expand upon.
fi: Tämä tehtiin koska järjestelmä halusi jatkaa aiemmin löydetyn erittäin kiinnostavan tuloksen tutkimista.
de: Dieser Schritt wurde gemacht, weil der vorhergehende Schritt sehr interessante Resultate gefunden hat, die der Investigator erweitern möchte.
fr: Cette étape a été entreprise car l'étape précédente a trouvé des résultats très intéressants que l'enquêteur souhaite développer.
| name = interesting_results
"""  # noqa: E501


class InterestingResultsResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "interesting results":
            return []

        return [Message(Fact("reason", "interesting_results", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
