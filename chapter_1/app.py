import json
from math import floor
from typing import Dict, Any


def statement(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:

    def usd(value: float) -> str:
        return f'${value/100:,.2f}'

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

    volume_credits: int = 0
    for perf in invoice["performances"]:
        volume_credits += volume_credits_for(perf)

    total_amount: int = 0
    result = f'Statement for {invoice["customer"]}\n'
    for perf in invoice["performances"]:
        result += f'    {play_for(perf)["name"]}: {usd(_amount_for(perf))} ({perf["audience"]} seats)\n'
        total_amount += _amount_for(perf)

    result += f'Amount owed is {usd(total_amount)}\n'
    result += f'You earned {volume_credits} credits\n'

    return result


def main():
    result = statement(
        json.load(open('data/invoices.json'))[0],
        json.load(open('data/plays.json')),
    )
    print(result)


if __name__ == '__main__':
    main()
