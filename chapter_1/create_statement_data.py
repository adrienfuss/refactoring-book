from math import floor
from typing import Dict, Any


class PerformanceCalculator:

    def __init__(self, a_performance, a_play):
        self.performance = a_performance
        self.play = a_play

    def amount(self):
        result = 0
        if self.play["type"] == "tragedy":
            result = 40000
            if self.performance["audience"] > 30:
                result += 1000 * (self.performance["audience"] - 30)
        elif self.play["type"] == "comedy":
            result = 30000
            if self.performance['audience'] > 20:
                result += 10000 + 500 * (self.performance["audience"] - 20)
            result += 300 * self.performance["audience"]
        else:
            raise Exception(f'Unknown type: {self.play["type"]}')
        return result

    def volume_credits(self):
        result = 0
        # add volume credits
        result += max(self.performance['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == self.play["type"]:
            result += floor(self.performance["audience"] / 5)
        return result


class TragedyCalculator(PerformanceCalculator):
    def __init__(self, a_performance, a_play):
        super().__init__( a_performance, a_play)


class ComedyCalculator(PerformanceCalculator):
    def __init__(self, a_performance, a_play):
        super().__init__( a_performance, a_play)

def create_performance_calculator(a_performance, a_play):
    if a_play["type"] == "tragedy":
        return TragedyCalculator(a_performance, a_play)
    elif a_play["type"] == "comedy":
        return ComedyCalculator(a_performance, a_play)
    else:
        raise Exception(f'Unknown type: {a_play["type"]}')


def create_statement_data(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
    def play_for(perf):
        return plays[perf["playID"]]

    def total_volume_credits(data):
        return sum(item["volume_credits"] for item in data["performances"])

    def total_amount(data):
        return sum(item["amount"] for item in data["performances"])

    def enrich_performance(a_performance):
        calculator = create_performance_calculator(a_performance, play_for(a_performance))
        result = a_performance.copy()
        result['play'] = calculator.play
        result['amount'] = calculator.amount()
        result['volume_credits'] = calculator.volume_credits()
        return result

    result = {}
    result['customer'] = invoice["customer"]
    result['performances'] = list(map(enrich_performance, invoice["performances"]))
    result['total_amount'] = total_amount(result)
    result['total_volume_credits'] = total_volume_credits(result)

    return result
