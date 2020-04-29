# QAJSON
QAJSON is a JSON schema definition created by the AusSeabed project to define Quality Assurance (QA) checks, check parameters, and input data files. QAJSON also supports the storage of QA check results.


# Testing

Unit tests can be run with the following command from the project root directory.

    python -m pytest -s --cov=ausseabed.qajson tests/

Or, to run only a single specific test.

    python -m pytest -s --cov=ausseabed.qajson  tests/ausseabed/qajson/test_model.py::TestModel::test_qa_json_file
