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
    print(data)
    return 'Success!', 200

knn = joblib.load('knn_model.pkl')

cwd = os.getcwd()
file_path = os.path.join(cwd, 'data', 'dataset.csv')
df = pd.read_csv(file_path)

df = df.dropna(axis=0)

df['track_genre'] = df['track_genre'].astype('category').cat.codes

X = df[['Unnamed: 0','key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature', 'track_genre']]

user_prediction = X.iloc[44075].values.reshape(1, -1) # get user in here
prediction_df = pd.DataFrame(user_prediction, columns=X.columns)

# getting songs from the user input
neighbors = knn.kneighbors(prediction_df)
neighbor_indices = neighbors[1][0]

print('Selected Track:')
print(df.iloc[int(prediction_df['Unnamed: 0'].iloc[0])-1]) # TODO: search by song id??

print('\n\nSimilar Tracks:')
for i in range(5):
    print(df.iloc[neighbor_indices[i]]['track_name'], "-----------------------------", df.iloc[neighbor_indices[i]]['track_id'], "\n", df.iloc[neighbor_indices[i]]['artists'], '  ', df.iloc[neighbor_indices[i]]['track_genre'])

if __name__ == '__main__':
    app.run(port=5000)
    print('running...')