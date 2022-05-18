from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.sqlite3"


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    content = db.Column(db.String())

    def to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/post/add", methods=["POST"])
def add_post():
    try:
        form = request.form
        post = Post(title=form["title"], content=form["content"], author=form["author"])
        db.session.add(post)
        db.session.commit()
    except Exception as error:
        print("Error", error)

    return redirect(url_for("home"))


@app.route("/post/<i>/delete")
def del_post(i):
    try:
        post = Post.query.get(i)
        db.session.delete(post)
        db.session.commit()
    except Exception as error:
        print('Error ', error)

    return redirect(url_for("home"))


@app.route("/post/<i>/edit", methods=["GET", "POST"])
def edit_post(i):
    if request.method == "POST":
        try:
            post = Post.query.get(i)
            form = request.form
            post.title = form["title"]
            post.content = form["content"]
            post.author = form["author"]
            db.session.commit()
        except Exception as error:
            print('Error ', error)

        return redirect(url_for("home"))

    else:
        try:
            post = Post.query.get(i)
            return render_template("guiga_edit.html", post=post)
        except Exception as error:
            print('Error ', error)

    return redirect(url_for("home"))

########################################################################################################################
#################################API FUNCTIONS##########################################################################
########################################################################################################################
@app.route("/api/posts")
def api_home():
    try:
        posts = Post.query.all()
        return jsonify([post.to_dict() for post in posts])
    except Exception as error:
        pass

    return jsonify([])


@app.route("/api/post", methods=["PUT"])
def api_add_post():
    try:
        data = request.get_json()
        post = Post(title=data["title"], author=data["author"], content=data["content"])
        db.session.add(post)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as error:
        print('Error ', error)

    return jsonify({"success": False})


@app.route("/api/<i>/delete", methods=["DELETE"])
def api_del_post(i):
    try:
        post = Post.query.get(i)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as error:
        print('Error ', error)

    return jsonify({"success": False})


@app.route("/api/<i>/edit", methods=["PUT"])
def api_edit_post(i):
    try:
        post = Post.query.get(i)
        data = request.get_json()
        post.title = data['title']
        post.author = data['author']
        post.content = data['content']
        db.session.commit()
        return jsonify({"success": True})
    except Exception as error:
        print('Error ', error)

    return jsonify({"success": False})


db.create_all()
app.run(debug=True)
