import lyricsgenius
import os
import pandas as pd


def scrape_lyrics(text_file):
    """Scrapes lyrics from Genius.com using `lyricsgenius` library

    Arguments:
        text_file {string} -- path to .txt file with artist names

    Returns:
        [string] -- names of artists
    """
    artist_file = open(text_file, 'r')
    artist_names = [line.strip() for line in artist_file.readlines()]

    genius = lyricsgenius.Genius(
        "etKd8sM-UwZkSRrZplkdUJhMGaIpvPKfLD_zpsFgd9ba0z0p5lMn92izAeVKHD89", remove_section_headers=True, excluded_terms=['(Live)', '(Demo)', '(Remix)'], timeout=10, verbose=False)

    print('Scraping lyrics from Genius.com...')

    for artist_name in artist_names:
        artist = genius.search_artist(artist_name, sort='title')
        print(f'{artist.name}: {artist.num_songs} songs')
        artist.save_lyrics(extension='json')

    return artist_names
