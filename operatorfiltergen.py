

import pandas as pd


def get_operators_as_json():

    results = {}

    ds = pd.read_csv("dataset_enhanced.csv", usecols=(
        "Operator", "Year", "Ground"))
    df = pd.DataFrame(ds).fillna(0)

    tot = 0
    for index, row in df.iterrows():
        op = str(row["Operator"])
        y = str(row['Year'])
        if op == None:
            continue

        if op not in results:
            results[op] = {"Crashes": {}}
        if y not in results[op]['Crashes']:
            results[op]['Crashes'][y] = 0
        results[op]["Crashes"][y] += 1
        tot += 1

    ret = {"data": []}

    for comp in results:
        sorted_years = []
        for year in results[comp]['Crashes']:
            sorted_years.append(year)
        sorted_years = sorted(sorted_years)

        first = [sorted_years[0], results[comp]['Crashes'][sorted_years[0]]]
        obj = {'Company': comp, 'Crashes': [first]}
        for i, y in enumerate(sorted_years[1:]):
            obj['Crashes'].append([y, results[comp]['Crashes'][y] + obj['Crashes'][-1][1]])
        
        ret['data'].append(obj)

    ret['data'] = sorted(ret['data'], key=lambda x: x['Crashes'][-1][1])

    return ret


if __name__ == "__main__":
    a = get_operators_as_json()
