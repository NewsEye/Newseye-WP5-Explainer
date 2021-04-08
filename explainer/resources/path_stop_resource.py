from typing import List, Type

from explainer.core.models import Fact, Message
from explainer.core.realize_slots import SlotRealizerComponent
from explainer.explainer_message_generator import Event
from explainer.resources.processor_resource import ReasonResource

TEMPLATE = """
en: This action was taken because the Investigator couldn't identify any meaningful step that would continue a previous track of investigation.
fi: Tämä tehtiin koska järjestelmä ei löytänyt mitään mielekästä tapaa jatkaa edellistä tutkimuslinjaa.
de: Diese Aktion wurde gemacht, weil der Investigator keinen sinnvollen Schritt identifizieren konnte, der vorhergehende Untersuchungen fortsetzen würde.
fr: Cette mesure a été entreprise car l'enquêteur n'a pu identifier d’étape significative permettant de poursuivre une précédente piste d'enquête.
| name = path_stop
"""  # noqa: E501


class PathStopResource(ReasonResource):
    def templates_string(self) -> str:
        return TEMPLATE

    def parse_reason(self, event: Event) -> List[Message]:
        task = event.reason
        if not task or task.name != "path stop":
            return []

        return [Message(Fact("reason", "path_stop", None, event.id))]

    def slot_realizer_components(self) -> List[Type[SlotRealizerComponent]]:
        return []
