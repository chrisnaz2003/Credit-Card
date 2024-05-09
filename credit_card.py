"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys

#finds minimum payment
def get_min_payment(balance, fees):
    m = 0.02
    min_payment = (balance * m) + fees
    if min_payment < 25:
        return 25
    return min_payment
#calculates interest using the apr given
def interest_charged(balance, apr):
    a = apr / 100.0
    y = 365
    d = 30
    return (a / y) * balance * d
#sets payment counters to 0 then using a while loop to add to counters when needed
def remaining_payments(balance, apr, targetamount, credit_line, fees):
    payments_counter = 0
    over75_counter = 0
    over50_counter = 0
    over25_counter = 0

    while balance > 0:
        if targetamount is None:
            payment = get_min_payment(balance, fees)
        else:
            payment = max(targetamount, get_min_payment(balance, fees))

        interest = interest_charged(balance, apr)
        payment_for_balance = payment - interest

        if payment_for_balance < 0:
            print("The card cannot be paid off.")
            sys.exit()

        balance -= payment_for_balance
        #this is where it increases the counter if balance is over the percentage to show how many months
        if balance > 0.75 * credit_line:
            over75_counter += 1
        if balance > 0.50 * credit_line:
            over50_counter += 1
        if balance > 0.25 * credit_line:
            over25_counter += 1

        payments_counter += 1

    return payments_counter, over25_counter, over50_counter, over75_counter

def parse_args(args_list):
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type=float, help='The total amount of balance left on the credit account')
    parser.add_argument('apr', type=int, help='The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type=int, help='The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type=int, default=None, help='The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type=float, default=0, help='The fees that are applied monthly.')
    
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("Balance amount must be positive.")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100.")
    if args.credit_line < 1:
        raise ValueError("Credit line must be positive.")
    if args.payment is not None and args.payment < 0:
        raise ValueError("Number of payments per year must be positive.")
    if args.fees < 0:
        raise ValueError("Fees must be positive.")
    return args
#prints out information to user after they input parameters
def main(balance, apr, targetamount=None, credit_line=5000, fees=0):
    min_payment = get_min_payment(balance, fees)
    print(f"Your recommended starting minimum payment is ${min_payment:.2f}.")
    
    pays_minimum = True if targetamount is None else False
    
    if not pays_minimum and targetamount < min_payment:
        print("Your target payment is less than the minimum payment for this credit card.")
        sys.exit()
    
    total_payments, over25_counter, over50_counter, over75_counter = remaining_payments(balance, apr, targetamount, credit_line, fees)
    
    if pays_minimum:
        print(f"If you pay the minimum payments each month, you will pay off the balance in {total_payments} payments.")
    else:
        print(f"If you make payments of ${targetamount}, you will pay off the balance in {total_payments} payments.")
    
    return f"You will spend a total of {over25_counter} months over 25% of the credit line\n" \
           f"You will spend a total of {over50_counter} months over 50% of the credit line\n" \
           f"You will spend a total of {over75_counter} months over 75% of the credit line."

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    
    print(main(arguments.balance_amount, arguments.apr, credit_line=arguments.credit_line, targetamount=arguments.payment, fees=arguments.fees))

def name(name):
    pass
    
