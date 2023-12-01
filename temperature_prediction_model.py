"""test python file for prediction
"""
import pandas as pd
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load your GeoJSON dataset
gdf = gpd.read_file('data/example_aggr_hexagon.geojson')

# Selecting the features and target variable
df = pd.DataFrame({
    'longitude': gdf['Lon'],
    'latitude': gdf['Lat'],
    'temperature': gdf['Ave temp annual_F'],
    'height_avg': gdf['centroid_stat_avg_height_area'],
    'terrain_mean': gdf['terrain_stat_mean']
})

# Drop the rows where at least one element is missing
DF_CLEANED = df.dropna()

# Selecting the features and target variable
X = DF_CLEANED[['longitude', 'latitude', 'height_avg', 'terrain_mean']]
y = DF_CLEANED['temperature']

model = KNeighborsRegressor()
scaler = StandardScaler()

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)


# Training the model
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Use model.predict([[longitude, latitude, height_avg, terrain_mean]])
# to make new predictions
