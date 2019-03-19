from app import app
from app.scripts import anime2019_clean, anime2019_get
from flask import render_template, url_for, redirect

#データ数 -> 74
def create_dataset():
    df, comment_list = anime2019_clean.clean_info()
    title = df.title.values
    onAir = df.onAir.values
    img = df.img.values
    comment = df.comment.values
    comment_count = df.comment_count.values
    dataset = zip(title, onAir, img, comment, comment_count, comment_list)
    return dataset

@app.route("/")
def index():
    dataset = create_dataset()
    return render_template("index.html", dataset=dataset)

@app.route("/updated", methods=["GET", "POST"])
def update_info():
    anime2019_get.get_info()
    return redirect(url_for('index'))
