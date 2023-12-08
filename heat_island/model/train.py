"""This module is to train KNN regression
and optimize the best k hyperparameter
"""
import os.path
import joblib
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
# from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
# from heat_island.data_process import input_file_from_data_dir


def get_keys():
    """Default keys for datafile might be subjected to change

    Returns:
        list: list of default keys for features
    """
    centroid = 'centroid_stat_'
    terrain = 'terrain_stat_'
    # Add or change what features to use or don't use here
    features = ['Lat', 'Lon', 'Elev (m.)',
                centroid+'mean', centroid+'std_dev', centroid+'min',
                centroid+'25%', centroid+'50%', centroid+'75%', centroid+'max',
                terrain+'mean', terrain+'std_dev', terrain+'min',
                terrain+'25%', terrain+'50%', terrain+'75%', terrain+'max'
                ]
    return features


def main(data_path: str, features: list = None,
         target: str = 'Ave temp annual_F',
         save_path: str = '', fname: str = 'model.bin'):
    """Main function for training model

    Args:
        data_path (str): path to training dataset
        features (list, optional): features keys
        if empty default keys will be used. Defaults to [].
        target (str, optional): key or column name of the target.
        Defaults to 'Ave temp annual_F'.
        save_path (str, optional): save directory. Defaults to ''.
        fname (str, optional): name of the save file. Defaults to 'model.bin'.
    """
    if features is None:
        features = get_keys()
    x, y = clean_data(data_path, features, target)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,
                                                        random_state=0)
    scale = StandardScaler()
    scale.fit(x_train)
    # Change here if performance is bad
    model = KNeighborsRegressor()
    # model = LinearRegression()
    model.fit(scale.transform(x_train), y_train)
    print("Training successful")
    train_score = model.score(x_train, y_train)
    print(f"Your train score is {train_score}")
    test_score = model.score(x_test, y_test)
    print(f'Your test score is {test_score}')
    save_model(model, scale, save_path, fname)


def predict(model, scale, raw_x):
    """predict function for the model

    Args:
        model (Regressor model): model instance for prediction
        scale (Standard scaler): Scaler for the model
        raw_x (dataframe): dataframe of features

    Returns:
        pandas series: A predicted value/series based on raw_x
    """
    x_std = scale.transform(raw_x)
    y_pred = model.predict(x_std)
    return y_pred


def clean_data(data_path: str, features: list, target: str):
    """Read data from file and clean all na value for next process

    Args:
        data_path (str): path to data file (.geojson)
        features (list): list of features
        target (str): key for output
        idx (str): Weather station identifier

    Raises:
        KeyError: Unexpect .geojson file structure

    Returns:
        dataframe: cleaned feature dataframe
        dataframe: cleaned output dataframe
    """
    if data_path[data_path.rfind('.')+1:] != 'geojson':
        raise ValueError("Incorrect file format: Expect '.geojson'")
    gdf = gpd.read_file(data_path)
    all_col = features+[target]
    if not all(col in gdf.columns for col in all_col):
        raise KeyError("Incorrect dataset format")
    gdf = gdf[all_col].dropna()
    if len(gdf) < 5:
        raise ValueError("Dataset too small")
    return gdf[features], gdf[target]


def save_model(model, scaler, direc: str, fname: str):
    """Function for saving the model into the computer for later use

    Args:
        model (regressor): regression model
        scaler (sklearn.preprocessing): scale for the model
        direc (str): directory of the save file
        fname (str): save file name

    Raises:
        TypeError: If scaler is not from sklearn.preprocessing
        AttributeError: If __module__ can't be called from scaler
        TypeError: If model is not a regressor
        AttributeError: If model is not from sklearn model
        ValueError: Output path does not exist
        ValueError: There is existing output file
    """
    try:
        if 'sklearn.preprocessing' not in getattr(scaler, '__module__'):
            raise TypeError("Unexpect scaler type")
    except Exception as exc:
        raise AttributeError('No "__module__" attribute in scaler') from exc
    try:
        if 'regressor' != getattr(model, '_estimator_type'):
            raise TypeError("model is not regressor")
    except Exception as exc:
        raise AttributeError('''There is no
 "_estimator_type" attribute''') from exc
    if not isinstance(direc, str):
        direc = str(direc)
    if len(direc) != 0:
        if not os.path.isdir(direc):
            raise ValueError("Output path does not exist")
        if direc[-1] != '/':
            direc = dir+'/'
    if os.path.isfile(direc+fname):
        raise ValueError("Output file exist, change file name")
    output = {'model': model, 'scaler': scaler}
    joblib.dump(output, direc+fname)


main('data/example_aggr_hexagon (2).geojson')
