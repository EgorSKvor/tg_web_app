import pandas as pd
import json


def to_table(user_data):
    df = pd.DataFrame(json.loads(user_data))
    df.to_excel('application_table.xlsx')
