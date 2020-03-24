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

        document_plan: DocumentPlanNode = DocumentPlanNode(children=[], relation=Relation.SEQUENCE)

        paragraph: DocumentPlanNode = DocumentPlanNode(children=[], relation=Relation.SEQUENCE)
        paragraph.children.append(messages[0])
        for message in messages[1:]:
            if message.main_fact.type == "task":
                document_plan.children.append(paragraph)
                paragraph = DocumentPlanNode(children=[message], relation=Relation.SEQUENCE)
            else:
                paragraph.children.append(message)

        document_plan.children.append(paragraph)

        return (document_plan, messages)
