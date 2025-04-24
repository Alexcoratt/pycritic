from abc import ABC, abstractmethod
import typing as t

import pycritic



class JsonCheckerBuilder(ABC):
	@abstractmethod
	def __call__(self, raw: t.Any) -> pycritic.Checker:
		pass



class BasicJsonCheckerBuilder(JsonCheckerBuilder):
	FUNCNAME_KEY = "func"
	VARNAME_KEY = "arg"


	def __init__(
		self,
		conditionMapping: t.Mapping[str, pycritic.Condition]
	) -> None:
		self.conditionMapping = conditionMapping


	def __call__(self, raw: t.Any) -> pycritic.Checker:
		if not isinstance(raw, t.Mapping):
			raise TypeError("mapping expected")

		varName = raw[BasicJsonCheckerBuilder.VARNAME_KEY]
		funcName = raw.get(BasicJsonCheckerBuilder.FUNCNAME_KEY)

		if funcName:
			func = self.conditionMapping[funcName]
			return pycritic.VarChecker(varName, func)
		return pycritic.VarChecker(varName)
