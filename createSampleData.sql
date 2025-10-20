INSERT INTO users (username, email, password_hash, gender, age, street, city, province, mbti)
VALUES
('alice', 'alice@example.com', SHA2('password123', 256), 'female', 23, '123 Maple St', 'Waterloo', 'Ontario', 'INFP'),
('bob', 'bob@example.com', SHA2('securepass', 256), 'male', 25, '45 King St', 'Toronto', 'Ontario', 'ENTJ'),
('charlie', 'charlie@example.com', SHA2('charliepwd', 256), 'nonbinary', 28, '78 Queen St', 'Ottawa', 'Ontario', 'INTP'),
('diana', 'diana@example.com', SHA2('dianapass', 256), 'female', 21, '56 Duke St', 'Kitchener', 'Ontario', 'ENFP');
