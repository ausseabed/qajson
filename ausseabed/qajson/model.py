from typing import Any
from abc import ABC, abstractmethod

import json
import logging

logger = logging.getLogger(__name__)


class QajsonObject(ABC):
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass

    def __repr__(self):
        return type(self).__name__ + "\n" + json.dumps(self.to_dict(), indent=4) + "\n"


class QajsonFile(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonFile":
        instance = cls(
            path=data["path"],
            file_type=data["file_type"],
            description=data.get("description", None),
        )
        return instance

    def __init__(self, path: str, file_type: str, description: str | None):
        self.path = path
        self.file_type = file_type
        self.description = description

    def to_dict(self) -> dict[str, Any]:
        out = {
            "path": self.path,
            "file_type": self.file_type,
        }
        if self.description is not None:
            out["description"] = self.description
        return out


class QajsonGroup(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonGroup":
        instance = cls(
            id=data["id"],
            name=data.get("name", None),
            description=data.get("description", None),
        )
        return instance

    def __init__(self, id: str, name: str | None, description: str | None):
        self.id = id
        self.name = name
        self.description = description

    def to_dict(self) -> dict[str, Any]:
        out = {
            "id": self.id,
        }
        if self.name is not None:
            out["name"] = self.name
        if self.description is not None:
            out["description"] = self.description
        return out


class QajsonExecution(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonExecution":
        instance = cls(
            start=data.get("start", None),
            end=data.get("end", None),
            status=data.get("status", None),
            error=data.get("error", None),
        )
        return instance

    def __init__(
        self,
        start: str | None,
        end: str | None,
        status: str | None,
        error: str | None,
    ):
        self.start = start
        self.end = end
        self.status = status
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "status": self.status,
        }
        if self.start is not None:
            out["start"] = self.start
        if self.end is not None:
            out["end"] = self.end
        if self.error is not None:
            out["error"] = self.error
        return out


class QajsonParam(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonParam":
        options = data.get("options", None)
        instance = cls(
            name=data["name"],
            value=data["value"],
            options=options,
        )
        return instance

    def __init__(
        self,
        name: str,
        value: Any,
        options: None | list[Any] = None,
    ):
        self.name = name
        self.value = value
        # Note: for the most part the options list is not used within QAJSON. It is
        # however used in some situations where a parameter must be of a certain value
        # QAX uses this options list to build pick lists when given
        self.options = options

    def to_dict(self) -> dict[str, Any]:
        out = {
            "name": self.name,
            "value": self.value,
        }
        if self.options is not None:
            out["options"] = self.options
        return out


class QajsonInfo(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonInfo":
        group = QajsonGroup.from_dict(data["group"]) if "group" in data else None
        instance = cls(
            id=data["id"],
            name=data.get("name", None),
            description=data.get("description", None),
            version=data.get("version", None),
            group=group,
        )
        return instance

    def __init__(
        self,
        id: str,
        name: str | None = None,
        description: str | None = None,
        version: str | None = None,
        group: QajsonGroup | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.group = group

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "id": self.id,
        }
        if self.name is not None:
            out["name"] = self.name
        if self.description is not None:
            out["description"] = self.description
        if self.version is not None:
            out["version"] = self.version
        if self.group is not None:
            out["group"] = self.group.to_dict()
        return out


class QajsonInputs(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonInputs":
        files = []
        if "files" in data:
            files = [QajsonFile.from_dict(file_dict) for file_dict in data["files"]]
        params = []
        if "params" in data:
            params = [
                QajsonParam.from_dict(param_dict) for param_dict in data["params"]
            ]
        instance = cls(files=files, params=params)
        return instance

    def __init__(self, files: list[QajsonFile], params: list[QajsonParam]):
        self.files = files
        self.params = params

    def to_dict(self) -> dict[str, Any]:
        return {
            "files": [file.to_dict() for file in self.files],
            "params": [param.to_dict() for param in self.params],
        }


class QajsonOutputs(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonOutputs":
        files = None
        if "files" in data:
            files = [QajsonFile.from_dict(file_dict) for file_dict in data["files"]]

        instance = cls(
            execution=QajsonExecution.from_dict(data["execution"]),
            files=files,
            count=data.get("count"),
            percentage=data.get("percentage", None),
            messages=data.get("messages", None),
            data=data.get("data", None),
            check_state=data.get("check_state", None),
        )
        return instance

    def __init__(
        self,
        execution: QajsonExecution,
        files: list[QajsonFile] | None = None,
        count: int | None = None,
        percentage: float | None = None,
        messages: list[str] | None = None,
        data: dict[str, Any] | None = None,
        check_state: str | None = None,
    ):
        self.execution = execution
        self.files = files
        self.count = count
        self.percentage = percentage
        self.messages = messages
        self.data = data
        self.check_state = check_state

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"execution": self.execution.to_dict()}
        if self.files is not None:
            out["files"] = [file.to_dict() for file in self.files]
        if self.count is not None:
            out["count"] = self.count
        if self.percentage is not None:
            out["percentage"] = self.percentage
        if self.messages is not None:
            out["messages"] = self.messages
        if self.data is not None:
            out["data"] = self.data
        if self.check_state is not None:
            out["check_state"] = self.check_state
        return out


class QajsonCheck(QajsonObject):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonCheck":
        outputs = (
            QajsonOutputs.from_dict(data["outputs"]) if "outputs" in data else None
        )
        inputs = QajsonInputs.from_dict(data["inputs"]) if "inputs" in data else None

        instance = cls(
            info=QajsonInfo.from_dict(data["info"]),
            outputs=outputs,
            inputs=inputs,
        )
        return instance

    def __init__(
        self,
        info: QajsonInfo,
        inputs: QajsonInputs | None = None,
        outputs: QajsonOutputs | None = None,
    ):
        self.info = info
        self.inputs = inputs
        self.outputs = outputs

    def get_or_add_inputs(self) -> QajsonInputs:
        if self.inputs is None:
            self.inputs = QajsonInputs(files=[], params=[])
        return self.inputs

    def to_dict(self) -> dict[str, Any]:
        out = {
            "info": self.info.to_dict(),
        }
        if self.inputs is not None:
            out["inputs"] = self.inputs.to_dict()
        if self.outputs is not None:
            out["outputs"] = self.outputs.to_dict()
        return out


class QajsonDataLevel(QajsonObject):
    """Represents QA JSON data type. Data type refers to a grouping of
    input data loosly based on processed state. eg; raw data, or survey
    products.
    """

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonDataLevel":
        checks = []
        if "checks" in data:
            checks = [
                QajsonCheck.from_dict(check_dict) for check_dict in data["checks"]
            ]
        instance = cls(checks=checks)
        return instance

    def __init__(self, checks: list[QajsonCheck]):
        self.checks = checks

    def get_check(self, check_id: str) -> QajsonCheck | None:
        """Gets a check based on id, or None if the check does not exist"""
        check = next((c for c in self.checks if c.info.id == check_id), None)
        return check

    def to_dict(self) -> dict[str, Any]:
        return {"checks": [check.to_dict() for check in self.checks]}


class QajsonQa(QajsonObject):
    """Represents QA JSON QA object. Includes metadata about the QA JSON"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonQa":
        version = data.get("version", None)
        chart_adequacy = (
            QajsonDataLevel.from_dict(data["chart_adequacy"])
            if "chart_adequacy" in data
            else None
        )
        instance = cls(
            version=version,
            raw_data=QajsonDataLevel.from_dict(data["raw_data"]),
            survey_products=QajsonDataLevel.from_dict(data["survey_products"]),
            chart_adequacy=chart_adequacy,
        )
        return instance

    def __init__(
        self,
        version: str | None,
        raw_data: QajsonDataLevel,
        survey_products: QajsonDataLevel,
        chart_adequacy: QajsonDataLevel | None = None,
    ):
        self.version = version
        self.raw_data = raw_data
        self.survey_products = survey_products
        self.chart_adequacy = chart_adequacy

    def get_or_add_data_level(self, data_level: str) -> QajsonDataLevel:
        """If a data level exists in the `qa` object it will be returned,
        otherwise a new QajsonDataLevel will be created, added to the qa object
        and returned
        """
        dl = self.get_data_level(data_level)
        if dl is None:
            dl = QajsonDataLevel(checks=[])
            setattr(self, data_level, dl)
        return dl

    def get_data_level(self, data_level: str) -> QajsonDataLevel:
        """If a data level exists in the `qa` object it will be returned,
        otherwise None will be returned
        """
        dl = getattr(self, data_level)
        return dl

    def to_dict(self) -> dict[str, Any]:
        out = {
            "version": self.version,
            "raw_data": self.raw_data.to_dict(),
            "survey_products": self.survey_products.to_dict(),
        }
        if self.chart_adequacy is not None:
            out["chart_adequacy"] = self.chart_adequacy.to_dict()
        return out


class QajsonRoot(QajsonObject):
    """Represents root of a QA JSON file"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "QajsonRoot":
        instance = cls(
            qa=QajsonQa.from_dict(data["qa"]),
        )
        return instance

    def __init__(self, qa: QajsonQa):
        self.qa = qa

    def to_dict(self) -> dict[str, Any]:
        return {"qa": self.qa.to_dict() if self.qa is not None else None}
