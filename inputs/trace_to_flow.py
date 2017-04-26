import pandas as pd

df = pd.read_csv('./transitions-mood-sound-gender-collaps.csv')
df = df[['playlist_id', 'source', 'tags', 'mood_source', 'mood_target',
         'sound_source', 'sound_target', 'playlist_name', 'genre_source',
         'genre_target']]

for i in range(len(df)):
    row = df.ix[i]
    try:
        if isinstance(row['tags'], str):
            tags = row['tags']
        else:
            tags = 'NT'
        if isinstance(row['playlist_name'], str):
            name = row['playlist_name']
        else:
            name = 'NN'

        t = str(row['playlist_id']) + '/' + tags + '/' + name + '/' + \
            row['source']

        print(0, end='\t')
        print(t, end='\t')

        print(row['mood_source'], end='/')
        print(row['sound_source'], end='/')
        print(row['genre_source'], end='\t')

        print(row['mood_target'], end='/')
        print(row['sound_target'], end='/')
        print(row['genre_target'])
    except:
        pass
