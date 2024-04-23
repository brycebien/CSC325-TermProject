import joblib
import pandas as pd
import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    knn = joblib.load('knn_model.pkl')

    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'data', 'dataset.csv')
    df = pd.read_csv(file_path)

    df = df.dropna(axis=0)

    X = df[['key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature', 'tempo']]

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

    songs = []
    for i in range(4):
        if df.iloc[neighbor_indices[i]]['track_name'] == df.iloc[neighbor_indices[i-1]]['track_name']:
            songs.append(df.iloc[neighbor_indices[i]-1]['track_id'])
        else:
            songs.append(df.iloc[neighbor_indices[i]]['track_id'])

    print(songs)

    # print(data)
    return songs, 200

if __name__ == '__main__':
    app.run(port=5000)
    print('running...')