from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    try:
        with open('blog_posts.json') as fileobj:
            blog_posts = json.load(fileobj)
    except json.decoder.JSONDecodeError:
        blog_posts = []    
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            with open('blog_posts.json') as fileobj:
                blog_posts = json.load(fileobj)
        except json.decoder.JSONDecodeError:
            blog_posts = []  

        post_id = str(uuid.uuid4())
        new_post = {
            'id': post_id,
            'title': request.form.get('title', ''),
            'content': request.form.get('content', ''),
            'author': request.form.get('author', ''),
            'likes': 0,
        }

        if new_post['title'] == '' or new_post['content'] == '' or new_post['author'] == '':
            return "Error: All fields are required", 400

        blog_posts.append(new_post)
        with open('blog_posts.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):
    with open('blog_posts.json') as fileobj:
        blog_posts = json.load(fileobj)

    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)

    with open('blog_posts.json', 'w') as fileobj:
        json.dump(blog_posts, fileobj)

    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open('blog_posts.json') as fileobj:
        blog_posts = json.load(fileobj)

    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title', '')
        post['content'] = request.form.get('content', '')
        post['author'] = request.form.get('author', '')

        with open('blog_posts.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<post_id>')
def like(post_id):
    with open('blog_posts.json') as fileobj:
        blog_posts = json.load(fileobj)

    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    with open('blog_posts.json', 'w') as fileobj:
        json.dump(blog_posts, fileobj)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()