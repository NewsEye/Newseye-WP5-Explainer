import logging
from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import TaskResource

log = logging.getLogger("root")


TEMPLATE = """
en: A topic model {parameters} was queried for similar documents.
| name = TopicModelDocumentLinking
"""


class TopicModelDocumentLinkingResource(TaskResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_task(self, event: Event) -> List[Message]:
        task = event.task
        if not task or task.name != "TopicModelDocumentLinking":
            return []

        return [
            Message(
                Fact(
                    "task",
                    "TopicModelDocumentLinking",
                    "[TopicModelDocumentLinking:NAME:{}] [TopicModelDocumentLinking:TYPE:{}]".format(
                        task.parameters.get("model_name"), task.parameters.get("model_type")
                    ),
                    event.id,
                )
            )
        ]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [EnglishTopicModelTypeRealizer, EnglishTopicModelNameRealizer]


class EnglishTopicModelTypeRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry,
            "en",
            r"(.*)\s?\[TopicModelDocumentLinking:TYPE:([^\]]*)\]\s?(.*)",
            (1, 2, 3),
            "{} of the {} variety {}",
        )


class EnglishTopicModelNameRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "en", r"(.*)\s?\[TopicModelDocumentLinking:NAME:([^\]]*)\]\s?(.*)", (1, 2, 3), "{} called {} {}",
        )
