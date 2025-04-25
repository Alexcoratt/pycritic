from abc import ABC, abstractmethod
import typing as t

import pycritic
from pycritic import Estimation

from .checker_builder import DefaultCheckerBuilder



class CriterionBuilder(ABC, t.Generic[Estimation]):
	@abstractmethod
	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		pass



class ValidatingCriterionBuilder(
	CriterionBuilder[Estimation]
):
	def __init__(
		self,
		criterionBuilder: CriterionBuilder[Estimation],
		validator: t.Callable[[t.Any], None]
	) -> None:
		self.__criterionBuilder = criterionBuilder
		self.__validator = validator


	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		self.__validator(raw)
		return self.__criterionBuilder(raw)



class DefaultCriterionBuilder(CriterionBuilder):
	CHECKER_BUILDER = lambda paramName, rawConditions: \
		DefaultCheckerBuilder(paramName)(rawConditions)
	ESTIMATION_KEY = "est"
	CHECKERS_KEY = "cond"


	def __call__(self, raw: t.Any) -> pycritic.Criterion:
		if not isinstance(raw, t.Mapping):
			raise TypeError("mapping expected", raw)

		rawCheckers = raw.get(DefaultCriterionBuilder.CHECKERS_KEY, {})
		checkers = [
			DefaultCriterionBuilder.CHECKER_BUILDER(paramName, rawConditions)
			for paramName, rawConditions in rawCheckers.items()
		]

		estimation = raw[DefaultCriterionBuilder.ESTIMATION_KEY]
		return pycritic.BasicCriterion(estimation, checkers)
