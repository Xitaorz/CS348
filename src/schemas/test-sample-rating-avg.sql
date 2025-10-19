SELECT s.title, a.artist_name, AVG(r.rating) AS avg_rating
FROM Ratings r
JOIN Songs s ON r.song_id = s.song_id
JOIN Artists a ON s.artist_id = a.artist_id
GROUP BY s.song_id, a.artist_name, s.title;