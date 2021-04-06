from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This action was taken because the Investigator wanted to compare some previously obtained results but was unable to identify a method to do so.
fi: Tämä tehtiin koska järjestelmä halusi vertailla aiemmin löydettyjä tuloksia, mutta ei löytänyt sopivaa vertailumetodia.
de: Diese Aktion wurde gemacht, weil der Investigator mit vorherigen Resultaten vergleichen wollte, aber dafür keine Methode identifizieren konnte
| name = nothing_to_compare
"""  # noqa: E501


class NothingToCompareResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "nothing-to-compare":
            return []

        return [Message(Fact("reason", "nothing_to_compare", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
