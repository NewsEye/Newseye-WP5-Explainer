import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: A short summary of the documents was created.
fi: Dokumenteistä tehtiin lyhyt tiivistelmä.
de: Eine kurze Zusammenfassung der Dokumente wurde erzeugt.
fr: Un bref résumé des documents a été créé.
| name = Summarization
"""


class SummarizationResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "Summarization":
            return []

        return [Message(Fact("task", "Summarization", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
