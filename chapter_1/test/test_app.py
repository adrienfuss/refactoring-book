import json

from chapter_1.statement import statement


def test_check_main_output():
    expected_output = '''
                        Statement for BigCo
                            Hamlet: $650.00 (55 seats)
                            As You Like It: $580.00 (35 seats)
                            Othello: $500.00 (40 seats)
                         Amount owed is $1,730.00
                        You earned 47 credits
                        '''

    result = statement(
        json.load(open('resources/invoices.json'))[0],
        json.load(open('resources/plays.json')),
    )

    assert result.split() == expected_output.split()
