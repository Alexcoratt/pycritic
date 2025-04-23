from abc import ABC, abstractmethod
import typing as t
import inspect



Estimand = t.Mapping[str, t.Any]
Condition = t.Callable[[t.Any], bool]



class Checker(ABC):
	@abstractmethod
	def __call__(self, estimand: Estimand) -> bool:
		pass



class VarChecker(Checker):
	def __init__(self, varname: str, condition: Condition = bool) -> None:
		self.__varname = varname
		self.__condition = condition


	def __call__(self, estimand: Estimand) -> bool:
		value = self.getVarValue(estimand)
		return self.__condition(value)


	def getVarValue(self, estimand: Estimand) -> t.Any:
		return estimand[self.__varname]



class AutoFuncChecker(Checker):
	def __init__(self, func: t.Callable[..., t.Any]) -> None:
		self.__func = func

	
	def __call__(self, estimand: Estimand) -> bool:
		requiredParams = self.getRequiredParams(estimand)
		return self.__func(**requiredParams)


	def getRequiredParams(self, estimand: Estimand) -> t.Mapping[str, t.Any]:
		signature = inspect.signature(self.__func)
		paramNames = signature.parameters.keys()
		return {pname: estimand[pname] for pname in paramNames}
