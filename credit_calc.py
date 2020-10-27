"""
Credit payment calculator
"""

import math


def get_user_input():
    """
    Get and check user input.
    :returns: dict with 'amount', 'interest', 'downpayment', 'term'
    """
    check_items = {'amount': int, 'interest': str, 'downpayment': int, 'term': int}
    user_input = {}
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break

        line_split = line.split(':')
        if line_split[0] not in check_items:
            raise Exception('Incorrect key user input', line_split[0])
        try:
            # Check inputted value
            user_input[line_split[0]] = check_items[line_split[0]](line_split[1].strip())
        except ValueError:
            raise Exception('Incorrect value user inputted:', line_split)

    # Check user_input['interest'] value
    if not user_input['interest'].endswith('%'):
        raise Exception('Incorrect value user inputted:', user_input['interest'])
    try:
        user_input['interest'] = float(user_input['interest'][:-1])
    except ValueError:
        raise Exception('Incorrect value user inputted:', user_input['interest'])

    # Check all keys are present
    if not set(check_items.keys()).issubset(user_input.keys()):
        raise Exception('Incorrect keys user inputted')

    return user_input


def calculations(data):
    """
    Return result of credit calculations
    :param data: dict with 'amount', 'interest', 'downpayment', 'term'
    :returns: dict with 'interval_payment', 'interest_paid', 'total_paid'
    """
    loan = data['amount'] - data['downpayment']
    interest = data['interest'] / 100
    eir = (math.pow(1 + interest / 2, 1 / 6) - 1) * 12
    num_intervals = 12 * data['term']
    interval_rate = eir * data['term'] / num_intervals
    z = 1 + interval_rate
    interval_payment = (loan * math.pow(z, num_intervals) * interval_rate) / (math.pow(z, num_intervals) - 1)
    total_paid = data['downpayment'] + interval_payment * num_intervals

    debt = abs(
        loan * math.pow(z, num_intervals) - interval_payment * ((math.pow(z, num_intervals) - 1) / interval_rate))
    equity = loan - debt
    interest_paid = num_intervals * interval_payment - equity
    return {'interval_payment': interval_payment, 'interest_paid': interest_paid, 'total_paid': total_paid}


def main():
    user_data = get_user_input()
    calcs = calculations(user_data)
    print('Месячная выплата по кредиту: {:,.2f}'.format(calcs['interval_payment']))
    print('Общий объём начисленных процентов: {:,.0f}'.format(calcs['interest_paid']))
    print('Общая сумма выплаты: {:,.0f}'.format(calcs['total_paid']))


if __name__ == '__main__':
    main()
