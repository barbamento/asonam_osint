import pandas as pd
import numpy as np
import time
import copy
import os

from Code.GeoData.GeoGuesser import GeoGeusser


if __name__ == "__main__":
    if os.path.exists("ProcessedData/locations_llava.csv"):
        info_csv = pd.read_csv("ProcessedData/locations_llava.csv", index_col=False)
    else:
        info_csv = pd.read_csv("ProcessedData/location_with_states.csv")
        for i in [1, 2, 3]:
            info_csv[f"llava_state{i}"] = None
            info_csv[f"llava_x{i}"] = None
            info_csv[f"llava_y{i}"] = None
        info_csv["name_pic"] = info_csv["name_pic"] - 1
        info_csv.to_csv("ProcessedData/locations_llava.csv", index=False)
        info_csv = pd.read_csv("ProcessedData/locations_llava.csv", index_col=False)

    ##llava part
    geoguess = GeoGeusser()
    print(geoguess.locate_position_prompt)
    exit()

    for n_row, row in info_csv.iterrows():
        row = copy.deepcopy(row)
        if row.hasnans:
            row = row.to_dict()
            print(f"working on {row['name_pic']}")
            answer = False
            while not answer:
                try:
                    answer = geoguess.locate_position(
                        f"Dataset/archive/dataset/{row['name_pic']}.png"
                    )
                    try:
                        if len(answer) != 3:
                            raise Exception(
                                "Answer not formatted accordignly to standard"
                            )
                        for i, pred in enumerate(answer):
                            if isinstance(pred["coordinates"][0], list):
                                pred["coordinates"] = pred["coordinates"][0]
                            info_csv.loc[
                                info_csv["name_pic"] == row["name_pic"],
                                [f"llava_state{i+1}", f"llava_x{i+1}", f"llava_y{i+1}"],
                            ] = [
                                pred["national_state"],
                                pred["coordinates"][0],
                                pred["coordinates"][1],
                            ]
                    except Exception as e:
                        print(answer)
                        raise Exception(f"error in handling answer")
                except Exception as e:
                    print(e)
                    answer = False
                    time.sleep(5)

            # print(info_csv.loc[info_csv["name_pic"] == row["name_pic"], :])
            info_csv.to_csv("ProcessedData/locations_llava.csv", index=False)
            print(f'{row["name_pic"]} done')
            # time.sleep(5)
