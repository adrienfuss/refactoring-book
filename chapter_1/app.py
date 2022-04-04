import json
from math import floor
from typing import Dict, Any


def statement(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
    def play_for(perf):
        return plays[perf["playID"]]

    def _amount_for(a_performance):
        result = 0
        if a_performance['play']["type"] == "tragedy":
            result = 40000
            if a_performance["audience"] > 30:
                result += 1000 * (a_performance["audience"] - 30)
        elif a_performance['play']["type"] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance["audience"] - 20)
            result += 300 * a_performance["audience"]
        else:
            raise Exception(f'Unknown type: {a_performance["play"]["type"]}')
        return result

    def volume_credits_for(a_performance):
        result = 0

        # add volume credits
        result += max(a_performance['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == a_performance["play"]["type"]:
            result += floor(a_performance["audience"] / 5)
        return result

    def total_volume_credits(data):
        volume_credits: int = 0
        for a_performance in data['performance']:
            volume_credits += a_performance['volume_credits']
        return volume_credits

    def total_amount(data):
        result: int = 0
        for a_performance in data['performance']:
            result += a_performance['amount']
        return result

    def enrich_performance(a_performance):
        result = a_performance.copy()
        result['play'] = play_for(result)
        result['amount'] = _amount_for(result)
        result['volume_credits'] = volume_credits_for(result)
        return result

    statement_data = {}
    statement_data['customer'] = invoice["customer"]
    statement_data['performance'] = list(map(enrich_performance, invoice["performances"]))
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(statement_data)
    result = render_plain_text(statement_data, plays)

    return result


def render_plain_text(data, plays):
    def usd(value: float) -> str:
        return f'${value / 100:,.2f}'

    result = f"Statement for {data['customer']}\n"
    for a_performance in data['performance']:
        result += f'    {a_performance["play"]["name"]}: {usd(a_performance["amount"])} ({a_performance["audience"]} seats)\n'
    result += f'Amount owed is {usd(data["total_amount"])}\n'
    result += f'You earned {data["total_volume_credits"]} credits\n'
    return result


def main():
    result = statement(
        json.load(open('data/invoices.json'))[0],
        json.load(open('data/plays.json')),
    )
    print(result)


if __name__ == '__main__':
    main()
