from abc import ABC, abstractmethod
import typing as t

import pycritic
from pycritic import Estimation



class CheckerDataLoader(ABC):
	@abstractmethod
	def loadCondition(self) -> pycritic.Condition:
		pass

	@abstractmethod
	def loadArgName(self) -> str:
		pass



class CriterionDataLoader(ABC, t.Generic[Estimation]):
	@abstractmethod
	def loadEstimation(self) -> Estimation:
		pass


	@abstractmethod
	def loadCheckers(self) -> t.Iterable[pycritic.Checker]:
		pass
