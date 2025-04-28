import typing as t

import os
import logging
import json
import jsonschema

import pycritic
from pycritic import Estimation

from .criterion_builder import \
	CriterionBuilder, DefaultCriterionBuilder



class DefaultSuiteBuilder(CriterionBuilder[Estimation]):
	CRITERION_BUILDER = DefaultCriterionBuilder()
	CRITERIA_KEY = "crit"
	ESTIMAND_SCHEMA_KEY = "schema"

	SCHEMA_ENV_KEY = "PYCRITIC_SUITE_SCHEMA"
	DEFAULT_SCHEMA_FILENAME = "../schemas/suite.schema.json"


	def __init__(self) -> None:
		self.loadSchema()


	def loadSchema(self) -> None:
		filename = DefaultSuiteBuilder.getSchemaFilename()
		with open(filename) as file:
			self.__schema = json.load(file)


	@staticmethod
	def getSchemaFilename() -> str:
		try:
			return os.environ[DefaultSuiteBuilder.SCHEMA_ENV_KEY]
		except KeyError:
			dir = os.path.dirname(__file__)
			filename = os.path.join(dir, DefaultSuiteBuilder.DEFAULT_SCHEMA_FILENAME)
			logging.warning(f"using the default pycritic schema file: {filename}")
			return filename



	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		jsonschema.validate(raw, self.__schema)

		if not isinstance(raw, t.Mapping):
			raise TypeError("mapping expected")
		
		rawCriteria = raw[DefaultSuiteBuilder.CRITERIA_KEY]
		criteria = list(map(DefaultSuiteBuilder.CRITERION_BUILDER, rawCriteria))

		baseSuite = pycritic.Suite(criteria)

		try:
			schema = raw[DefaultSuiteBuilder.ESTIMAND_SCHEMA_KEY]
			validator = lambda raw: jsonschema.validate(raw, schema)
			return pycritic.ValidatingCriterion(baseSuite, validator)
		except KeyError:
			return baseSuite
