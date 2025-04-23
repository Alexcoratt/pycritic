from abc import ABC, abstractmethod
import typing as t
from .checker import Estimand, Checker



Estimation = t.TypeVar("Estimation")



class Criterion(ABC, t.Generic[Estimation]):
	@abstractmethod
	def __call__(self, estimand: Estimand) -> Estimation:
		pass



class BasicCriterion(Criterion[Estimation]):
	def __init__(
		self,
		estimation: Estimation,
		checkers: t.Iterable[Checker] = []
	) -> None:
		self.estimation = estimation
		self.checkers = checkers


	def __call__(self, estimand: Estimand) -> Estimation:
		assert all(checker(estimand) for checker in self.checkers)
		return self.estimation



class Suite(Criterion[Estimation]):
	def __init__(self, criteria: t.Iterable[Criterion]) -> None:
		self.criteria = criteria


	def __call__(self, estimand: Estimand) -> Estimation:
		for crit in self.criteria:
			try:
				return crit(estimand)
			except AssertionError:
				pass
		raise AssertionError
