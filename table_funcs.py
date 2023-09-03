import pandas as pd
import json
import csv


def to_csv(user_data):
    d_data = json.loads(user_data)
    # df = pd.DataFrame(columns=['FIO', 'NAPR', 'AGE', 'WHYYOU'])
    # df = pd.DataFrame()
    with open('application_table.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=d_data.keys())
        writer.writeheader()
        writer.writerow(d_data)


# def to_table(csv):
