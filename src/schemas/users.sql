/*
CREATE TABLE users (
  uid        BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  username       VARCHAR(64)  NOT NULL,     
  email          VARCHAR(255) NOT NULL UNIQUE,
  password_hash  VARCHAR(255) NOT NULL,

  -- profile (kept simple; normalize further if needed)
  gender         ENUM('male','female','nonbinary','other') NULL,
  age            SMALLINT UNSIGNED NULL,
  hobby          VARCHAR(255) NULL,
  street         VARCHAR(255) NULL,
  city           VARCHAR(128) NULL,
  province       VARCHAR(128) NULL,
  mbti           ENUM('INTJ','INTP','ENTJ','ENTP','INFJ','INFP','ENFJ','ENFP','ISTP','ISFP','ESFJ','ESFP','ISTJ','ISFJ','ESTJ','ESFJ') NULL,

  created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
*/