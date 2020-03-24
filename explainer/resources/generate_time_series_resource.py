import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")


TEMPLATE = """
en: A time series was created from {parameters}.
| name = GenerateTimeSeries
"""


class GenerateTimeSeriesResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "GenerateTimeSeries":
            return []

        return [
            Message(
                Fact(
                    "task", "GenerateTimeSeries", "[TimeSeries:FACET:{}]".format(task.parameters.get("facet")), event.id
                )
            )
        ]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [EnglishTimeSeriesRealizer]


class EnglishTimeSeriesRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry,
            "en",
            r"\[ACTION:GenerateTimeSeries\]",
            [],
            "a time series was generated from the output of the previous step",
        )
