import json
from math import floor
from typing import Dict, Any


def statement(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:

    def enrich_performance(perf):
        result =perf.copy()
        return result

    statement_data = {}
    statement_data['customer'] = invoice["customer"]
    statement_data['performance'] = invoice["performances"]
    result = render_plain_text(statement_data, plays)

    return result


def render_plain_text(data, plays):
    def usd(value: float) -> str:
        return f'${value / 100:,.2f}'

    def _amount_for(perf):
        result = 0
        if play_for(perf)["type"] == "tragedy":
            result = 40000
            if perf["audience"] > 30:
                result += 1000 * (perf["audience"] - 30)
        elif play_for(perf)["type"] == "comedy":
            result = 30000
            if perf['audience'] > 20:
                result += 10000 + 500 * (perf["audience"] - 20)
            result += 300 * perf["audience"]
        else:
            raise Exception(f'Unknown type: {play_for(perf)["type"]}')
        return result

    def play_for(perf):
        return plays[perf["playID"]]

    def volume_credits_for(perf):
        result = 0

        # add volume credits
        result += max(perf['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == play_for(perf)["type"]:
            result += floor(perf["audience"] / 5)
        return result

    def total_volume_credits():
        volume_credits: int = 0
        for perf in data['performance']:
            volume_credits += volume_credits_for(perf)
        return volume_credits

    def total_amount():
        result: int = 0
        for perf in data['performance']:
            result += _amount_for(perf)
        return result

    result = f"Statement for {data['customer']}\n"
    for perf in data['performance']:
        result += f'    {play_for(perf)["name"]}: {usd(_amount_for(perf))} ({perf["audience"]} seats)\n'
    result += f'Amount owed is {usd(total_amount())}\n'
    result += f'You earned {total_volume_credits()} credits\n'
    return result


def main():
    result = statement(
        json.load(open('data/invoices.json'))[0],
        json.load(open('data/plays.json')),
    )
    print(result)


if __name__ == '__main__':
    main()
