import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: The most promising timespan was identified from a timeseries.
fi: Aikasarjasta etsittiin lupaavin aikajänne.
de: Der vielversprechendste Zeitraum einer Zeitreihe wurde identifiziert.
| name = FindBestSplitFromTimeseries
"""


class FindBestSplitFromTimeseriesResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "FindBestSplitFromTimeseries":
            return []

        return [Message(Fact("task", "FindBestSplitFromTimeseries", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
