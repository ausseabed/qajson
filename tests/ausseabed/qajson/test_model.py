import unittest

from ausseabed.qajson.model import QajsonFile, QajsonParam, QajsonInputs, \
    QajsonOutputs, QajsonInfo


class TestModel(unittest.TestCase):

    qajson_file_dict = {
        "path": "test/path/test.txt",
        "description": "test file",
        "file_type": "Raw Files"
    }

    qajson_param_01_dict = {
        "name": "threshold",
        "value": 123
    }

    qajson_outputs = {
        "percentage": 55,
        "execution": {
            "start": "2019-07-08T14:56:49.006647",
            "end": "2019-07-08T14:56:49.006677",
            "status": "completed"
        },
        "files": [
            {"path": "t3.txt", "file_type": "unknown"},
            {"path": "t4.txt", "file_type": "unknown"}
        ],
        "messages": ["message one", "message two"],
        "check_state": "pass"
    }

    qajson_outputs_minimal = {
        "execution": {
            "start": "2019-07-08T14:56:49.006647",
            "end": "2019-07-08T14:56:49.006677",
            "status": "completed"
        }
    }

    qajson_outputs_data = {
        "execution": {
            "start": "2019-07-08T14:56:49.006647",
            "end": "2019-07-08T14:56:49.006677",
            "status": "completed"
        },
        "data": {
            "var1": 1234,
            "list_var": [1, 2, 3, 4]
        }
    }

    qajson_info = {
        "id": "7761e08b-1380-46fa-a7eb-f1f41db38541",
        "name": "Filename checked",
        "description": "desc",
        "version": "1",
        "group": {
            "id": "123",
            "name": "123"
        }
    }

    qajson_inputs = {
        "files": [qajson_file_dict],
        "params": []
    }

    def test_qajson_file(self):
        # converts dict to QajsonFile object, then back to dict for
        # comparison
        qajson_file = QajsonFile.from_dict(TestModel.qajson_file_dict)
        qajson_file_dict_test = QajsonFile.to_dict(qajson_file)
        self.assertDictEqual(
            TestModel.qajson_file_dict,
            qajson_file_dict_test
        )

    def test_qajson_param(self):
        p1 = QajsonParam.from_dict(TestModel.qajson_param_01_dict)
        self.assertDictEqual(TestModel.qajson_param_01_dict, p1.to_dict())

    def test_qajson_inputs(self):
        i1 = QajsonInputs.from_dict(TestModel.qajson_inputs)
        self.assertDictEqual(TestModel.qajson_inputs, i1.to_dict())

    def test_qajson_outputs_minimal(self):
        # checks an output object that only has the required parameters set
        o1 = QajsonOutputs.from_dict(TestModel.qajson_outputs_minimal)
        self.assertDictEqual(TestModel.qajson_outputs_minimal, o1.to_dict())

    def test_qajson_outputs_with_data(self):
        # checks an output object that only has the required parameters set
        o1 = QajsonOutputs.from_dict(TestModel.qajson_outputs_data)
        self.assertDictEqual(TestModel.qajson_outputs_data, o1.to_dict())

    def test_qajson_outputs(self):
        o1 = QajsonOutputs.from_dict(TestModel.qajson_outputs)
        self.assertDictEqual(TestModel.qajson_outputs, o1.to_dict())

    def test_qajson_info(self):
        i1 = QajsonInfo.from_dict(TestModel.qajson_info)
        self.assertDictEqual(TestModel.qajson_info, i1.to_dict())
