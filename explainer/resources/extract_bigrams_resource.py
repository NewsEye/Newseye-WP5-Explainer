import logging
from typing import List, Type

from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.resources.generic_explainer_resource import GenericExplainerResource

log = logging.getLogger("root")


class ExtractBigramsResource(GenericExplainerResource):
    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [EnglishExtractBigramStemsRealizer, EnglishExtractBigramsTokenRealizer]


class EnglishExtractBigramStemsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry,
            "en",
            r"\[ACTION:ExtractBigrams:stems\]",
            [],
            "all pairs of subsequent stems were extracted and counted",
        )


class EnglishExtractBigramsTokenRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry,
            "en",
            r"\[ACTION:ExtractBigrams:tokens\]",
            [],
            "all pairs of subsequent tokens were extracted and counted",
        )
