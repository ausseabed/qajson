from collections import defaultdict
from jsonschema import validate, ValidationError, SchemaError, Draft7Validator
from pathlib import Path
from typing import Optional, Dict, List, Any
import json
import logging
import os
import time
import traceback

logger = logging.getLogger(__name__)


class QajsonFile:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonFile':
        instance = cls(
            path=data['path'],
            description=data['description'] if 'description' in data else None
        )
        return instance

    def __init__(self, path: str, description: str):
        self.path = path
        self.description = description

    def to_dict(self):
        dict = {
            'path': self.path,
        }
        if self.description is not None:
            dict['description'] = self.description
        return dict


class QajsonGroup:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonGroup':
        instance = cls(
            id=data['id'],
            name=data['name'] if 'name' in data else None,
            description=data['description'] if 'description' in data else None
        )
        return instance

    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    def to_dict(self):
        dict = {
            'id': self.id,
        }
        if self.name is not None:
            dict['name'] = self.name
        if self.description is not None:
            dict['description'] = self.description
        return dict


class QajsonExecution:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonExecution':
        instance = cls(
            start=data['start'] if 'start' in data else None,
            end=data['end'] if 'end' in data else None,
            status=data['status'] if 'status' in data else None,
            error=data['error'] if 'error' in data else None
        )
        return instance

    def __init__(self, start: str, end: str, status: str, error: str):
        self.start = start
        self.end = end
        self.status = status
        self.error = error

    def to_dict(self):
        dict = {
            'status': self.status,
        }
        if self.start is not None:
            dict['start'] = self.start
        if self.end is not None:
            dict['end'] = self.end
        if self.error is not None:
            dict['error'] = self.error
        return dict


class QajsonParam:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonParam':
        group = (
            QajsonGroup.from_dict(data['group']) if 'group' in data else None)
        instance = cls(
            name=data['name'],
            value=data['value']
        )
        return instance

    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value

    def to_dict(self):
        dict = {
            'name': self.name,
            'value': self.value
        }
        return dict


class QajsonInfo:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonInfo':
        group = (
            QajsonGroup.from_dict(data['group']) if 'group' in data else None)
        instance = cls(
            id=data['id'],
            name=data['name'] if 'name' in data else None,
            description=data['description'] if 'description' in data else None,
            version=data['version'] if 'version' in data else None,
            group=group,
        )
        return instance

    def __init__(
            self,
            id: str,
            name: str,
            description: str,
            version: str,
            group: QajsonGroup):
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.group = group

    def to_dict(self):
        dict = {
            'id': self.id,
        }
        if self.name is not None:
            dict['name'] = self.name
        if self.description is not None:
            dict['description'] = self.description
        if self.version is not None:
            dict['version'] = self.version
        if self.group is not None:
            dict['group'] = self.group.to_dict()
        return dict


class QajsonInputs:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonInputs':
        files = []
        if 'files' in data:
            files = [
                QajsonFile.from_dict(file_dict)
                for file_dict in data['files']
            ]
        params = []
        if 'params' in data:
            params = [
                QajsonParam.from_dict(param_dict)
                for param_dict in data['params']
            ]
        instance = cls(files=files, params=params)
        return instance

    def __init__(self, files: List[QajsonFile], params: List[QajsonParam]):
        self.files = files
        self.params = params

    def to_dict(self):
        return {
            'files': [file.to_dict() for file in self.files],
            'params': [param.to_dict() for param in self.params]
        }


class QajsonOutputs:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonOutputs':
        files = None
        if 'files' in data:
            files = [
                QajsonFile.from_dict(file_dict)
                for file_dict in data['files']
            ]

        instance = cls(
            execution=QajsonExecution.from_dict(data['execution']),
            files=files,
            count=data['count'] if 'count' in data else None,
            percentage=data['percentage'] if 'percentage' in data else None,
            message=data['message'] if 'message' in data else None,
            qa_pass=data['qa_pass'] if 'qa_pass' in data else None,
        )
        return instance

    def __init__(
            self,
            execution: QajsonExecution = None,
            files: List[QajsonFile] = None,
            count: int = None,
            percentage: float = None,
            message: str = None,
            qa_pass: str = None):
        self.execution = execution
        self.files = files
        self.count = count
        self.percentage = percentage
        self.message = message
        self.qa_pass = qa_pass

    def to_dict(self):
        dict = {
            'execution': QajsonExecution.to_dict(self.execution)
        }
        if self.files is not None:
            dict['files'] = [file.to_dict() for file in self.files]
        if self.count is not None:
            dict['count'] = self.count
        if self.percentage is not None:
            dict['percentage'] = self.percentage
        if self.message is not None:
            dict['message'] = self.message
        if self.qa_pass is not None:
            dict['qa_pass'] = self.qa_pass
        return dict


