from abc import ABC, abstractmethod
import typing as t
import os
import re
import json
import jsonschema
import logging

import pycritic



SCHEMA_FILENAME_ENV_VARNAME = "PYCRITIC_JSON_CONVERTER_SCHEMA"
DEFAULT_SCHEMA_FILENAME = "../schemas/suite.schema.json"



def getDefaultSchemaFilename():
	try:
		return os.environ[SCHEMA_FILENAME_ENV_VARNAME]
	except KeyError:
		dir = os.path.dirname(__file__)
		return os.path.join(dir, DEFAULT_SCHEMA_FILENAME)



class SuiteConverter(ABC):
	@abstractmethod
	def __call__(self, rawSuite: t.Any) -> pycritic.Suite:
		pass


	def convertFromFile(self, filename: str) -> pycritic.Suite:
		with open(filename) as file:
			rawSuite = json.load(file)
		return self.__call__(rawSuite)



class BasicSuiteConverter(SuiteConverter):
	def __init__(self, schema: t.Any = None) -> None:
		self.resetSchema(schema)
	

	def resetSchema(self, schema: t.Any = None) -> None:
		if schema is None:
			self.resetDefaultSchema()
		self.__schema = schema


	def resetDefaultSchema(self) -> None:
		filename = getDefaultSchemaFilename()
		logging.warning(f"using default schema: {filename}")
		with open(filename) as file:
			self.__schema = json.load(file)


	def __call__(self, rawSuite: t.Any) -> pycritic.Suite:
		self.validateRawSuite(rawSuite)
		


	def validateRawSuite(self, rawSuite: t.Any) -> None:
		jsonschema.validate(rawSuite, self.__schema)



class CriterionConverter(ABC):
	@abstractmethod
	def __call__(self, rawCriterion: t.Any) -> pycritic.Criterion:
		pass



class BasicCriterionConverter(CriterionConverter)


def makeCriterion(rawCriterion: t.Any) -> pycritic.Criterion:
	estimation = rawCriterion["est"]
	


VAR_REGEX = re.compile("^\\$([A-Za-z_][A-Za-z0-9_]*)$")



def makeCondition(rawCondition: t.Any) -> pycritic.Condition:
	if isinstance(rawCondition, str):
		matchResult = VAR_REGEX.match(rawCondition)
		if matchResult:
			varname = matchResult.group(1)
			return pycritic.VariableCondition(varname)
	if isinstance(rawCondition, t.Mapping):

	return pycritic.LiteralCondition(rawCondition)
