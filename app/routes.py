from flask import request
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

# Create new Post route
@app.route('/posts', methods=['POST'])
def create_post():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get data from the body
    title = data.get('title')
    body = data.get('body')

    # Create a new post with data
    new_post = {
        "id": len(post_data) + 1,
        "title": title,
        "body": body,
        "userId": 1,
        "dateCreated": "2024-01-09T11:25:45",
        "likes": 0
    }
    # Add the new post to the list of posts
    post_data.append(new_post)
    return new_post, 201
