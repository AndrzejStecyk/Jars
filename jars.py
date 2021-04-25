import db
from optparse import OptionParser
import json


def create_a_jar(currency):
    if currency:
        db.create_jar(currency.upper())
    else:
        db.create_jar()


def make_a_deposit(jar_id, amount, currency):
    if amount and jar_id and len(jar_id) == 24:
        jar = db.get_jar(jar_id)
        try:
            if currency:
                if jar[0]['currency'] == currency.upper():
                    db.deposit(jar_id, abs(amount))
                    print("Deposit successful")
                else:
                    print("Currency do not match currency of destination account")
            elif not jar[0]['currency']:
                db.deposit(jar_id, abs(amount))
                print("Deposit successful")
            else:
                print("Currency do not match currency of destination account")
        except IndexError:
            print("Jar ID does not exist")
    else:
        parser.print_help()


def make_a_withdraw(jar_id, amount):
    if amount and jar_id and len(jar_id) == 24:
        db.withdraw(jar_id, abs(amount))
        print("Withdraw successful")
    else:
        parser.print_help()


def make_a_transfer(source, destination, amount):
    if amount and source and destination and len(source) == 24 and len(
            destination) == 24:
        source_jar = db.get_jar(source)
        dest_jar = db.get_jar(destination)
        try:
            if source_jar[0]['currency'] == dest_jar[0]['currency']:
                db.transfer(source, destination, abs(amount))
                print("Transfer successful")
            else:
                print("Accounts have different currencies. Operation Canceled")
        except IndexError:
            print("Jar ID does not exist")


def show_history(jar_id, order_by, desc):
    if jar_id and len(jar_id) == 24:
        hist_data = db.get_history(jar_id)
    else:
        hist_data = db.get_history(jar_id)

    if order_by:
        sorted_hist_data = sorted(hist_data, key=lambda i: i[order_by.lower()], reverse=desc)
        print(json.dumps(sorted_hist_data))
    else:
        print(json.dumps(hist_data))


if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-o", "--operation", dest="operation", type=str,
                      help="[CREATE|DEPOSIT|WITHDRAW|TRANSFER|LIST|HISTORY]")

    parser.add_option("-j", "--jar", dest="jar_id", type=str,
                      help="id of the jar for", default=False)

    parser.add_option("-a", "--amount", dest="amount", type=int,
                      help="Amount of funds for specified operation")

    parser.add_option("-s", "--source", dest="source", type=str,
                      help="Source jar for funds transfer")

    parser.add_option("-d", "--destination", dest="destination", type=str,
                      help="Destination jar for funds transfer")

    parser.add_option("-c", "--currency", dest="currency", type=str,
                      help="PLN|USD|EUR")

    parser.add_option("--order_by", dest="order_by", type=str,
                      help="|ID|OPERATION|AMOUNT")

    parser.add_option("--desc", dest="desc", action="store_true", default=False,
                      help="Flag enables descending sorting")

    (options, args) = parser.parse_args()

    if not options.operation:
        parser.print_help()
        exit()

    allowed_currencies = ['PLN', 'USD', 'EUR']
    allowed_order_by = ['ID', 'OPERATION', 'AMOUNT']

    if options.currency and options.currency.upper() not in allowed_currencies:
        parser.print_help()
        exit()
    if options.order_by and options.order_by.upper() not in allowed_order_by:
        parser.print_help()
        exit()

    if options.operation.upper() == "CREATE":
        create_a_jar(options.currency)

    elif options.operation.upper() == "DEPOSIT":
        make_a_deposit(options.jar_id, options.amount, options.currency)

    elif options.operation.upper() == "WITHDRAW":
        make_a_withdraw(options.jar_id, options.amount)

    elif options.operation.upper() == "TRANSFER":
        make_a_transfer(options.source, options.destination, options.amount)

    elif options.operation.upper() == "LIST":
        print(json.dumps(db.get_jar()))

    elif options.operation.upper() == "HISTORY":
        show_history(options.jar_id, options.order_by, options.desc)
    else:
        parser.print_help()
