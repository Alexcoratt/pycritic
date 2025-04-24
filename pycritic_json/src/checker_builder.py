from abc import ABC, abstractmethod
import typing as t

import pycritic
from data_loader import CheckerDataLoader



class JsonCheckerBuilder(ABC):
	@abstractmethod
	def __call__(self, raw: t.Any) -> pycritic.Checker:
		pass



class BasicJsonCheckerBuilder(JsonCheckerBuilder):
	def __init__(
		self,
		dataLoaderBuilder: t.Callable[[t.Any], CheckerDataLoader]
	) -> None:
		self.__dataLoaderBuilder = dataLoaderBuilder


	def __call__(self, raw: t.Any) -> pycritic.Checker:
		dataLoader = self.__dataLoaderBuilder(raw)
		varName = dataLoader.loadArgName()
		condition = dataLoader.loadCondition()
		return pycritic.VarChecker(varName, condition)
