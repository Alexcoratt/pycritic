from abc import ABC, abstractmethod
import typing as t



Estimand = t.Mapping[str, t.Any]
Condition = t.Callable[[t.Any], bool]



class Checker(ABC):
	@abstractmethod
	def __call__(self, estimand: Estimand) -> bool:
		pass



class SingleConditionChecker(Checker):
	def __init__(self, paramName: str, condition: Condition) -> None:
		self.__paramName = paramName
		self.__condition = condition
	

	def __call__(self, estimand: Estimand) -> bool:
		value = estimand[self.__paramName]
		return self.__condition(value)



class MultiConditionChecker(Checker):
	def __init__(
		self,
		paramName: str,
		conditions: t.Iterable[Condition]
	) -> None:
		self.__paramName = paramName
		self.__conditions = conditions


	def __call__(self, estimand: Estimand) -> bool:
		value = estimand[self.__paramName]
		return all(cond(value) for cond in self.__conditions)
