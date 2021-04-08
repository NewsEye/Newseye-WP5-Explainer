import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent, RegexRealizer
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")

TEMPLATE = """
en: The {parameters} named entities were identified from the corpus.
fi: Aineistosta tunnistettiin {parameters} siinä esiintyvää entiteettiä tunnistettiin.
de: Die {parameters} Entitäten des Korpus wurden identifiziert.
fr: {parameters} ont été identifiées à partir du corpus.
| name = ExtractNames
"""


class ExtractNamesResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "ExtractNames":
            return []

        return [
            Message(
                Fact(
                    "task",
                    "ExtractNames",
                    "[ExtractNames:{}:{}]".format(
                        event.task.parameters.get("sort_by"), event.task.parameters.get("max_number")
                    ),
                    event.id,
                )
            )
        ]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [
            EnglishExtractNamesParameterRealizer,
            #
            FinnishExtractNamesParameterRealizer,
            #
            GermanExtractNamesParameterRealizer,
            #
            FrenchExtractNamesParameterRealizer,
        ]


class EnglishExtractNamesParameterRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"\[ExtractNames:salience:([^\]]*)\]", [1], "{} most salient",
        )


class FinnishExtractNamesParameterRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "fi", r"\[ExtractNames:salience:([^\]]*)\]", [1], "{} tärkeintä",
        )


class GermanExtractNamesParameterRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "de", r"\[ExtractNames:salience:([^\]]*)\]", [1], "{} auffälligsten benannten",
        )


class FrenchExtractNamesParameterRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "fr", r"\[ExtractNames:salience:([^\]]*)\]", [1], "Les {} entités nommées les plus saillantes",
        )
