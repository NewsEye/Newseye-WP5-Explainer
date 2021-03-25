import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: The dataset was split by different values of the {parameters} facets.
fi: Kokoelma jaettiin osiin {parameters} arvojen pohjalta.
| name = SplitByFacet
"""


class SplitByFacetResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "SplitByFacet":
            return []

        return [
            Message(
                Fact("task", "SplitByFacet", "[SplitByFacet:FACET:{}]".format(task.parameters.get("facet")), event.id)
            )
        ]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [SplitByFacetFacetRealizer]


class SplitByFacetFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "ANY", r"\[SplitByFacet:FACET:(.*)\]", (1), "'{}'",
        )
