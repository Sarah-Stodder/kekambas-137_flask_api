from app import app

@app.route('/')
def index():
    first_name = 'Brian'
    last_name = 'Stanton'
    return f'Hello World!! - From {first_name} {last_name}'
