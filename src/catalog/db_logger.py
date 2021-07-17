import os
import configparse
import pandas as pd


# This file is used to write the update logs in csv file to ensure fault tolerance and consistent systems
def db_log(query, field, item_number, value, i):
    # log update requests
    # print("Loggin errror__________")
    log = {'query': query, 'field': field, 'item_number': item_number, 'value': value}
    log = pd.DataFrame([log])

    if os.path.exists("db_logcatalog" + i + ".csv"):
        df = pd.read_csv("db_logcatalog" + i + ".csv", )
        df = df.append(log)
        df.to_csv("db_logcatalog" + i + ".csv", index=False)
        print("updated recovery log in :db_logcatalog" + i + ".csv")
    else:
        df = log.to_csv("db_logcatalog" + i + ".csv", index=False)
        print("created recovery log successfully:db_logcatalog" + i + ".csv", )
    return
