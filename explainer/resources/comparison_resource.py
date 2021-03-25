import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: Two corpora were compared based on {parameters} .
fi: Kahta kokoelmaa verrattiin {parameters} osalta.
| name = Comparison
"""


class ComparisonResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "ExtractBigrams":
            return []

        if task.parameters.get("facet"):
            params = ("[Comparison:Task:Facet:{}]".format(task.parameters["facet"]),)
        else:
            params = ("[Comparison:Task:UNKNOWN",)

        return [Message(Fact("task", "Comparison", params, event.id,))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [
            EnglishComparisonFacetRealizer,
            EnglishComparisonUknownFacetRealizer,
            #
            FinnishComparisonFacetRealizer,
            FinnishComparisonUknownFacetRealizer,
        ]


class EnglishComparisonFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[Comparison:Task:Facet:([^\]]+)\]", [0], "the facet '{}'",
        )


class EnglishComparisonUknownFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[Comparison:Task:Unknown]", [], "a facet unfamiliar to the Explainer",
        )


class FinnishComparisonFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "fi", r"\[Comparison:Task:Facet:([^\]]+)\]", [0], "'{}' arvon",
        )


class FinnishComparisonUknownFacetRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "fi", r"\[Comparison:Task:Unknown]", [], "jonkin tuntemattoman arvon",
        )
