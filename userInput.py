import joblib
import pandas as pd
import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__) # create an instance of the Flask class for the web app
CORS(app) # enable Cross-Origin Resource Sharing (CORS) for the web app

@app.route('/receive_data', methods=['POST']) # define the route for the web app
# This function receives data from the user and returns the recommended songs
def receive_data():
    data = request.json
    # Load the k-Nearest Neighbors model from the file
    knn = joblib.load('knn_model.pkl')

    # Load the dataset from the file
    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'data', 'dataset.csv')
    df = pd.read_csv(file_path)

    # delete rows with missing values
    df = df.dropna(axis=0)

    X = df[['key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature', 'tempo']] # features

    #clean input data to match the model
    data_df = pd.DataFrame()
    data_df['key'] = [data['key']]
    data_df['danceability'] = [data['danceability']]
    data_df['energy'] = [data['energy']]
    data_df['loudness'] = [data['loudness']]
    data_df['instrumentalness'] = [data['instrumentalness']]
    data_df['liveness'] = [data['liveness']]
    data_df['valence'] = [data['valence']]
    data_df['time_signature'] = [data['time_signature']]
    data_df['tempo'] = [data['tempo']]
    user_prediction = data_df.values.reshape(1, -1) 
    prediction_df = pd.DataFrame(user_prediction, columns=X.columns)

    # removing song from the database if it exists
    if data['id'] in df['track_id'].values:
        df = df[df['track_id'] != data['id']]

    # getting songs from the user input
    neighbors = knn.kneighbors(prediction_df)
    neighbor_indices = neighbors[1][0]
    print(neighbor_indices)

    # getting the songs from the indices
    songs = []
    for i in range(4):
        if df.iloc[neighbor_indices[i]]['track_name'] == df.iloc[neighbor_indices[i-1]]['track_name']:
            songs.append(df.iloc[neighbor_indices[i]-1]['track_id'])
        else:
            songs.append(df.iloc[neighbor_indices[i]]['track_id'])

    print(songs) # print the recommended songs

    return songs, 200 # return the recommended songs

# Run the web app
if __name__ == '__main__':
    app.run(port=5000) # run the web app on port 5000
    print('running...')