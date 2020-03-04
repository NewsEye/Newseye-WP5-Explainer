import logging
from typing import List, Type

from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.resources.generic_explainer_resource import GenericExplainerResource

log = logging.getLogger("root")


class ExtractFacetsResource(GenericExplainerResource):
    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [EnglishExtractFacetsRealizer]


class EnglishExtractFacetsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry,
            "en",
            r"\[ACTION:ExtractFacets\]",
            [],
            "the publication years, newspapers and languages of the documents were extracted",
        )
