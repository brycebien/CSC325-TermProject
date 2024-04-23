import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import joblib
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

# Assign a number to each genre
df['track_genre'] = df['track_genre'].astype('category').cat.codes

summary_statistics = df.describe()
print(summary_statistics)

# Scaling data with MinMaxScaler
scaler = MinMaxScaler()
df[['key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature', 'tempo', 'popularity', 'duration_ms', 'explicit']] = scaler.fit_transform(df[['key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature', 'tempo', 'popularity', 'duration_ms', 'explicit']])
print('Data after scaling: ')
print(df.head())

X = df[['key', 'danceability', 'energy', 'loudness', 'instrumentalness', 'liveness', 'valence', 'time_signature', 'Unnamed: 0']]

X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

print("X_train shape: ", X_train.shape)
print("X_test shape: ", X_test.shape)

k_values = range(1, 41)
average_distances = []

for k in k_values:
    knn = NearestNeighbors(n_neighbors=k)
    nbrs = knn.fit(X)
    distances, indices = nbrs.kneighbors(X)
    average_distance = distances.mean()
    average_distances.append(average_distance)

plt.plot(k_values, average_distances)
plt.xlabel('k')
plt.ylabel('Average distance')
plt.title('Elbow Method For Optimal k')
plt.show()

# giving a specific song to the model

song = X.iloc[33987] # set this value to the song that you want to give the model
song_values = song.values.reshape(1, -1) # reshape the values to a 2D array

song_df = pd.DataFrame(song_values, columns=X_test.columns) # create a dataframe from the values

predicted_neighbors = knn.kneighbors(song_df) # get the nearest neighbors of the song
neighbor_indices = predicted_neighbors[1][0] # get the indices of the nearest neighbors
print('Similar tracks to the chosen song indicies: ', neighbor_indices, '\n-----------------------------------')

print('Selected track info:')
print(df.iloc[int(song['Unnamed: 0'])-1])
print('-----------------------------------')
print('Similar songs to the selected track:')

print('Track Name\tDanceability\tEnergy\tLoudness\tSpeechiness\tAcousticness\tInstrumentalness\tLiveness\tValence')
for i in range (5):
  print(df.iloc[neighbor_indices[i]]['track_name'],'\t', df.iloc[neighbor_indices[i]]['danceability'],'\t', df.iloc[neighbor_indices[i]]['energy'], '\t', df.iloc[neighbor_indices[i]]['loudness'], '\t', df.iloc[neighbor_indices[i]]['speechiness'], '\t', df.iloc[neighbor_indices[i]]['acousticness'], '\t', df.iloc[neighbor_indices[i]]['instrumentalness'], '\t', df.iloc[neighbor_indices[i]]['liveness'], '\t', df.iloc[neighbor_indices[i]]['valence'])

#testing similarity matematically
print('\nTesting Similarity Matematically')
print('-----------------------------------')
print('Distance from the given song for each of the 5 selected tracks')
for i in range (5):
  print(predicted_neighbors[0][0][i])
print('each of the selected tracks are close to the given track resulting in unique but similar reccomendations')

# Saving the model as .pkl file
joblib.dump(knn, 'knn_model.pkl')