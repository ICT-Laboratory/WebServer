from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

print("aaaafeksaflneksanflkesunflakf")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.String(10), nullable=False)
    version_id = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Blog('{self.blog_id}', '{self.version_id}', '{self.title}', '{self.date}', '{self.author}', '{self.thumbnail}')"

with app.app_context():
    db.create_all()

@app.route('/getblog')
def getblog():
    data = Blog.query.all()
    return jsonify([{"id":i.id, "blog_id":i.blog_id, "version_id":i.version_id, "title":i.title, "text":i.text, "date":i.date, "author":i.author, "thumnnail": i.thumbnail} for i in data])

@app.route('/addblog', methods=["POST", 'GET'])
def addblog():
    if request.method == "POST":
        if request.headers['Content-Type'] == 'application/json':
            data = request.json
            blog = Blog(blog_id='aaa', version_id='bbb', title=data["title"], text=data["text"], date=data["date"], author=data["author"], thumbnail=data["thumbnail"])
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for("getblog"))
        else:
            title = request.form["title"]
            text = request.form["text"]
            date = request.form["date"]
            author = request.form["author"]
            thumbnail = request.form["thumbnail"]
            blog = Blog(blog_id='aaa', version_id='bbb', title=title, text=text, date=date, author=author,thumbnail=thumbnail)
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for("getblog"))
    return '''<form method="POST">
    <label>title</label><input name="title"><br>
    <label>text</label><textarea name="text"></textarea><br>
    <label>date</label><input name="date"><br>
    <label>author</label><input name="author"><br>
    <label>thumbnail</label><input name="thumbnail"><br>
    <input type="submit" value="Submit">
    </form>'''

@app.route("/")
def home():
    return render_template("index.html", name="Home")


@app.route("/sitemap")
def site():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://ict-lab.org/</loc>
        <lastmod>2024-08-08</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://ict-lab.org/about</loc>
        <lastmod>2024-08-08</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>
"""

@app.route("/<path>")
def all_page(path):
    return render_template(f"{path}.html")

@app.route("/app/<dirname>/<filename>")
def webapp(dirname, filename):
    return render_template(f"app/{dirname}/{filename}")

@app.route("/lab/home")
def store():
    return render_template("ECsite/home.html")

if __name__ == "__main__":
    app.run(port=5002, debug=True, host="0.0.0.0")
