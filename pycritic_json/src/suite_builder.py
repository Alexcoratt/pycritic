import typing as t

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



class ValidatingJsonCriterionBuilder(
	JsonCriterionBuilder[Estimation]
):
	def __init__(
		self,
		criterionBuilder: JsonCriterionBuilder[Estimation],
		validator: t.Callable[[t.Any], None]
	) -> None:
		self.__criterionBuilder = criterionBuilder
		self.__validator = validator


	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		self.__validator(raw)
		return self.__criterionBuilder(raw)
