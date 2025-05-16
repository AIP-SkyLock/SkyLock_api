from flask import Blueprint

# Create a Blueprint for routes
main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def landing():
    return {"message": "Welcome to the Flask API!"}
@main_routes.route('/test')
def test():
    return {"message": "Welcome to the test!"}