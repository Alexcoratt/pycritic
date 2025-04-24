from abc import ABC, abstractmethod
import typing as t

import pycritic
from pycritic import Estimation

from .checker_builder import JsonCheckerBuilder



class JsonCriterionBuilder(ABC, t.Generic[Estimation]):
	@abstractmethod
	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		pass



class BasicJsonCriterionBuilder(JsonCriterionBuilder[Estimation]):
	ESTIMATION_KEY = "est"
	CHECKERS_KEY = "cond"
	

	def __init__(
		self,
		estimationBuilder: t.Callable[[t.Any], Estimation],
		checkerBuilder: JsonCheckerBuilder
	) -> None:
		self.__estimationBuilder = estimationBuilder
		self.__checkerBuilder = checkerBuilder


	def __call__(self, raw: t.Any) -> pycritic.BasicCriterion[Estimation]:
		estimation = self.extractEstimation(raw)
		checkers = self.extractCheckers(raw)
		return pycritic.BasicCriterion(estimation, checkers)


	def extractEstimation(self, raw: t.Mapping[str, t.Any]) -> Estimation:
		rawEst = raw[BasicJsonCriterionBuilder.ESTIMATION_KEY]
		return self.__estimationBuilder(rawEst)

	
	def extractCheckers(self, raw: t.Mapping[str, t.Any]) \
		-> t.Iterable[pycritic.Checker]:
		rawCheckers = raw.get(BasicJsonCriterionBuilder.CHECKERS_KEY, [])
		return map(self.__checkerBuilder, rawCheckers)
