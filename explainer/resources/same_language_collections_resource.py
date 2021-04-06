from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This action was taken because there were several datasets in the same language, so comparing them seemed relevant.
fi: Tämä tehtiin koska tutkittavina oli useita saman kielisiä aineistoja, jolloin niiden vertailu vaikuttaa mielekkäänä.
de: Diese Aktion wurde gemacht, weil es verschiedene Datensätze in derselben Sprache gibt, so dass ein Vergleich relevant erschien.
| name = same_language_collections
"""  # noqa: E501


class SameLanguageCollectionsResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "same language collections":
            return []

        return [Message(Fact("reason", "same_language_collections", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
