import geopandas as gpd
import xarray as xr
import pandas as pd

# 1. 加载 SHP 文件和 NetCDF 文件
city_boundaries = gpd.read_file('E:/data/2022年地市边界/shi2022.shp')
weather = xr.open_dataset('气象数据/weather2022.nc')

# 2. 将 NetCDF 转换为 DataFrame，并打印列名
weather_df = weather.to_dataframe().reset_index()
print("Weather DataFrame columns:", weather_df.columns)

# 将 DataFrame 转换为 GeoDataFrame，并设置坐标参考系统
geometry = gpd.points_from_xy(weather_df.longitude, weather_df.latitude)
weather_gdf = gpd.GeoDataFrame(weather_df, geometry=geometry)
weather_gdf.crs = "EPSG:4326"
weather_gdf = weather_gdf.to_crs(city_boundaries.crs)

print("CRS of city_boundaries:", city_boundaries.crs)
print("CRS of weather_gdf:", weather_gdf.crs)

# 3. 使用 geopandas.sjoin 进行空间匹配，并打印结果的列名
merged_data = gpd.sjoin(city_boundaries, weather_gdf, how='inner', op='intersects')
print("Merged data columns:", merged_data.columns)
