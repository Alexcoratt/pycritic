from abc import ABC, abstractmethod
import typing as t

import functools
import re

import pycritic



class CheckerBuilder(ABC):
	@abstractmethod
	def __call__(self, raw: t.Any) -> pycritic.Checker:
		pass



def getComparator(sample: t.Any, func: t.Callable[[
	t.Any,	# argument
	t.Any	# sample
], bool]):
	def comparator(value: t.Any) -> bool:
		return func(value, sample)
	return comparator



class MatchCondition:
	def __init__(self, pattern: str) -> None:
		self.__regex = re.compile(pattern)


	def __call__(self, s: str) -> bool:
		matchResult = self.__regex.match(s)
		return bool(matchResult)



class DefaultCheckerBuilder(CheckerBuilder):
	CONDITION_BUILDER_MAPPING = {
		# binary comparison
		"lt": functools.partial(getComparator, func=lambda l, r: l < r),
		"le": functools.partial(getComparator, func=lambda l, r: l <= r),
		"gt": functools.partial(getComparator, func=lambda l, r: l > r),
		"ge": functools.partial(getComparator, func=lambda l, r: l >= r),
		"eq": functools.partial(getComparator, func=lambda l, r: l == r),
		"ne": functools.partial(getComparator, func=lambda l, r: l != r),

		# other
		"regex": MatchCondition
	}
	DEFAULT_CONDITION_BUILDER = CONDITION_BUILDER_MAPPING["eq"]


	def __init__(self, paramName: str) -> None:
		self.__paramName = paramName


	def __call__(self, raw: t.Any) -> pycritic.Checker:
		if isinstance(raw, t.Mapping):
			conditions = list(map(
				lambda item: DefaultCheckerBuilder.\
					CONDITION_BUILDER_MAPPING[item[0]](item[1]),
				raw.items()
			))
			return pycritic.MultiConditionChecker(self.__paramName, conditions)

		condition = DefaultCheckerBuilder.DEFAULT_CONDITION_BUILDER(raw)
		return pycritic.SingleConditionChecker(self.__paramName, condition)
