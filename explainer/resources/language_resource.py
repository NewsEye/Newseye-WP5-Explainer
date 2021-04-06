from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: The collection is in specific language, which limits tool applicability (e.g. topic modeling might not be available for all languages).
fi: Tämä tehtiin koska tutkittavan kokoelman kieli rajoittaa käytettävissä olevia työkaluja (esim. aihemallinnus ei ole käytettävissä kaikille kielille).
de: Die Kollektion ist in einer speziellen Sprache, was die Anwendbarkeit der Werkzeuge einschränkt (z.B. könnte  das Topic-Modelling nicht für alle Sprachen verfügbar sein).
| name = language
"""  # noqa: E501


class LanguageResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "language":
            return []

        return [Message(Fact("reason", "language", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
