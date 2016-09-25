#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM matches')
    conn.commit()
    c.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM players;')
    conn.commit()
    c.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM players')
    number_of_players = str(c.fetchall())
    number_of_players = number_of_players.replace("[(","")
    number_of_players = number_of_players.replace("L,)]" , "")
    number_of_players = int(number_of_players)
    c.close()
    return(number_of_players)


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO players (player_name) VALUES (%s)', (name,))
    conn.commit()
    c.close()


def printPlayers():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM players')
    print(c.fetchall())
    c.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT  players.player_id, players.player_name, CASE WHEN t.wins IS NULL THEN 0 ELSE t.wins END, \
    CASE WHEN t.num IS NULL THEN 0 ELSE t.num END \
    FROM players \
    LEFT JOIN \
    (SELECT matches.id, w.wins, matches.num FROM \
    (SELECT winner_id, COUNT(*) as wins FROM matches GROUP BY winner_id) AS w \
    RIGHT JOIN \
    (SELECT id, COUNT(*) AS num FROM \
    (SELECT winner_id AS id FROM matches UNION ALL SELECT loser_id AS id FROM matches) AS m GROUP BY id) AS matches \
    ON w.winner_id = matches.id) AS t \
    ON players.player_id = t.id \
    ORDER BY wins DESC;')
    standings = c.fetchall()
    c.close()
    return (standings)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO matches (winner_id, loser_id) VALUES (%s,%s)', (winner, loser))
    conn.commit()
    c.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairs = []
    for i in range(0,len(standings),2):
        pairs.append([standings[i][0],standings[i][1],standings[i+1][0],standings[i+1][1]])
    return(pairs)