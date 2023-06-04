import subprocess
"""
# Install GeoPandas
subprocess.check_call(["pip", "install", "geopandas"])
subprocess.check_call(['pip', 'install', 'pycountry'])
#
subprocess.check_call(["pip", "install", "numpy"])
subprocess.check_call(["pip", "install", "pandas"])
subprocess.check_call(["pip", "install", "matplotlib"])
subprocess.check_call(["pip", "install", "geopy"])
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import pycountry
import plotly.express as px



df = pd.read_excel("/Users/wei/Python/MPHDissertation/test_file/19_ratified_country_15 May 2023.xlsx")
# 讀取世界地圖的shapefile
world_map = gpd.read_file(
    '/Users/wei/UCD-MPH/MPH Lecture/MPH Dissertation/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

# 繪製世界地圖
world_map.plot()
merged_map = world_map.merge(df, left_on='name', right_on='Country Name')

# 显示带有数据的地图
merged_map.plot(column='CVD mortality rate in Female (%)', legend=True)

plt.show()
