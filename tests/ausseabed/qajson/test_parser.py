import os
import unittest

from ausseabed.qajson.model import QajsonFile, QajsonParam, QajsonInputs, \
    QajsonOutputs, QajsonInfo, QajsonRoot, QajsonQa, QajsonDataLevel
from ausseabed.qajson.parser import QajsonParser


class TestParser(unittest.TestCase):

    def test_qajson_read(self):
        here = os.path.abspath(os.path.dirname(__file__))
        test_file = os.path.join(here, "qa_json_test.json")

        qajson = QajsonParser(test_file)

        self.assertIsInstance(qajson.root, QajsonRoot)
        self.assertIsInstance(qajson.root.qa, QajsonQa)

        self.assertEqual(qajson.root.qa.version, '0.1.4')

        self.assertIsInstance(qajson.root.qa.raw_data, QajsonDataLevel)
        self.assertIsInstance(qajson.root.qa.survey_products, QajsonDataLevel)
        self.assertIsInstance(qajson.root.qa.chart_adequacy, QajsonDataLevel)
