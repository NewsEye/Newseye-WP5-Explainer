from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This was done because it's an integral part of the global strategy selected at the start of the experiment.
fi: Tämä tehtiin koska se on oleellinen osa koeasetelman alussa määriteltyä globaalia strategiaa.
de: Dies wurde gemacht, weil es ein integraler Bestandteil der globalen Strategie ist, die am Beginn des Experiments ausgewählt wurde.
| name = global_strategy
"""  # noqa: E501


class GlobalStrategyResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "global strategy":
            return []

        return [Message(Fact("reason", "global_strategy", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
