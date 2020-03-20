import json
import os
import pandas as pd
import numpy as np


def make_df(path_to_directory, export_as_csv=True, remove_na=False):
    """Make a .csv file with relevant data for each song for all .json files in a directory. Following the format of the Genius API

    Arguments:
        path_to_directory {string} -- path to directory of .json files
        export_as_csv {boolean} -- export DataFrame as .csv as `songs.csv`
        remove_na {boolean} -- remove `na` values from album and lyrics columns

    Returns:
        pandas.DataFrame -- dataframe
    """
    df = pd.DataFrame(columns=['artist', 'song_title', 'lyrics',
                               'producers', 'year_of_release', 'album'])

    for file in os.listdir(path_to_directory):
        if file.endswith('.json'):
            current_artist = file[7:-5]
            path = os.path.join(path_to_directory, file)
            with open(path) as json_file:
                data = json.load(json_file)
                for song in data['songs']:
                    song_title = song['title']
                    lyrics = song['lyrics']

                    album = song['album']
                    if album != None:
                        album = album['name']

                    producers = song['producer_artists']
                    if len(producers) > 0:
                        producers = [producer['name']
                                     for producer in producers]

                    year_of_release = song['release_date']

                    df = df.append({
                        "artist": current_artist,
                        "song_title": song_title,
                        "lyrics": lyrics,
                        "producers": producers,
                        "year_of_release": year_of_release,
                        "album": album
                    }, ignore_index=True)

    df['year_of_release'] = pd.to_datetime(
        df['year_of_release'], errors='coerce')

    df['year_of_release'] = pd.DatetimeIndex(df['year_of_release']).year
    df.loc[df['year_of_release'].isna(), 'year_of_release'] = 0
    df['year_of_release'] = df['year_of_release'].astype(int)
    df = df[df['year_of_release'] != 0]

    if remove_na:
        df = df.dropna(subset=['album', 'lyrics'])

    if export_as_csv:
        df.to_csv('songs.csv', index=False)

    return df
