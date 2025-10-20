SELECT 
    s.name AS song_name,
    a.name AS artist_name,
    ROUND(AVG(r.rate_value), 2) AS avg_rating
FROM song_ratings r
JOIN songs s ON r.sid = s.sid
JOIN album_song als ON s.sid = als.sid
JOIN album_owned_by_artist aoa ON als.alid = aoa.alid
JOIN artists a ON aoa.artid = a.artid
GROUP BY s.sid, a.artid, s.name, a.name;