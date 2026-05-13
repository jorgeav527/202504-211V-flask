from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
from app.database import get_db_connection

post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route("/list")
def get_all_posts():
    db = get_db_connection()
    posts = db.execute("SELECT * FROM posts;")
    return render_template("post/list.html", post_list=posts)

@post_bp.route("/api/list", methods=["GET"])
def get_posts_partial():
    db = get_db_connection()
    posts = db.execute("SELECT * FROM posts;")
    return render_template("partials/datos-json.html", post_list=posts)


@post_bp.route("/api/posts", methods=["GET"])
def get_all_posts_json():
    db = get_db_connection()
    posts = db.execute("SELECT * FROM posts;").fetchall()
    return jsonify([dict(post) for post in posts])


@post_bp.route("/<int:post_id>")
def get_single_post(post_id):
    db = get_db_connection()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    print(post)
    if post is None:
        abort(404)
    return render_template("post/single.html", post_single=post)


@post_bp.route("/create", methods=("GET", "POST"))
def create_post():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        title = request.form["title_title"]
        content = request.form["content_content"]
        db = get_db_connection()
        db.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)", (title, content)
        )
        db.commit()
        return redirect(url_for("post.get_all_posts"))


@post_bp.route("/update/<int:post_id>", methods=("GET", "POST"))
def update_post(post_id):
    db = get_db_connection()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if post is None:
        abort(404)
    if request.method == "GET":
        return render_template("post/update.html", single_post=post)
    if request.method == "POST":
        title = request.form["title_title"]
        content = request.form["content_content"]
        db.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            (title, content, post_id),
        )
        db.commit()
        return redirect(url_for("post.get_all_posts"))


@post_bp.route("/delete/<int:post_id>", methods=["POST"])
def delete_one_post(post_id):
    db = get_db_connection()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if post is None:
        abort(404)
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return redirect(url_for("post.get_all_posts"))


@post_bp.route("/delete/<int:post_id>/htmx", methods=["DELETE"])
def delete_one_post_htmx(post_id):
    db = get_db_connection()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if post is None:
        abort(404)
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    if request.method == "DELETE":
        return ""