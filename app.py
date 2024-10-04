from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_posts.json') as fileobj:
        blog_posts = json.load(fileobj)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            with open('blog_posts.json', 'r') as fileobj:
                blog_posts = json.load(fileobj)
        except FileNotFoundError:
            blog_posts = []

        new_post = {
            'id': len(blog_posts) + 1,
            'title': request.form.get('title', ''),
            'content': request.form.get('content', ''),
            'author': request.form.get('author', '')
        }

        if new_post['title'] == '' or new_post['content'] == '' or new_post['author'] == '':
            return "Error: All fields are required", 400

        blog_posts.append(new_post)
        with open('blog_posts.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj)

        return redirect(url_for('index'))

    return render_template('add.html')




if __name__ == '__main__':
    app.run()