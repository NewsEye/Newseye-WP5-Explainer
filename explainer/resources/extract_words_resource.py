import logging
from typing import List, Type

from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.resources.generic_explainer_resource import GenericExplainerResource

log = logging.getLogger("root")


class ExtractWordsResource(GenericExplainerResource):
    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [EnglishExtractWordStemsRealizer, EnglishExtractWordTokenRealizer]


class EnglishExtractWordStemsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry,
            "en",
            r"\[ACTION:ExtractWords:stems\]",
            [],
            "The stems of all the words were extracted and counted",
        )


class EnglishExtractWordTokenRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(registry, "en", r"\[ACTION:ExtractWords:tokens\]", [], "All tokens were extracted and counted")
