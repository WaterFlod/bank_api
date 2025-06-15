import os

import hashlib


def hash(account_id,amount,transaction_id,
        user_id,secret_key=os.getenv('HASH_SECRET_KEY')):
    hash_object = hashlib.sha256()
    data = str(account_id) + str(amount) + str(transaction_id) + str(user_id) + str(secret_key)
    hash_object.update(data.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def get_accounts(account_data, id_user):
    accounts = list()
    for account in account_data:
        if account.user_id == id_user:
            accounts.append(account)
    return accounts


def get_transactions(transaction_data, id_user):
    transactions = list()
    for transaction in transaction_data:
        if transaction.user_id == id_user:
            transactions.append(transaction)
    return transactions