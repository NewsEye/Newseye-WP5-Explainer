import json
import logging
from typing import Any, Callable, Dict, List, Tuple

from numpy.random import Generator

from explainer.core.message_generator import NoMessagesForSelectionException
from explainer.core.models import Fact, Message
from explainer.core.pipeline import NLGPipelineComponent, Registry

log = logging.getLogger("root")


class Task:
    def __init__(self, name: str, parameters: Dict[str, Any]) -> None:
        self.name = name
        self.parameters = parameters

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "Task":
        return Task(dict.get("name", "UNNAMED_TASK"), dict.get("parameters", {}))


class Reason:
    def __init__(self, name: str, parameters: Dict[str, Any]) -> None:
        self.name = name
        self.parameters = parameters

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "Reason":
        return Reason(dict.get("name", "UNNAMED_REASON"), dict.get("parameters", {}))


class Event:
    def __init__(self, task: Task, reason: Reason, id: str) -> None:
        self.task = task
        self.reason = reason
        self.id = id

    @staticmethod
    def from_dict(dict: Dict[str, Any]) -> "Event":
        task = Task.from_dict(dict["task"]) if "task" in dict else None
        reason = Reason.from_dict(dict["reason"]) if "reason" in dict else None
        return Event(task, reason, dict.get("id"))


class ExplainerMessageGenerator(NLGPipelineComponent):
    def run(
        self, registry: Registry, random: Generator, language: str, data: List[Dict[str, str]]
    ) -> Tuple[List[Message]]:
        """
        Run this pipeline component.
        """

        if not data:
            raise NoMessagesForSelectionException("No data at all!")

        task_parsers: List[Callable[[Event], List[Message]]] = registry.get("task-parsers")
        reason_parsers: List[Callable[[Event], List[Message]]] = registry.get("reason-parsers")
        events: List[Event] = [Event.from_dict(event) for event in json.loads(data)]

        messages: List[Message] = []

        for event in events:
            task_generation_succeeded = False
            for task_parser in task_parsers:
                try:
                    new_messages = task_parser(event)
                    for message in new_messages:
                        log.debug("Parsed message {}".format(message))
                    if new_messages:
                        task_generation_succeeded = True
                        messages.extend(new_messages)
                except Exception as ex:
                    log.error("Task parser crashed: {}".format(ex), exc_info=True)

            if not task_generation_succeeded:
                messages.append(
                    Message(Fact("task", "UNKNOWN_TASK:{}".format(event.task.name), event.task.parameters, event.id))
                )
                log.error("Failed to parse a Message from {}".format(event.task))

            reason_generation_succeeded = False
            for reason_parser in reason_parsers:
                try:
                    new_messages = reason_parser(event)
                    for message in new_messages:
                        log.debug("Parsed message {}".format(message))
                    if new_messages:
                        reason_generation_succeeded = True
                        messages.extend(new_messages)
                except Exception as ex:
                    log.error("Reason parser crashed: {}".format(ex), exc_info=True)

            if not reason_generation_succeeded:
                messages.append(
                    Message(
                        Fact("reason", "UNKNOWN_REASON:{}".format(event.task.name), event.reason.parameters, event.id)
                    )
                )
                log.error("Failed to parse a Message from {}".format(event.reason))

        log.debug("Generated {} messages".format(len(messages)))

        if not messages:
            raise NoMessagesForSelectionException()

        return (messages,)
