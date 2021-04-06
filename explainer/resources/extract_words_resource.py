import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: All {parameters} were extracted and counted.
fi: Aineistossa esiintyvät {parameters} laskettiin.
de: Alle {parameters} wurden extrahiert und gezählt.
| name = ExtractWords
"""


class ExtractWordsResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "ExtractWords":
            return []

        return [
            Message(
                Fact(
                    "task",
                    "ExtractWords",
                    "[ExtractWords:UNIT:{}]".format(task.parameters.get("units", "stems")),
                    event.id,
                )
            )
        ]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [
            EnglishExtractWordStemsRealizer,
            EnglishExtractWordTokenRealizer,
            #
            FinnishExtractWordStemsRealizer,
            FinnishExtractWordTokenRealizer,
            #
            GermanExtractWordStemsRealizer,
            GermanExtractWordTokenRealizer,
        ]


class EnglishExtractWordStemsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[ExtractWords:UNIT:stems\]", [], "stems",
        )


class EnglishExtractWordTokenRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(registry, "en", r"\[ExtractWords:UNIT:tokens\]", [], "tokens")


class FinnishExtractWordStemsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "fi", r"\[ExtractWords:UNIT:stems\]", [], "tyvet",
        )


class FinnishExtractWordTokenRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(registry, "fi", r"\[ExtractWords:UNIT:tokens\]", [], "saneet")


class GermanExtractWordStemsRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "de", r"\[ExtractWords:UNIT:stems\]", [], "Stämme",
        )


class GermanExtractWordTokenRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(registry, "de", r"\[ExtractWords:UNIT:tokens\]", [], "Token")
