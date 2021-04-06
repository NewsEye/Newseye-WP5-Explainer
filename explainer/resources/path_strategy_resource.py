from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This was done because the Investigator is attempting to expand on an intermediate result.
fi: Tämä tehtiin koska järjestelmä pyrkii käsittelemään jotain aiempaa tulosta laajemmin.
de: Dies wurde getan, weil Investigator zu erweitern auf ein Zwischenergebnis versucht.
| name = path_strategy_expansion

en: This was done because the Investigator is attempting to elaborate on an intermediate result.
fi: Tämä tehtiin koska järjestelmä pyrkii käsittelemään jotain aiempaa tulosta syvällisemmin.
de: Dies wurde getan, weil Investigator versucht, ein Zwischenergebnis zu erarbeiten auf.
| name = path_strategy_elaboration
"""  # noqa: E501


class PathStrategyResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        reason = event.reason
        if not reason or reason.name != "path strategy":
            return []

        return [Message(Fact("reason", "path_strategy_{}".format(reason.strategy), None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
