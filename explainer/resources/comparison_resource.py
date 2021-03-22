import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: Two corpora were compared based on {parameters}
| name = Comparison
"""


class ComparisonResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "ExtractBigrams":
            return []

        return [
            Message(
                Fact(
                    "task",
                    "Comparison",
                    "[Comparison:Task:{}]".format(task.parameters.get("facet", "unknown")),
                    event.id,
                )
            )
        ]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [ComparisonFacetRealizer]


class ComparisonFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "ANY", r"\[Comparison:Task:([^\]]+)\]", [1], "the facet '{}'",
        )
