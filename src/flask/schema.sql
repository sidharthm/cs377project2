DROP TABLE IF EXISTS users;

CREATE TABLE users(
id integer primary key autoincrement,
username text not null,
password text not null,
email text not null
);

DROP TABLE IF EXISTS notes;

CREATE TABLE notes(
id integer primary key autoincrement,
user_id id integer,
title text not null,
content text not null,
color text not null
);