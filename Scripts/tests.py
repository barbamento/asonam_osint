from Code.GeoData.GeoLocation import GeoLocation

import pandas as pd

coord_1: tuple[int, int]
coord_2: tuple[int, int]

# print(geopy.distance.geodesic(coord_1, coord_2).km)
df = (
    pd.read_csv("Dataset/archive/coords.csv", header=None)
    .reset_index()
    .rename({"index": "name_pic", 0: "x", 1: "y"}, axis="columns")
)
df["name_pic"] = df["name_pic"] + 1
df["state"] = df.apply(
    lambda row: GeoLocation().locate_state(row["x"], row["y"]), axis=1
)
df.to_csv("ProcessedData/location_with_states.csv", index=False)
