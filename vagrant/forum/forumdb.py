#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    cursor.execute("SELECT time, content FROM posts ORDER BY time DESC")
    cos = cursor.fetchall()
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in cos]
    #posts.sort(key=lambda row: row['time'], reverse=True)
    db.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    t = time.strftime('%c', time.localtime())
    cursor.execute("INSERT INTO posts (content) VALUES (%s)" , (bleach.clean(content),))
    db.commit()
    DB.append((t, content))
    db.close()