import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimatedPrice(location, total_sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x_dict = {
        'total_sqft': total_sqft,
        'bath': bath,
        'bhk': bhk
    }

    for location in __locations:
        x_dict[location] = 0

    if loc_index >= 0:
        x_dict[location] = 1

    x = np.array([x_dict[column] for column in __data_columns])
    return round(__model.predict([x])[0], 2)

def get_locations():
    return __locations

def local_saved_info():
    global __data_columns
    global __locations
    global __model
    try:
        with open("columns.json", 'r') as f:
            data = json.load(f)
            print(f"Data loaded from JSON: {data}")
            __data_columns = data['data_columns']
            __locations = __data_columns[3:]
            print(f"Loaded locations: {__locations}")
        with open("price_estimation_model.pickle", 'rb') as f:
            __model = pickle.load(f)
            print("Model loaded successfully")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    local_saved_info()
    print(get_locations())
    print(get_estimatedPrice('1st Phase JP Nagar', 1000, 2, 3))
