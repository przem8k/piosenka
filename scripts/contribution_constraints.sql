ALTER TABLE songs_artistcontribution ADD CONSTRAINT artistcontribution_unique UNIQUE (song_id, artist_id);
ALTER TABLE songs_artistcontribution ADD CONSTRAINT artistcontribution_not_dummy CHECK ( performed = True OR texted = True OR composed = True OR translated = True );

ALTER TABLE songs_bandcontribution ADD CONSTRAINT bandcontribution_unique UNIQUE (song_id, band_id);
ALTER TABLE songs_bandcontribution ADD CONSTRAINT bandcontribution_not_dummy CHECK ( performed = True );