class QajsonCheck:

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonCheck':
        outputs = (
            QajsonOutputs.from_dict(data['outputs'])
            if 'outputs' in data else None)
        inputs = (
            QajsonInputs.from_dict(data['inputs'])
            if 'inputs' in data else None)

        instance = cls(
            info=QajsonInfo.from_dict(data['info']),
            outputs=outputs,
            inputs=inputs,
        )
        return instance

    def __init__(
            self,
            info: QajsonInfo,
            inputs: QajsonInputs,
            outputs: QajsonOutputs):
        self.info = info
        self.inputs = inputs
        self.outputs = outputs

    def get_or_add_inputs(self) -> QajsonInputs:
        if self.inputs is None:
            self.inputs = QajsonInputs(files=[], params=[])
        return self.inputs

    def to_dict(self):
        dict = {
            'info': self.info.to_dict(),
        }
        if self.inputs is not None:
            dict['inputs'] = self.inputs.to_dict()
        if self.outputs is not None:
            dict['outputs'] = self.outputs.to_dict()
        return dict


class QajsonDataLevel:
    """ Represents QA JSON data type. Data type refers to a grouping of
    input data loosly based on processed state. eg; raw data, or survey
    products.
    """

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonDataLevel':
        checks = []
        if 'checks' in data:
            checks = [
                QajsonCheck.from_dict(check_dict)
                for check_dict in data['checks']
            ]
        instance = cls(checks=checks)
        return instance

    def __init__(self, checks: List[QajsonCheck]):
        self.checks = checks

    def get_check(self, check_id: str) -> QajsonCheck:
        """ Gets a check based on id, or None if the check does not exist
        """
        check = next((c for c in self.checks if c.info.id == check_id), None)
        return check

    def to_dict(self):
        return {
            'checks': [check.to_dict() for check in self.checks]
        }


class QajsonQa:
    """ Represents QA JSON QA object. Includes metadata about the QA JSON
    """

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonQa':
        version = data['version'] if 'version' in data else None
        chart_adequacy = (
            QajsonDataLevel.from_dict(data['chart_adequacy'])
            if 'chart_adequacy' in data else None)
        instance = cls(
            version=version,
            raw_data=QajsonDataLevel.from_dict(data['raw_data']),
            survey_products=QajsonDataLevel.from_dict(data['survey_products']),
            chart_adequacy=chart_adequacy
        )
        return instance

    def __init__(
            self,
            version: str,
            raw_data: QajsonDataLevel,
            survey_products: QajsonDataLevel,
            chart_adequacy: QajsonDataLevel = None):
        self.version = version
        self.raw_data = raw_data
        self.survey_products = survey_products
        self.chart_adequacy = chart_adequacy

    def get_or_add_data_level(
            self, data_level: str) -> QajsonDataLevel:
        """ If a data level exists in the `qa` object it will be returned,
        otherwise a new QajsonDataLevel will be created, added to the qa object
        and returned
        """
        dl = getattr(self, data_level)
        if dl is None:
            dl = QajsonDataLevel(checks=[])
            setattr(self, data_level, dl)
        return dl

    def to_dict(self):
        dict = {
            'version': self.version,
            'raw_data': self.raw_data.to_dict(),
            'survey_products': self.survey_products.to_dict()
        }
        if self.chart_adequacy is not None:
            dict['chart_adequacy'] = self.chart_adequacy.to_dict()
        return dict


class QajsonRoot:
    """ Represents root of a QA JSON file
    """

    @classmethod
    def from_dict(cls, data: Dict) -> 'QajsonRoot':
        instance = cls(
            qa=QajsonQa.from_dict(data['qa']),
        )
        return instance

    def __init__(self, qa: QajsonQa):
        self.qa = qa

    def to_dict(self) -> Dict:
        return {
            'qa': self.qa.to_dict() if self.qa is not None else None
        }
