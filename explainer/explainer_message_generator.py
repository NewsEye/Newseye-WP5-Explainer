import json
import logging
from typing import Dict, List, Tuple

from numpy.random import Generator

from explainer.core.message_generator import NoMessagesForSelectionException
from explainer.core.models import Fact, Message
from explainer.core.pipeline import NLGPipelineComponent, Registry

log = logging.getLogger("root")


class ExplainerMessageGenerator(NLGPipelineComponent):
    def run(
        self, registry: Registry, random: Generator, language: str, data: List[Dict[str, str]]
    ) -> Tuple[List[Message]]:
        """
        Run this pipeline component.
        """

        if not data:
            raise NoMessagesForSelectionException("No data at all!")
        messages = [
            Message(
                Fact(
                    "[ACTION:{}]".format(o.get("action", "UNKNOWN_ACTION")),
                    "[REASON:{}]".format(o.get("reason", "UNKNOWN_REASON")),
                    o.get("id"),
                )
            )
            for o in json.loads(data)
        ]
        log.debug("Generated {} messages".format(len(messages)))

        if not messages:
            raise NoMessagesForSelectionException()

        return (messages,)
