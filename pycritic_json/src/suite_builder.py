import typing as t
import jsonschema

import pycritic
from pycritic import Estimation

from .criterion_builder import JsonCriterionBuilder



class BasicJsonSuiteBuilder(JsonCriterionBuilder[Estimation]):
	def __init__(
		self,
		criterionBuilder: JsonCriterionBuilder[Estimation]
	) -> None:
		self.__critierionBuilder = criterionBuilder


	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		if not isinstance(raw, t.Iterable):
			raise TypeError("iterable expected")
		criteria = map(self.__critierionBuilder, raw)
		return pycritic.Suite(criteria)



class JsonSchemaValidatingJsonCriterionBuilder(
	JsonCriterionBuilder[Estimation]
):
	def __init__(
		self,
		baseBuilder: JsonCriterionBuilder[Estimation],
		schema: t.Any
	) -> None:
		self.__baseBuilder = baseBuilder
		self.__schema = schema


	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		jsonschema.validate(raw, self.__schema)
		return self.__baseBuilder(raw)
