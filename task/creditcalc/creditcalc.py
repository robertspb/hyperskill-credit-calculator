import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str)
parser.add_argument("--principal", type=int)
parser.add_argument("--payment", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
args = parser.parse_args()


def param_error():
    print('Incorrect parameters')


def param_check():
    param_count = sum(1 for i in vars(args).values() if i)
    if (not args.type or
            (args.type != 'diff' and args.type != 'annuity') or
            (args.type == 'diff' and args.payment) or
            not args.interest or
            (args.principal and args.principal <= 0) or
            (args.periods and args.periods <= 0) or
            (args.interest and args.interest <= 0) or
            (args.payment and args.payment <= 0) or
            param_count != 4):
        return param_error()
    else:
        calc_key = [i for i, val in vars(args).items() if val is None][0]
        calculate(calc_key)


def calculate(calc_key):
    interest = args.interest / (12 * 100)
    principal = args.principal
    payment = args.payment
    periods = args.periods
    if args.type == 'annuity':
        if calc_key == 'principal':
            principal = payment / (interest * math.pow(1 + interest, periods) / (math.pow(1 + interest, periods) - 1))
            print(f'Your credit principal = {principal}!')
            print(f'Overpayment = {payment * periods - principal}')
        elif calc_key == 'payment':
            payment = math.ceil(principal * interest * math.pow(1 + interest, periods) /
                                (math.pow(1 + interest, periods) - 1))
            print(f'Your annuity payment = {payment}!')
            print(f'Overpayment = {payment * periods - principal}')
        elif calc_key == 'periods':
            periods = math.ceil(math.log(payment / (payment - interest * principal), 1 + interest))
            years = periods // 12
            months = periods % 12
            if years >= 1 and months >= 1:
                print(f'You need {years} {"year" if years == 1 else "years"} and {months} '
                      f'{"month" if months == 1 else "months"} to repay this credit!')
            elif years >= 1 and months == 0:
                print(f'You need {years} {"year" if years == 1 else "years"} to repay this credit!')
            else:
                print(f'You need {months} {"month" if months == 1 else "months"} to repay this credit!')
            print(f'Overpayment = {periods * payment - principal}')
    elif args.type == 'diff':
        total_payments = 0
        for m in range(1, periods + 1):
            payment = math.ceil(principal / periods + interest * (principal - (principal * (m - 1)) / periods))
            total_payments += payment
            print(f'Month {m}: paid out {payment}')
        print()
        print(f'Overpayment = {total_payments - principal}')


param_check()

