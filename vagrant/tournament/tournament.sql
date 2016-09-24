-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

CREATE TABLE players (
	player_id serial primary key,
	player_name varchar(255)
);

CREATE TABLE matches (
	match_id serial,
	winner_id int REFERENCES players(player_id) ,
	loser_id int REFERENCES playerspPlayer_id)
);

