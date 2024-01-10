from flask import request
from app import app, db
from fake_data.posts import post_data
from app.models import User, Post

# # We will setup DB later, for now we will store all new users in this list
# users = []

@app.route('/')
def index():
    first_name = 'Brian'
    last_name = 'Stanton'
    return f'Hello World!! - From {first_name} {last_name}'

# USER ENDPOINTS 

# Create New User
@app.route('/users', methods=['POST'])
def create_user():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    # Get the data from the request body
    data = request.json

    # Validate that the data has all of the required fields
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get the values from the data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check to see if any current users already have that username and/or email
    check_users = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    # If the list is not empty then someone already has that username or email
    if check_users:
        return {'error': 'A user with that username and/or email already exists'}, 400

    # Create a new user instance with the request data which will add it to the database
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user.to_dict(), 201

# POST ENDPOINTS

# Get all posts
@app.route('/posts')
def get_posts():
    # Get the posts from the database
    posts = db.session.execute(db.select(Post)).scalars().all()
    # return a list of the dictionary version of each post in posts
    return [p.to_dict() for p in posts]

# Get single post by ID
@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # Get the Post from the database based on the ID
    post = db.session.get(Post, post_id)
    if post:
        return post.to_dict()
    else:
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

    # Create a new instance of Post which will add to our database
    new_post = Post(title=title, body=body, user_id=4)
    return new_post.to_dict(), 201
