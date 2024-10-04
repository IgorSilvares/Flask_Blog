from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the main page of the blog, which displays a list of all blog posts.

    If the blog_posts.json file does not exist or is empty, render the template
    with an empty list of posts. Otherwise, load the list of posts from the file
    and render the template with it.
    """
    try:
        with open('blog_posts.json') as fileobj:
            blog_posts = json.load(fileobj)
    except json.decoder.JSONDecodeError:
        blog_posts = []    
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle a request to add a new blog post.

    If the request method is POST, attempt to load the list of posts from the
    blog_posts.json file. If the file does not exist or is empty, create an empty
    list. Otherwise, load the list from the file.

    Extract the title, content, and author from the request form data. If any of
    these fields is empty, return a 400 error with a message indicating that all
    fields are required.

    Generate a post ID as a random UUID, and create a new post dictionary with
    the extracted title, content, author, and post ID. Add this new post to the
    list of posts, and write the updated list back to the blog_posts.json file.

    Redirect the user to the main page of the blog.

    If the request method is not POST, render the add.html template.
    """
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
    """
    Handle a request to delete a blog post with the given post_id.

    Load the list of posts from the blog_posts.json file. Iterate over the list
    of posts, and if a post has a matching post_id, remove it from the list.

    Write the updated list of posts back to the blog_posts.json file, and
    redirect the user to the main page of the blog.
    """
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
    """
    Handle a request to update a blog post with the given post_id.

    Load the list of posts from the blog_posts.json file. If a post with the
    given post_id is found, render the update.html template with the post
    filled in. If the request is a POST, update the post in the list of
    posts and write the list back to the blog_posts.json file. Then redirect
    the user to the main page of the blog.
    """
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
    """
    Handle a request to like a blog post with the given post_id.

    Load the list of posts from the blog_posts.json file. If a post with the
    given post_id is found, increment its likes field by 1 and write the
    list back to the blog_posts.json file. Then redirect the user to the
    main page of the blog.
    """
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