from abc import ABC, abstractmethod
import typing as t

import pycritic
from pycritic import Estimation

from .data_loader import CriterionDataLoader



class JsonCriterionBuilder(ABC, t.Generic[Estimation]):
	@abstractmethod
	def __call__(self, raw: t.Any) -> pycritic.Criterion[Estimation]:
		pass



class BasicJsonCriterionBuilder(JsonCriterionBuilder[Estimation]):
	def __init__(
		self,
		dataLoaderBuilder: t.Callable[[t.Any], CriterionDataLoader]
	) -> None:
		self.__dataLoaderBuilder = dataLoaderBuilder


	def __call__(self, raw: t.Any) -> pycritic.BasicCriterion[Estimation]:
		dataLoader = self.__dataLoaderBuilder(raw)
		estimation = dataLoader.loadEstimation()
		checkers = dataLoader.loadCheckers()
		return pycritic.BasicCriterion(estimation, checkers)
