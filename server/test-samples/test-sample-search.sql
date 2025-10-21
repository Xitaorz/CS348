SELECT 
    s.name AS song_name,
    a.name AS artist_name,
    al.title AS album_name
FROM songs s
JOIN album_song als ON s.sid = als.sid
JOIN albums al ON als.alid = al.alid
JOIN album_owned_by_artist aoa ON al.alid = aoa.alid
JOIN artists a ON aoa.artid = a.artid
WHERE LOWER(s.name) LIKE LOWER('%Debug Duo%')
   OR LOWER(a.name) LIKE LOWER('%Debug Duo%')
   OR LOWER(al.title) LIKE LOWER('%Debug Duo%');