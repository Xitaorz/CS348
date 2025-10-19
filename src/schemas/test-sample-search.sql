SELECT s.title, a.artist_name, al.title AS album, s.duration, s.popularity
FROM Songs s
JOIN Albums al ON s.album_id = al.album_id
JOIN Artists a ON al.artist_id = a.artist_id
WHERE s.title ILIKE '%<search_string>%'
   OR a.artist_name ILIKE '%<search_string>%'
   OR al.title ILIKE '%<search_string>%';