import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import os

# Get the current working directory
cwd = os.getcwd()

# Construct the file path relative to the current working directory
file_path = os.path.join(cwd, 'data', 'dataset.csv')

df = pd.read_csv(file_path)

missing_values = df.isnull().sum()
print('Columns with missing values:')
print(missing_values[missing_values > 0])

df.head().sum()

# delete rows with missing values
df = df.dropna(axis=0)
#drop columns not needed
df = df.drop(columns=['tempo'])
df = df.drop(columns=['popularity'])
df = df.drop(columns=['duration_ms'])
df = df.drop(columns=['explicit'])
df = df.drop(columns=['track_genre'])

summary_statistics = df.describe()
summary_statistics

X = df[['Unnamed: 0','key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature']]

X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

print("X_train shape: ", X_train.shape)
print("X_test shape: ", X_test.shape)

knn = NearestNeighbors(n_neighbors=5)
knn.fit(X_train)

predicted_neighbors = knn.kneighbors(X_test)
neighbor_indices = predicted_neighbors[1][0]

print('Similar tracks to the chosen song indicies: ', neighbor_indices, '\n-----------------------------------')

print('Selected track info:')
print(df.iloc[int(X_test.iloc[0]['Unnamed: 0'])-1])
print('-----------------------------------')
print('Similar songs to the selected track:')

print('Track Name\tDanceability\tEnergy\tLoudness\tSpeechiness\tAcousticness\tInstrumentalness\tLiveness\tValence')
for i in range (5):
  print(df.iloc[neighbor_indices[i]]['track_name'],'\t', df.iloc[neighbor_indices[i]]['danceability'],'\t', df.iloc[neighbor_indices[i]]['energy'], '\t', df.iloc[neighbor_indices[i]]['loudness'], '\t', df.iloc[neighbor_indices[i]]['speechiness'], '\t', df.iloc[neighbor_indices[i]]['acousticness'], '\t', df.iloc[neighbor_indices[i]]['instrumentalness'], '\t', df.iloc[neighbor_indices[i]]['liveness'], '\t', df.iloc[neighbor_indices[i]]['valence'])


#testing similarity matematically
print('Distance from the given song for each of the 5 selected tracks')
for i in range (5):
  print(predicted_neighbors[0][0][i])
print('each of the selected tracks are close to the given track resulting in unique but similar reccomendations')