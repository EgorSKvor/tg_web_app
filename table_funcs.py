import pandas as pd
import json


def to_table(user_data):
    d_data = json.loads(user_data)
    df = pd.DataFrame.from_dict(d_data)
    df.to_excel('application_table.xlsx')
