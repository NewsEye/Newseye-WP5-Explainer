import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: The change of sentiment towards identified entities over time was identified.
fi: Tarkasteltiin kuinka aineiston suuntautuminen eri entiteetteihin vaihtelee eri ajanjaksoina.
| name = TrackNameSentiment
"""


class TrackNameSentimentResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "TrackNameSentiment":
            return []

        return [Message(Fact("task", "TrackNameSentiment", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
