import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: All pairs of subsequent {parameters} were extracted and counted.
fi: Kaikki {parameters} noudettin ja laskettiin.
| name = ExtractBigrams
"""


class ExtractBigramsResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "ExtractBigrams":
            return []

        return [
            Message(
                Fact(
                    "task",
                    "ExtractBigrams",
                    "[ExtractBigrams:UNIT:{}]".format(task.parameters.get("unit", "stems")),
                    event.id,
                )
            )
        ]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [
            EnglishExtractBigramStemsRealizer,
            EnglishExtractBigramsTokenRealizer,
            #
            FinnishExtractBigramStemsRealizer,
            FinnishExtractBigramsTokenRealizer,
        ]


class EnglishExtractBigramStemsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[ExtractBigrams:UNIT:stems\]", [], "stems",
        )


class EnglishExtractBigramsTokenRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[ExtractBigrams:UNIT:tokens\]", [], "tokens",
        )


class FinnishExtractBigramStemsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "fi", r"\[ExtractBigrams:UNIT:stems\]", [], "tyviparit",
        )


class FinnishExtractBigramsTokenRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "fi", r"\[ExtractBigrams:UNIT:tokens\]", [], "saneparit",
        )
