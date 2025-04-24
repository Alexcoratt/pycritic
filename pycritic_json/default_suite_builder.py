import os
import json
import jsonschema

import logging

from abc import ABC, abstractmethod
import typing as t

import pycritic

from .src.checker_builder import \
	BasicJsonCheckerBuilder
from .src.criterion_builder import \
	JsonCriterionBuilder, BasicJsonCriterionBuilder
from .src.suite_builder import \
	BasicJsonSuiteBuilder, ValidatingJsonCriterionBuilder

from .src.data_loader import \
	CheckerDataLoader, CriterionDataLoader



class JsonConditionBuilder(ABC):
	@abstractmethod
	def __call__(self, raw: t.Any) -> pycritic.Condition:
		pass



class DefaultJsonCmpCondtionBuilder(JsonConditionBuilder):
	def __init__(self, func: t.Callable[[
		t.Any,	# compared argument
		t.Any	# example
	], t.Any]) -> None:
		self.__func = func


	def __call__(self, raw: t.Any) -> pycritic.Condition:
		example = raw["example"]
		return lambda arg: self.__func(arg, example)



class DefaultJsonFitConditionBuilder(JsonConditionBuilder):
	def __init__(self, includeMin: bool, includeMax: bool) -> None:
		self.includeMin = includeMin
		self.includeMax = includeMax


	def __call__(self, raw: t.Any) -> pycritic.Condition:
		minCmp = self.makeMinCmp(raw)
		maxCmp = self.makeMaxCmp(raw)
		return lambda arg: minCmp(arg) and maxCmp(arg)

	
	def makeMinCmp(self, raw: t.Any) -> pycritic.Condition:
		minValue = raw["min"]
		return lambda arg: self.includeMin and minValue <= arg or minValue < arg


	def makeMaxCmp(self, raw: t.Any) -> pycritic.Condition:
		maxValue = raw["max"]
		return lambda arg: self.includeMax and maxValue >= arg or maxValue > arg



class DefaultCheckerDataLoader(CheckerDataLoader):
	CONDITION_BUILDER_MAPPING = {
		# binary comparison
		"lt": DefaultJsonCmpCondtionBuilder(lambda l, r: l < r),
		"le": DefaultJsonCmpCondtionBuilder(lambda l, r: l <= r),
		"gt": DefaultJsonCmpCondtionBuilder(lambda l, r: l > r),
		"ge": DefaultJsonCmpCondtionBuilder(lambda l, r: l >= r),
		"eq": DefaultJsonCmpCondtionBuilder(lambda l, r: l == r),
		"ne": DefaultJsonCmpCondtionBuilder(lambda l, r: l != r),

		# ternary comparison
		"fit": DefaultJsonFitConditionBuilder(False, False),
		"nfit": DefaultJsonFitConditionBuilder(True, False),
		"xfit": DefaultJsonFitConditionBuilder(False, True),
		"nxfit": DefaultJsonFitConditionBuilder(True, True),

		# default operation
		"": lambda _: bool
	}


	def __init__(self, raw: t.Any) -> None:
		if not isinstance(raw, t.Mapping):
			raise TypeError(f"mapping expected: {raw}")
		funcName = raw.get("func", "")
		builder = DefaultCheckerDataLoader.CONDITION_BUILDER_MAPPING[funcName]

		self.__condition = builder(raw)
		self.__argName = raw["arg"]


	def loadCondition(self) -> pycritic.Condition:
		return self.__condition


	def loadArgName(self) -> str:
		return self.__argName



class DefaultCriterionDataLoader(CriterionDataLoader[t.Any]):
	CHECKER_BUILDER = BasicJsonCheckerBuilder(DefaultCheckerDataLoader)


	def __init__(self, raw: t.Any) -> None:
		self.__estimation = raw["est"]
		self.__checkers = map(
			DefaultCriterionDataLoader.CHECKER_BUILDER,
			raw["cond"]
		)


	def loadEstimation(self) -> t.Any:
		return self.__estimation


	def loadCheckers(self) -> t.Iterable[pycritic.Checker]:
		return self.__checkers
		


def makeDefaultJsonSuiteBuilder() -> JsonCriterionBuilder:
	criterionBuilder = BasicJsonCriterionBuilder(DefaultCriterionDataLoader)
	suiteBuilder = BasicJsonSuiteBuilder(criterionBuilder)

	schema = loadSchema()
	validator = lambda raw: jsonschema.validate(raw, schema)

	return ValidatingJsonCriterionBuilder(suiteBuilder, validator)



def loadSchema() -> t.Any:
	filename = getSchemaFilename()
	with open(filename) as file:
		return json.load(file)



SCHEMA_ENV_KEY = "PYCRITIC_SUITE_SCHEMA"
DEFAULT_SCHEMA_FILENAME = "../schemas/suite.schema.json"


def getSchemaFilename() -> str:
	try:
		return os.environ[SCHEMA_ENV_KEY]
	except KeyError:
		dir = os.path.dirname(__file__)
		filename = os.path.join(dir, DEFAULT_SCHEMA_FILENAME)
		logging.warning(f"using the default pycritic schema file: {filename}")
		return filename
