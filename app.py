from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_posts.json') as fileobj:
        blog_posts = json.load(fileobj)
    return render_template('index.html', posts=blog_posts)



if __name__ == '__main__':
    app.run()