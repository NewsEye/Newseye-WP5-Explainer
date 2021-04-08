from typing import List, Type

from explainer.core.models import Message
from explainer.core.realize_slots import RegexRealizer, SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: A task called {name} was completed with the paramaters {parameters}. Please report how, where, and when you encountered this message by email to leo.leppanen@helsinki.fi.
fi: Suoritettiin tuntematon analyysi nimeltä {name} (parametreina {parameters} ). Autat järjestelmän kehitystyötä jos kerrot milloin ja missä yhteydessä törmäsit tähän viestiin sähköpostitse osoitteeseen leo.leppanen@helsinki.fi.
de: Der Schritt {name} wurde mit dem Paramater {parameters} ausgeführt. Bitte berichten Sie per E-Mail an leo.leppanen@helsinki.fi, wie, wo und wann Sie diese Meldung erhalten haben.
fr: Une tâche appelée {name} a été effectuée avec les paramètres {parameters}. Veuillez écrire à leo.leppanen@helsinki.fi pour lui signifier comment, où et quand vous avez rencontré ce message.
| name = UNKNOWN_TASK:.*
"""  # noqa: E501


class UnknownTaskResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        return []

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return [UnknownTaskNameRealizer]


class UnknownTaskNameRealizer(RegexRealizer):
    def __init__(self, registry):
        super().__init__(
            registry, "ANY", r"UNKNOWN_TASK:(.*)", (1), "'{}'",
        )
