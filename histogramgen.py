

import pandas as pd


def get_histogram_as_json():

    ds = pd.read_csv("dataset_enhanced.csv")
    df = pd.DataFrame(ds)

    allops = set()

    d = dict()

    for index, row in df.iterrows():

        y = row["Year"]

        t = row["Time"]
        if pd.isna(t):
            continue
        hrs = int(t.split(":")[0])

        if y not in d:
            d[y] = {"Day": 0, "Night": 0}

        if 6 <= hrs <= 18:
            d[y]["Day"] += 1
        else:
            d[y]["Night"] += 1
    lst = []
    for k in sorted(d.keys()):
        d[k].update({"Year": str(k)})
        lst.append(d[k])

    return {"data": lst}


if __name__ == "__main__":
    get_histogram_as_json()
