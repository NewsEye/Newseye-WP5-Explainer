import logging
from typing import Dict, Optional

from uralicNLP import uralicApi

from reporter.core.models import Slot
from reporter.core.morphological_realizer import LanguageSpecificMorphologicalRealizer

log = logging.getLogger("root")


class EnglishUralicNLPMorphologicalRealizer(LanguageSpecificMorphologicalRealizer):
    def __init__(self):
        super().__init__("fi")

        self.case_map: Dict[str, str] = {"genitive": "GEN"}

    def realize(self, slot: Slot) -> str:
        case: Optional[str] = slot.attributes.get("case")
        if case is None:
            return slot.value

        log.debug("Realizing {} to Finnish")

        case = self.case_map.get(case.lower(), case.upper())
        log.debug("Normalized case {} to {}".format(slot.attributes.get("case"), case))

        possible_analyses = uralicApi.analyze(slot.value, "eng")
        log.debug("Identified {} possible analyses".format(len(possible_analyses)))
        if len(possible_analyses) == 0:
            log.warning(
                "No valid morphological analysis for {}, unable to realize despite case attribute".format(slot.value)
            )
            return slot.value

        analysis = possible_analyses[0][0]
        log.debug("Picked {} as the morphological analysis of {}".format(analysis, slot.value))

        analysis = analysis.replace("Nom", case)
        log.debug("Modified analysis to {}".format(analysis))

        modified_value = uralicApi.generate(analysis, "eng")[0][0]
        log.debug("Realized value is {}".format(modified_value))

        return modified_value
