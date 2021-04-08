import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")


TEMPLATE = """
en: A topic model was used to compare corpora.
fi: Korpuksia vertailtiin aihemallin avulla.
de: Ein Topic-Modell wurde verwendet, um die Korpora zu vergleichen.
fr: Un modèle thématique a été utilisé pour comparer les corpus.
| name = TopicModelDocsetComparison
"""


class TopicModelDocumentSetComparisonResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "TopicModelDocsetComparison":
            return []

        return [Message(Fact("task", "TopicModelDocsetComparison", None, event.id,))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
