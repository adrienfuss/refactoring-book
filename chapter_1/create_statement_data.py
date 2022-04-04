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


def create_statement_data(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
    def play_for(perf):
        return plays[perf["playID"]]

    def _amount_for(a_performance):
        return PerformanceCalculator(a_performance, play_for(a_performance)).amount()

    def volume_credits_for(a_performance):
        result = 0

        # add volume credits
        result += max(a_performance['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == a_performance["play"]["type"]:
            result += floor(a_performance["audience"] / 5)
        return result

    def total_volume_credits(data):
        return sum(item["volume_credits"] for item in data["performances"])

    def total_amount(data):
        return sum(item["amount"] for item in data["performances"])

    def enrich_performance(a_performance):
        calculator = PerformanceCalculator(a_performance, play_for(a_performance))
        result = a_performance.copy()
        result['play'] = calculator.play
        result['amount'] = _amount_for(result)
        result['volume_credits'] = volume_credits_for(result)
        return result

    result = {}
    result['customer'] = invoice["customer"]
    result['performances'] = list(map(enrich_performance, invoice["performances"]))
    result['total_amount'] = total_amount(result)
    result['total_volume_credits'] = total_volume_credits(result)

    return result
