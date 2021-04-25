import db
from optparse import OptionParser
import json

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

    # allowed_operations = ['CREATE', 'DEPOSIT', 'WITHDRAW', 'TRANSFER', 'LIST', 'HISTORY']
    allowed_currencies = ['PLN', 'USD', 'EUR']

    if options.currency and options.currency.upper() not in allowed_currencies:
        parser.print_help()
        exit()

    if options.operation.upper() == "CREATE":
        if options.currency:
            db.create_jar(options.currency.upper())
        else:
            db.create_jar()

    elif options.operation.upper() == "DEPOSIT":
        if options.amount and options.jar_id and len(options.jar_id) == 24:
            jar = db.get_jar(options.jar_id)
            if options.currency:
                if jar[0]['currency'] == options.currency.upper():
                    db.deposit(options.jar_id, abs(options.amount))
                else:
                    print("Currency do not match currency of destination account")
            elif not jar[0]['currency']:
                db.deposit(options.jar_id, abs(options.amount))
            else:
                print("Currency do not match currency of destination account")
        else:
            parser.print_help()

    elif options.operation.upper() == "WITHDRAW":
        if options.amount and options.jar_id and len(options.jar_id) == 24:
            db.withdraw(options.jar_id, abs(options.amount))
        else:
            parser.print_help()
    elif options.operation.upper() == "TRANSFER":
        if options.amount and options.source and options.destination and len(options.source) == 24 and len(
                options.destination) == 24:
            source_jar = db.get_jar(options.source)
            dest_jar = db.get_jar(options.destination)
            if source_jar[0]['currency'] == dest_jar[0]['currency']:
                db.transfer(options.source, options.destination, abs(options.amount))
            else:
                print("Accounts have different currencies. Operation Canceled")
    elif options.operation.upper() == "LIST":
        print(db.get_jar())
    elif options.operation.upper() == "HISTORY":
        if options.jar_id and len(options.jar_id) == 24:
            hist_data = db.get_history(options.jar_id)
        else:
            hist_data = db.get_history(options.jar_id)

        if options.order_by:
            sorted_hist_data = sorted(hist_data, key=lambda i: i[options.order_by.lower()], reverse=options.desc)
            print(json.dumps(sorted_hist_data))
        else:
            print(json.dumps(hist_data))
    else:
        parser.print_help()
