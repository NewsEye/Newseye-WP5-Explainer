import logging
from typing import List, Tuple

from numpy.random.generator import Generator

from explainer.core.document_planner import DocumentPlanner
from explainer.core.models import DocumentPlanNode, Message, Relation
from explainer.core.registry import Registry

log = logging.getLogger("root")


class ExplainerDocumentPlanner(DocumentPlanner):
    def run(
        self, registry: Registry, random: Generator, language: str, messages: List[Message]
    ) -> Tuple[DocumentPlanNode, List[Message]]:

        document_plan: DocumentPlanNode = DocumentPlanNode(
            children=[DocumentPlanNode(children=messages, relation=Relation.SEQUENCE)], relation=Relation.SEQUENCE
        )

        return (document_plan, messages)
