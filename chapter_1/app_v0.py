import json
import os
from math import floor
from typing import Dict, Any


def format_usd(value: float) -> str:
    return f'${value:,.2f}'


def statement(invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
    total_amount: int = 0
    volume_credits: int = 0
    result = f'Statement for {invoice["customer"]}\n'

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = 0

        if play["type"] == "tragedy":
            this_amount = 40000
            if perf["audience"] > 30:
                this_amount += 1000 * (perf["audience"] - 30)
        elif play["type"] == "comedy":
            this_amount = 30000
            if perf['audience'] > 20:
                this_amount += 10000 + 500 * (perf["audience"] - 20)
            this_amount += 300 * perf["audience"]
        else:
            raise Exception(f'Unknown type: {play["type"]}')

        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)

        # add extra credits for every ten comedy attendees
        if 'comedy' == play["type"]:
            volume_credits += floor(perf["audience"] / 5)

        # print line for this order
        result += f'    {play["name"]}: {format_usd(this_amount / 100)} ({perf["audience"]} seats)\n'
        total_amount += this_amount
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