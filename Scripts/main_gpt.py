import pandas as pd
import numpy as np
import json
import time
import copy
import os

from Code.GeoData.GeoGuesser import GeoGeusser
from Code.LLM.Chatgpt import API

if __name__ == "__main__":
    if os.path.exists("ProcessedData/locations_gpt.csv"):
        info_csv = pd.read_csv("ProcessedData/locations_gpt.csv", index_col=False)
    else:
        info_csv = pd.read_csv("ProcessedData/location_with_states.csv")
        for i in [1, 2, 3]:
            info_csv[f"gpt_state{i}"] = None
            info_csv[f"gpt_x{i}"] = None
            info_csv[f"gpt_y{i}"] = None
        info_csv["name_pic"] = info_csv["name_pic"] - 1
        info_csv.to_csv("ProcessedData/locations_gpt.csv", index=False)
        info_csv = pd.read_csv("ProcessedData/locations_gpt.csv", index_col=False)

    geoguess = GeoGeusser()

    with open("Secrets/keys.json", "r") as f:
        api = API(json.loads(f.read())["chatgpt"])

    for n_row, row in info_csv.head(1000).iterrows():
        row = copy.deepcopy(row)
        if row.hasnans:
            row = row.to_dict()
            print(f"working on {row['name_pic']}")
            # answer = False
            try:
                answer = geoguess.locate_position_gpt(
                    f"Dataset/archive/dataset/{row['name_pic']}.png",
                    api,
                )
                if len(answer) != 3:
                    raise Exception("Answer not formatted accordignly to standard")
                for i, pred in enumerate(answer):
                    if isinstance(pred["coordinates"][0], list):
                        pred["coordinates"] = pred["coordinates"][0]
                    info_csv.loc[
                        info_csv["name_pic"] == row["name_pic"],
                        [f"gpt_state{i+1}", f"gpt_x{i+1}", f"gpt_y{i+1}"],
                    ] = [
                        pred["national_state"],
                        pred["coordinates"][0],
                        pred["coordinates"][1],
                    ]
            except Exception as e:
                try:
                    print(answer)
                except Exception as e:
                    print("answer is not defined")
            # print(info_csv.loc[info_csv["name_pic"] == row["name_pic"], :])
            info_csv.to_csv("ProcessedData/locations_gpt.csv", index=False)
            print(f'{row["name_pic"]} done')
            # time.sleep(5)
