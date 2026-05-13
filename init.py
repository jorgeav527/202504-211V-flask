import sqlite3

connection = sqlite3.connect("basedatos.db")

with open("schema.sql", "w") as f:
    f.write("""
DROP TABLE IF EXISTS post_comments;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL
);

CREATE TABLE post_comments (
    post_id INTEGER NOT NULL,
    comment_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, comment_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE
);
""")

with open("schema.sql", "r") as f:
    connection.executescript(f.read())


def insert_post(title, content):
    connection = sqlite3.connect("basedatos.db")
    cur = connection.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
    connection.commit()
    post_id = cur.lastrowid
    connection.close()
    return post_id


def insert_comment(content, post_ids):
    connection = sqlite3.connect("basedatos.db")
    cur = connection.cursor()
    cur.execute("INSERT INTO comments (content) VALUES (?)", (content,))
    comment_id = cur.lastrowid
    for post_id in post_ids:
        cur.execute(
            "INSERT INTO post_comments (post_id, comment_id) VALUES (?, ?)",
            (post_id, comment_id),
        )
    connection.commit()
    connection.close()
    return comment_id


p1 = insert_post("primer post", "content del primer post")
p2 = insert_post("segundo post", "content del segundo post")

insert_comment("comentario uno al primer post", [p1])
insert_comment("comentario dos a ambos posts", [p1, p2])
