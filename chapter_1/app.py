import json
from math import floor
from typing import Dict, Any


def format_usd(value: float) -> str:
    return f'${value:,.2f}'


def statement(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
    total_amount: int = 0
    volume_credits: int = 0
    result = f'Statement for {invoice["customer"]}\n'

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
        volume_credits =0

        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == play_for(perf)["type"]:
            volume_credits += floor(perf["audience"] / 5)
        return volume_credits


    for perf in invoice["performances"]:
        volume_credits += volume_credits_for(perf)

        # print line for this order
        result += f'    {play_for(perf)["name"]}: {format_usd(_amount_for(perf) / 100)} ({perf["audience"]} seats)\n'
        total_amount += _amount_for(perf)
    result += f'Amount owed is {format_usd(total_amount / 100)}\n'
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