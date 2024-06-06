from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from dotenv import load_dotenv
from src.dria_searching_agent.main import ResearchCrew, GetResearchCrew
from src.dria_searching_agent.config import config

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app
)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="ratelimit exceeded", description=str(e.description)), 429

# decorator for validating requests
def validate_query(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        query = data.get('query')
        if not query:
            return jsonify(error="Invalid body"), 400
        return func(*args, **kwargs)
    return decorated_function

@app.route('/search', methods=['POST'])
@validate_query
# @limiter.limit("3 per minute")
def search():
    data = request.get_json()
    query = data.get('query')
    manager = data.get("with_manager")
    
    crew = GetResearchCrew()
    if manager == True:
        result = crew.run_w_manager(query=query)
    else:
        result = crew.run(query=query)

    return jsonify(result)

def server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    config.load_config()
    GetResearchCrew()
    server()
