

import pandas as pd


def get_operators_as_json():

    results = {}

    ds = pd.read_csv("dataset_enhanced.csv", usecols=(
        "Operator", "Aboard", "Fatalities", "Ground"))
    df = pd.DataFrame(ds).fillna(0)

    for index, row in df.iterrows():
        op = str(row["Operator"])
        if op == None:
            continue

        a = float(row["Aboard"])
        f = float(row["Fatalities"])
        g = float(row["Ground"])

        if op not in results:
            results[op] = {"Crashes": 0}
        # results[op]["Aboard"] += a
        # results[op]["Fatalities"] += f
        # results[op]["Ground"] += g
        results[op]["Crashes"] += 1

    ret = {"data": []}

    for key, value in results.items():
        ret["data"].append({"Company": key, "Crashes": value["Crashes"]})

    ret["data"] = sorted(ret["data"], key=lambda x: x["Crashes"])
    print(len(ret["data"]))
    return ret


if __name__ == "__main__":
    a = get_operators_as_json()
    print(a)
