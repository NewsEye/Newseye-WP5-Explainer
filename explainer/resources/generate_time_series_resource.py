import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")


TEMPLATE = """
en: A time series of the {parameters} was created.
| name = GenerateTimeSeries
"""


class GenerateTimeSeriesResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "GenerateTimeSeries":
            return []

        if "facet_name" in task.parameters:
            split_by = "[TimeSeries:FACET:{}]".format(task.parameters.get("facet_name"))
        else:
            split_by = "[TimeSeries:NO_FACET]"

        return [Message(Fact("task", "GenerateTimeSeries", split_by, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [EnglishTimeSeriesFacetRealizer, EnglishTimeSeriesNoFacetRealizer]


class EnglishTimeSeriesFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[TimeSeries:FACET:(.*)\]", (1), "'{}' facet values",
        )


class EnglishTimeSeriesNoFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[TimeSeries:NO_FACET\]", (), "data",
        )
