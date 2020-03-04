from typing import List, Type

from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.resources.processor_resource import ProcessorResource

TEMPLATE = """
en: {action} {reason}
| action = .*
"""


class GenericExplainerResource(ProcessorResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [EnglishBruteForceRealizer]


class EnglishBruteForceRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[REASON:BruteForce\]", [], "as one of the steps always conducted when possible"
        )
