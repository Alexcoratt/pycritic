import pytest

import pycritic
from pycritic_json import makeDefaultJsonSuiteBuilder



@pytest.fixture
def suiteBuilder():
	return makeDefaultJsonSuiteBuilder()



RAW_SAMPLE_SUITE = [
	{
		"est": {
			"mark": 5,
			"comment": "High quality goods and fast delivery. Just flawless"
		},
		"cond": [
			{
				"arg": "delivery_time",
				"func": "le",
				"example": 30
			},
			{
				"arg": "quality",
				"func": "eq",
				"example": 5
			},
			{
				"arg": "package",
				"func": "eq",
				"example": 5
			},
			{
				"arg": "courier_politeness",
				"func": "ge",
				"example": 4
			}
		]
	},
	{
		"est": {
			"mark": 4,
			"comment": "Good quality and delivery. Well done!"
		},
		"cond": [
			{
				"arg": "delivery_time",
				"func": "xfit",
				"min": 0,
				"max": 45
			},
			{
				"arg": "quality",
				"func": "ge",
				"example": 4
			},
			{
				"arg": "package",
				"func": "ge",
				"example": 3
			},
			{
				"arg": "courier_politeness",
				"func": "ge",
				"example": 4
			}
		]
	},
	{
		"est": {
			"mark": 4,
			"comment": "Rude courier"
		},
		"cond": [
			{
				"arg": "delivery_time",
				"func": "le",
				"example": 30
			},
			{
				"arg": "quality",
				"func": "ge",
				"example": 5
			},
			{
				"arg": "package",
				"func": "ge",
				"example": 4
			},
			{
				"arg": "courier_politeness",
				"func": "le",
				"example": 3
			}
		]
	},
	{
		"est": {
			"mark": 3,
			"comment": "Discount carries"
		},
		"cond": [
			{
				"arg": "discount_ratio",
				"func": "ge",
				"example": .15
			}
		]
	},
	{
		"est": {
			"mark": 1,
			"comment": "I'm disappointed!"
		}
	}
]



@pytest.fixture
def sampleSuite(suiteBuilder):
	return suiteBuilder(RAW_SAMPLE_SUITE)

	

@pytest.mark.parametrize("delivery,expected", (
	(
		{
			"delivery_time": 25,
			"quality": 4,
			"package": 5,
			"courier_politeness": 5,
			"discount_ratio": 0
		},
		4
	),
	(
		{
			"delivery_time": 90,
			"quality": 3,
			"package": 3,
			"courier_politeness": 4,
			"discount_ratio": .05
		},
		1
	),
	(
		{
			"delivery_time": 90,
			"quality": 3,
			"package": 3,
			"courier_politeness": 4,
			"discount_ratio": .15
		},
		3
	),
	(
		{
			"delivery_time": 29,
			"quality": 5,
			"package": 5,
			"courier_politeness": 5,
			"discount_ratio": .10
		},
		5
	)
))
def testCritic(delivery, expected, sampleSuite):
	est = sampleSuite(delivery)
	assert expected == est["mark"]
