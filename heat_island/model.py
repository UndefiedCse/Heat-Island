"""This module is to train KNN regression
and optimize the best k hyperparameter
"""
import os.path
import joblib
import geopandas as gpd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
# from heat_island.data_process import input_file_from_data_dir


def get_keys():
    """Default keys for datafile might be subjected to change

    Returns:
        list: list of default keys for features
    """
    centroid = 'centroid_stat_'
    # terrain = 'terrain_stat_'
    # Add or change what features to use or don't use here
    # features = ['Lat', 'Lon', 'Elev (m.)',
    #             centroid+'mean', centroid+'std_dev', centroid+'min',
    #             centroid+'25%', centroid+'50%', centroid+'75%', centroid+'max',
    #             terrain+'mean', terrain+'std_dev', terrain+'min',
    #             terrain+'25%', terrain+'50%', terrain+'75%', terrain+'max'
    #             ]
    features = [centroid+'total_height_area',
                centroid+'avg_height_area', centroid+'mean', centroid+'std_dev',
                centroid+'min', centroid+'25%', centroid+'50%', centroid+'75%',
                centroid+'max', 'Lat', 'Lon'
               ]
    return features


def find_best_estimator(x_train, y_train, scaler):
    """Find the best hyperparameter for KNN, LR, RFR

    Args:
        x_train (df): training data input
        y_train (df): true value of training dataset
        scaler (scaler): standard scaler for transforming

    Returns:
        dict: best KNN, LR, RFR model
    """
    models = {
        'KNN': KNeighborsRegressor(weights='distance'),
        'LinearRegression': LinearRegression(),
        'RandomForestRegressor': RandomForestRegressor()
    }
    param_grid = {
        'KNN': {'n_neighbors': [3, 5, 7, 9],
                'weights': ['uniform', 'distance']},
        'LinearRegression': {},
        'RandomForestRegressor': {
            'n_estimators': [100, 150, 200],
            'max_depth': [2, 5, 10, 20]
        }
    }
    best_estimators = {}
    for model_name, model_inst in models.items():
        grid_search = GridSearchCV(model_inst, param_grid[model_name],
                                   cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(scaler.transform(x_train), y_train)
        best_estimators[model_name] = grid_search.best_estimator_
    return best_estimators


def get_scores(x_test, y_test, best_estimators, scaler):
    """Calculate RMSE for each model to check generalization error

    Args:
        x_test (df): testing data feature
        y_test (df): true value of testing data
        best_estimators (dict): dict of optimized model (KNN, LR, RFR)
        scaler (standard scaler): scaler for transformation

    Returns:
        dict: RMSE of each model type
    """
    model_scores = {}
    for model_name, model in best_estimators.items():
        y_pred = model.predict(scaler.transform(x_test))
        model_scores[model_name] = mean_squared_error(y_test, y_pred)**0.5
    return model_scores


def train(data_path: str, features: list = None,
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
    if fname[-4:] != '.bin':
        raise ValueError("Save file must be `.bin` format")
    if features is None:
        features = get_keys()
    x, y = clean_data(data_path, features, target)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,
                                                        random_state=0)
    scale = StandardScaler()
    scale.fit(x_train)

    best_estimators = find_best_estimator(x_train, y_train, scale)
    model_scores = get_scores(x_test, y_test, best_estimators, scale)

    print(f"Model Scores: {model_scores}")
    model_path = save_model(best_estimators[min(model_scores,
                                            key=model_scores.get)],
                            scale, save_path, fname)
    return model_path


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
    if len(gdf) < 9:
        raise ValueError("Dataset too small")
    return gdf[features], gdf[target]


def load_model(path: str):
    """Load model with the same format as save_model

    Args:
        path (str): path to saved model file

    Raises:
        ValueError: If there is no file according to `path`
        ValueError: Save file format must be the same as save_model
        ValueError: If file structure is not the same as save_model

    Returns:
        regressor: regressor model
        scaler: scale for prediction
    """
    if not isinstance(path, str):
        path = str(path)
    if not os.path.isfile(path):
        raise ValueError("Input path does not exist")
    if path[-4:] != '.bin':
        raise ValueError("Incorrect file type")
    tmp = joblib.load(path)
    if 'model' not in tmp.keys() or 'scaler' not in tmp.keys():
        raise ValueError("Unexpected file structure")
    return tmp['model'], tmp['scaler']


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
    print(f"Save file at {direc+fname}")
    return direc+fname

# For testing purposes
# if __name__ == '__main__':
#     model_path = train('data/example_aggr_hexagon (2).geojson', save_path='data/',
#                        fname='seattle_model.bin'
#                       )
#     model_path = 'data/seattle_model.bin'
#     modeler, scaler = load_model(model_path)
#     print("complete")
