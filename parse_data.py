import pandas as pd 
import pymongo


def load_data():
    # PARSE EXCEL DATA
    data = pd.read_excel("Interns_2025_SWIFT_CODES.xlsx")
    data = data.drop(columns = ["CODE TYPE", "TOWN NAME", "TIME ZONE"]) # DROP REDUNDANT COLUMNS
    colnames = ["countryISO2", "swiftCode", "bankName", "address", "countryName"]
    data.columns = colnames


    # CREATE MONGO DB DATABASE
    client = pymongo.MongoClient("mongodb://localhost:27017/") # default mongodb port
    database = client["swift_codes_db"]
    collections = database.list_collection_names()
    # Drop each collection
    for coll_name in collections:
        database.drop_collection(coll_name)
    # CREATE HEADQUARTER COLLECTION
    collection_banks = database['banks']
    collection_banks.delete_many({})
    data_dict = data.to_dict(orient='records')
    collection_banks.insert_many(data_dict)


