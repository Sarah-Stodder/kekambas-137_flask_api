from app import app
from fake_data.posts import post_data

@app.route('/')
def index():
    first_name = 'Brian'
    last_name = 'Stanton'
    return f'Hello World!! - From {first_name} {last_name}'


# POST ENDPOINTS

# Get all posts
@app.route('/posts')
def get_posts():
    # Get the posts from storage (fake data, will setup db tomorrow)
    posts = post_data
    return posts

# Get single post by ID
@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # Get the posts from storage
    posts = post_data
    # For each dictionary in the list of post dictionaries
    for post in posts:
        # if the key of 'id' on the post dictionary matches the post_id from the URL
        if post['id'] == post_id:
            # Return that post dictionary
            return post
    # If we loop through all of the posts without returning, the post with that ID does not exist
    return {'error': f'Post with an ID of {post_id} does not exist'}, 404
    
