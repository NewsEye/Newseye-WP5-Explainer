import logging
from typing import Dict, Optional

from uralicNLP import uralicApi

from explainer.core.models import Slot
from explainer.core.morphological_realizer import LanguageSpecificMorphologicalRealizer

log = logging.getLogger("root")


class FinnishUralicNLPMorphologicalRealizer(LanguageSpecificMorphologicalRealizer):
    def __init__(self):
        super().__init__("fi")

        self.case_map: Dict[str, str] = {"ssa": "Ine", "ssä": "Ine", "inessive": "Ine", "genitive": "Gen"}

    def realize(self, slot: Slot) -> str:
        case: Optional[str] = slot.attributes.get("case")
        if case is None:
            return slot.value

        log.debug("Realizing {} to Finnish")

        case = self.case_map.get(case.lower(), case.capitalize())
        log.debug("Normalized case {} to {}".format(slot.attributes.get("case"), case))

        possible_analyses = uralicApi.analyze(slot.value, "fin")
        log.debug("Identified {} possible analyses".format(len(possible_analyses)))
        if len(possible_analyses) == 0:
            log.warning(
                "No valid morphological analysis for {}, unable to realize despite case attribute".format(slot.value)
            )
            return slot.value

        analysis = possible_analyses[0][0]
        log.debug("Picked {} as the morphological analysis of {}".format(analysis, slot.value))

        # We only want to replace the last occurence of "Nom", as otherwise all parts of compound words, rather than
        # only the last, get transformed to genitive. This is simply wrong for, e.g. "tyvipari". Simply doing a global
        # replacement results in *"tyvenparin", rather than "tyviparin". Unfortunately, python lacks a replace() which
        # starts from the right, so we need to identify the correct instance of "Nom" with rfind() and then manually
        # fiddle with slices.
        gen_start_idx = analysis.rfind("Nom")
        analysis = analysis[:gen_start_idx] + "Gen" + analysis[gen_start_idx + 4 :]  # 4 = 1 + len("Nom")
        log.debug("Modified analysis to {}".format(analysis))

        modified_value = uralicApi.generate(analysis, "fin")[0][0]
        log.debug("Realized value is {}".format(modified_value))

        return modified_value
