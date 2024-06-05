from mpl_toolkits.basemap import Basemap
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


class WorldMap:

    def _init__(self, figsize: tuple[int, int] = (12, 6)):
        sns.set(style="whitegrid")

        # Crea una figura
        self.fig, self.ax = plt.subplots(figsize=figsize)

        # Crea una mappa globale
        self.mappa = Basemap(projection="mill", ax=self.ax)

        # Disegna coste e confini dei paesi
        self.mappa.drawcoastlines()
        self.mappa.drawcountries()

    def add_location(
        self, x, y, marker: str = "o", color: str = "red", markersize: int = 5
    ):
        x, y = self.mappa(y, x)
        self.mappa.plot(x, y, marker=marker, color=color, markersize=markersize)

    def save(self, folder_path: str, name: str, format: str = "png", dpi: int = 300):
        Path(folder_path).mkdir(exist_ok=True, parents=True)
        plt.savefig(f"{folder_path}/{name}.{format}", dpi=dpi)
        plt.close()
