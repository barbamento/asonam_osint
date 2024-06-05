import geopandas as gpd
from shapely.geometry import Point


class GeoLocation:
    filepath = "Dataset/Maps/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp"

    def __init__(self) -> None:
        self.gdf = gpd.read_file(self.filepath)

    def locate_state(self, lat, lon):
        point = Point(lon, lat)

        for _, row in self.gdf.iterrows():
            if row["geometry"].contains(point):
                return row["NAME"]

        return "Paese non trovato"
