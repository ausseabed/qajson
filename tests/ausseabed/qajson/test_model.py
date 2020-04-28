import unittest

from ausseabed.qajson.model import QaJsonFile


class TestModel(unittest.TestCase):

    qa_json_file_dict = {
        "path": "test/path/test.txt",
        "description": "test file"
    }

    def test_qa_json_file(self):
        # converts dict to QaJsonFile object, then back to dict for
        # comparison
        qa_json_file = QaJsonFile.from_dict(TestModel.qa_json_file_dict)
        qa_json_file_dict_test = QaJsonFile.to_dict(qa_json_file)
        self.assertDictEqual(
            TestModel.qa_json_file_dict,
            qa_json_file_dict_test
        )
