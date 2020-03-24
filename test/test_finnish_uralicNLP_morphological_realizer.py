from unittest import TestCase, main

from explainer.core.models import Fact, FactField, FactFieldSource, LiteralSlot, Matcher, Message, Slot, Template
from explainer.finnish_uralicNLP_morphological_realizer import FinnishUralicNLPMorphologicalRealizer


class TestRealization(TestCase):
    def setUp(self):
        self.fact = Fact("1", "kissa", "params", "id",)
        self.message = Message(self.fact)

        self.expr = FactField("type")
        self.matcher = Matcher(self.expr, "=", "1")
        self.rules = [([self.matcher], [0])]

        self.slot = Slot(FactFieldSource("name"))
        self.literal = LiteralSlot("sana")
        self.components = [self.slot, self.literal]

        self.template = Template(self.components, self.rules)
        self.template.fill(self.message, [self.message])

        self.realizer = FinnishUralicNLPMorphologicalRealizer()

    def test_no_attrs_slot_left_as_is(self):
        self.assertEqual("kissa", self.realizer.realize(self.slot))

    def test_no_attrs_literal_left_as_is(self):
        self.assertEqual("sana", self.realizer.realize(self.literal))

    def test_gen_slot_realized_correctly(self):
        self.slot.attributes["case"] = "genitive"
        self.assertEqual("kissan", self.realizer.realize(self.slot))

    def test_gen_literal_realized_correctly(self):
        self.literal.attributes["case"] = "genitive"
        self.assertEqual("sanan", self.realizer.realize(self.literal))


if __name__ == "__main__":
    main()
