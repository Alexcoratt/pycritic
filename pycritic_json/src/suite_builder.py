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
	"""Default suite builder
	
	The suite builder which is used by default
	"""

	CRITERION_BUILDER = DefaultCriterionBuilder()
	"""Criterion builder"""

	CRITERIA_KEY = "crit"
	"""Key of the criteria parameter in a config"""

	ESTIMAND_SCHEMA_KEY = "schema"
	"""Key of the schema parameter in a config"""

	SCHEMA_ENV_KEY = "PYCRITIC_SUITE_SCHEMA"
	"""Key of the environmental variable storing path to a schema for a suite"""

	DEFAULT_SCHEMA_FILENAME = "../schemas/suite.schema.json"
	"""Default relative path to a schema for a suite"""


	def __init__(self) -> None:
		self.loadSchema()


	def loadSchema(self) -> None:
		"""Load a JSON schema"""
		filename = DefaultSuiteBuilder.getSchemaFilename()
		with open(filename) as file:
			self.__schema = json.load(file)


	@staticmethod
	def getSchemaFilename() -> str:
		"""Get a filepath to a schema
		
		:return: Filepath to a schema
		:rtype: str
		"""
		try:
			return os.environ[DefaultSuiteBuilder.SCHEMA_ENV_KEY]
		except KeyError:
			dir = os.path.dirname(__file__)
			filename = os.path.join(dir, DefaultSuiteBuilder.DEFAULT_SCHEMA_FILENAME)
			logging.warning(f"using the default pycritic schema file: {filename}")
			return filename



	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		"""
		
		Validates the parameter value using the schema and decides which one criterion to create

		:param raw: A raw data to convert
		:type raw: typing.Any
		"""
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
