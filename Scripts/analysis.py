import seaborn as sns
import pandas as pd
import numpy as np

from geopy import distance

import matplotlib.pyplot as plt


class Results:
    def __init__(self, model: str) -> None:
        self.model = model
        self.df = pd.read_csv(
            f"ProcessedData/locations_{self.model}.csv", index_col=False
        )
        self.df = self.df.dropna(how="any")
        print(self.df)

    def compute_min_distances(self, row: pd.Series):
        res = []
        for i in range(1, 4):
            try:
                res.append(
                    distance.geodesic(
                        (row["x"], row["y"]),
                        (row[f"{self.model}_x{i}"], row[f"{self.model}_y{i}"]),
                    ).km
                )
            except ValueError as e:
                print(f"Malformed input in {row['name_pic']}")
                continue
            except Exception as e:
                raise e
        if len(res) == 0:
            return None
        else:
            return min(res)

    def is_state_prediction_correct(self, row: pd.Series):
        res = False
        for i in range(1, 4):
            if row[f"{self.model}_state{i}"] == row["state"]:
                res = True
        return res


MODEL = "llava"
MODEL = "gpt"
if __name__ == "__main__":
    r_gpt = Results(MODEL)
    print(r_gpt.df.columns)
    res: pd.Series = r_gpt.df.apply(
        lambda row: r_gpt.compute_min_distances(row), axis=1
    ).dropna()
    print(res.mean(), res.std())
    print(res)
    for limit in [1, 25, 200, 750, 2500]:
        print(
            f"percentage of location less than {limit} : {len(res[res<limit])/len(res)}"
        )
    sol: pd.Series = r_gpt.df.apply(
        lambda row: r_gpt.is_state_prediction_correct(row), axis=1
    ).dropna()
    df = pd.DataFrame()
    df["dist"] = res
    df.loc[sol, ["State Prediction"]] = "Correct"
    df["State Prediction"] = df["State Prediction"].fillna("Not correct")

    print(df["dist"])
    print("Percentage of wrong answer that dist less than 750km from correct")
    print(
        len(df.loc[(df["State Prediction"] == "Correct") & (df["dist"] < 750)])
        / len(df.loc[(df["State Prediction"] == "Correct")])
    )
    print("Percentage of correct answer")
    print(len(df.loc[df["State Prediction"] == "Correct"]) / len(sol))
    print("Percentage answer less than 750km")
    print(len(df.loc[df["dist"] < 750]) / len(sol))
    print("Percentage of correct answer or less than 750km")
    print(
        len(df.loc[(df["dist"] < 750) | (df["State Prediction"] == "Correct")])
        / len(df)
    )

    plt.figure(figsize=(8, 5))
    ax1 = plt.subplot()
    sns.histplot(
        df,
        x="dist",
        hue="State Prediction",
        bins=30,
        hue_order=["Correct", "Not correct"],
        edgecolor="black",
        log_scale=True,
        ax=ax1,
        multiple="stack",
        legend=False,
    )
    ax1.set_xticklabels(
        ax1.get_xticklabels(),
        fontsize=22,
    )
    ax1.set_yticklabels(
        ax1.get_yticklabels(),
        fontsize=22,
    )
    if False:
        sns.move_legend(
            ax1,
            "lower center",
            bbox_to_anchor=(0.5, 1),
            ncol=2,
            title=None,
            fontsize="26",
            frameon=False,
        )
    plt.xlabel("Distance from correct solution (km)", fontdict={"size": 26})
    plt.ylabel("Count", fontdict={"size": 22})
    plt.xscale("log")
    plt.savefig(
        f"distances_{MODEL}.png",
        bbox_inches="tight",
    )
