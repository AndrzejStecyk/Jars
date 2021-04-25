import pymongo
import datetime
from bson.objectid import ObjectId
from bson import errors as bson_errors

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['TestTask']


def add_hitory(source, dest, operation, amount):
    mycol = mydb["history"]
    data = {'source': source,
            'destination': dest,
            'operation': operation,
            'amount': amount,
            'date': datetime.datetime.now()}
    mycol.insert_one(data)


def create_jar(currency=None):
    mycol = mydb["jars"]
    id = mycol.insert_one({'balance': 0,
                           'currency': currency})
    add_hitory(None, str(id.inserted_id), "Creation", 0)
    return id.inserted_id


def deposit(jar_id, amount, transfer=False):
    mycol = mydb["jars"]
    jar = mycol.find_one(ObjectId(jar_id))
    final_amount = amount + jar['balance']
    mycol.find_one_and_update(
        {"_id": ObjectId(jar_id)},
        {"$set": {"balance": final_amount}
         }, upsert=True
    )
    if not transfer:
        add_hitory(None, jar_id, 'Deposit', amount)


def withdraw(jar_id, amount, transfer=False):
    mycol = mydb["jars"]
    try:
        jar = mycol.find_one(ObjectId(jar_id))
    except bson_errors.InvalidId:
        print("Invalid Jar ID")
        exit(-1)

    if jar['balance'] >= amount:
        final_amount = jar['balance'] - amount
        mycol.find_one_and_update(
            {"_id": ObjectId(jar_id)},
            {"$set": {"balance": final_amount}
             }, upsert=True
        )
        if not transfer:
            add_hitory(None, jar_id, 'Withdraw', amount)
    else:
        return "Jar has not enough funds. Operation is canceled"


def transfer(source, destination, amount):
    withdraw(source, amount, transfer=True)
    deposit(destination, amount, transfer=True)
    add_hitory(source, destination, "Transfer", amount)


def get_jar(jar_id=None):
    query = None
    mycol = mydb["jars"]
    list_of_jars = list()
    try:
        if jar_id:
            query = {'_id': ObjectId(jar_id)}
    except bson_errors.InvalidId:
        print("Invalid Jar ID")
        exit(-1)

    results = mycol.find(query)
    for x in results:
        list_of_jars.append({'id': str(x['_id']), 'balance': x['balance'], 'currency': x['currency']})
    return list_of_jars


def get_history(jar_id=None):
    query = None
    mycol = mydb["history"]
    history = list()
    if jar_id:
        query = {'$or': [{'destination': jar_id}, {'source': jar_id}]}

    results = mycol.find(query)

    for x in results:
        del x['_id']
        x['date'] = x['date'].strftime("%d-%b-%Y (%H:%M:%S.%f)")
        history.append(x)
    return history
