# Jars
Options:
  -h, --help            show this help message and exit
  -o OPERATION, --operation=OPERATION
                        [CREATE|DEPOSIT|WITHDRAW|TRANSFER|LIST|HISTORY]
  -j JAR_ID, --jar=JAR_ID
                        id of the jar for
  -a AMOUNT, --amount=AMOUNT
                        Amount of funds for specified operation
  -s SOURCE, --source=SOURCE
                        Source jar for funds transfer
  -d DESTINATION, --destination=DESTINATION
                        Destination jar for funds transfer
  -c CURRENCY, --currency=CURRENCY
                        PLN|USD|EUR
  --order_by=ORDER_BY   |ID|OPERATION|AMOUNT
  --desc                Flag enables descending sorting


Żeby skrypt działał poprawnie, na maszynie lokalniej musi istnieć instancja mongoDb.
Założenie jest takie, że przy użyciu opcji TRANSFER używamy opcji --source i --destination a do DEPOSIT|WITHDRAW|LIST|HISTORY opcji --jar.
