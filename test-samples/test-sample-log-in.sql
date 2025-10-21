SELECT uid
FROM users
WHERE username = "alice"
  AND password_hash = SHA2("password123", 256);
