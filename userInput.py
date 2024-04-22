import joblib
import pandas as pd
import os

knn = joblib.load('knn_model.pkl')

cwd = os.getcwd()
file_path = os.path.join(cwd, 'data', 'dataset.csv')
df = pd.read_csv(file_path)

df = df.dropna(axis=0)
df = df.drop(columns=['tempo'])
df = df.drop(columns=['popularity'])
df = df.drop(columns=['duration_ms'])
df = df.drop(columns=['explicit'])
df = df.drop(columns=['track_genre'])

X = df[['Unnamed: 0','key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature']]

user_prediction = X.iloc[100].values.reshape(1, -1) # get user in here
prediction_df = pd.DataFrame(user_prediction, columns=X.columns)

# getting songs from the user input
neighbors = knn.kneighbors(prediction_df)
neighbor_indices = neighbors[1][0]
print("HERE:::: ", neighbor_indices)

print('Selected Track:')
print(df.iloc[int(prediction_df['Unnamed: 0'].iloc[0])-1]) # TODO: search by song id??

print('\n\nSimilar Tracks:')
for i in range(5):
    print(df.iloc[neighbor_indices[i]]['track_name'], "-----------------------------", df.iloc[neighbor_indices[i]]['track_id'])


