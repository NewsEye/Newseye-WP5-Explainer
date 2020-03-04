import logging
from typing import List, Type

from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.resources.generic_explainer_resource import GenericExplainerResource

log = logging.getLogger("root")


class GenerateTimeSeriesResource(GenericExplainerResource):
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
