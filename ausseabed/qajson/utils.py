from ausseabed.qajson.model import QajsonFile, QajsonParam, QajsonInputs, \
    QajsonOutputs, QajsonInfo, QajsonRoot, QajsonQa, QajsonDataLevel
from ausseabed.qajson.parser import QajsonParser
import os


def latest_schema_version() -> str:
    ''' Gets the latest schema version '''
    schema_paths = QajsonParser.schema_paths()
    if len(schema_paths) == 0:
        raise RuntimeError("No schemas found")

    schema_path = schema_paths[-1]
    # get the folder name that the schema file was found in eg "v0.1.4"
    schema_version_name = os.path.basename(os.path.dirname(schema_path))
    if schema_version_name[0] != 'v':
        raise RuntimeError("Unexpected schema location {}".format(schema_path))

    version = schema_version_name[1:]
    return version


def minimal_qajson() -> QajsonRoot:
    ''' Builds a minimal QAJSON structure '''

    version = latest_schema_version()
    raw_data = QajsonDataLevel([])
    survey_products = QajsonDataLevel([])

    qa = QajsonQa(
        version=version,
        raw_data=raw_data,
        survey_products=survey_products,
    )

    root = QajsonRoot(qa=qa)
    return root
