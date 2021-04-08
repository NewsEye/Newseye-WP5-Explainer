from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This is one of the steps taken always as part of a brute force search.
fi: Tämä vaihe suoritetaan aina osana raakaan voimaan perustuvaa hakua.
de: Dies ist einer der Schritte, die als Teil einer Brute-Force-Suche immer ausgeführt werden.
fr: C'est l'une des étapes toujours suivies dans le cadre d'une recherche par force brute.
| name = BruteForce
"""


class BruteForceResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "brute_force":
            return []

        return [Message(Fact("reason", "BruteForce", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
