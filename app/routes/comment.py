from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
from app.database import get_db_connection

comments_bp = Blueprint("comments", __name__, url_prefix="/comments")


@comments_bp.route("/list")
def get_all_comments():
    db = get_db_connection()
    comments = db.execute("SELECT * FROM comments;")
    return render_template("comment/list.html", comment_list=comments)


@comments_bp.route("/api/list", methods=["GET"])
def get_comments_partial():
    db = get_db_connection()
    comments = db.execute("SELECT * FROM comments;")
    return render_template("partials/datos-comments.html", comment_list=comments)


@comments_bp.route("/api/comments", methods=["GET"])
def get_all_comments_json():
    db = get_db_connection()
    comments = db.execute("SELECT * FROM comments;").fetchall()
    return jsonify([dict(c) for c in comments])


@comments_bp.route("/<int:comment_id>")
def get_single_comment(comment_id):
    db = get_db_connection()
    comment = db.execute(
        "SELECT * FROM comments WHERE id = ?", (comment_id,)
    ).fetchone()
    if comment is None:
        abort(404)
    posts = db.execute(
        """SELECT p.id, p.title FROM posts p
           JOIN post_comments pc ON pc.post_id = p.id
           WHERE pc.comment_id = ?""",
        (comment_id,),
    )
    return render_template("comment/single.html", comment=comment, posts=posts)


@comments_bp.route("/create", methods=("GET", "POST"))
def create_comment():
    db = get_db_connection()
    if request.method == "GET":
        posts = db.execute("SELECT id, title FROM posts;")
        return render_template("comment/create.html", posts=posts)
    if request.method == "POST":
        content = request.form["content_content"]
        post_ids = request.form.getlist("post_ids")
        db.execute("INSERT INTO comments (content) VALUES (?)", (content,))
        comment_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        for pid in post_ids:
            db.execute(
                "INSERT INTO post_comments (post_id, comment_id) VALUES (?, ?)",
                (pid, comment_id),
            )
        db.commit()
        return redirect(url_for("comments.get_all_comments"))


@comments_bp.route("/update/<int:comment_id>", methods=("GET", "POST"))
def update_comment(comment_id):
    db = get_db_connection()
    comment = db.execute(
        "SELECT * FROM comments WHERE id = ?", (comment_id,)
    ).fetchone()
    if comment is None:
        abort(404)
    if request.method == "GET":
        posts = db.execute("SELECT id, title FROM posts;")
        selected_ids = [
            r[0]
            for r in db.execute(
                "SELECT post_id FROM post_comments WHERE comment_id = ?",
                (comment_id,),
            ).fetchall()
        ]
        return render_template(
            "comment/update.html",
            comment=comment,
            posts=posts,
            selected_ids=selected_ids,
        )
    if request.method == "POST":
        content = request.form["content_content"]
        post_ids = request.form.getlist("post_ids")
        db.execute("UPDATE comments SET content = ? WHERE id = ?", (content, comment_id))
        db.execute("DELETE FROM post_comments WHERE comment_id = ?", (comment_id,))
        for pid in post_ids:
            db.execute(
                "INSERT INTO post_comments (post_id, comment_id) VALUES (?, ?)",
                (pid, comment_id),
            )
        db.commit()
        return redirect(url_for("comments.get_all_comments"))


@comments_bp.route("/delete/<int:comment_id>", methods=["POST"])
def delete_one_comment(comment_id):
    db = get_db_connection()
    comment = db.execute(
        "SELECT * FROM comments WHERE id = ?", (comment_id,)
    ).fetchone()
    if comment is None:
        abort(404)
    db.execute("DELETE FROM post_comments WHERE comment_id = ?", (comment_id,))
    db.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    db.commit()
    return redirect(url_for("comments.get_all_comments"))


@comments_bp.route("/delete/<int:comment_id>/htmx", methods=["DELETE"])
def delete_one_comment_htmx(comment_id):
    db = get_db_connection()
    comment = db.execute(
        "SELECT * FROM comments WHERE id = ?", (comment_id,)
    ).fetchone()
    if comment is None:
        abort(404)
    db.execute("DELETE FROM post_comments WHERE comment_id = ?", (comment_id,))
    db.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    db.commit()
    return ""
