from flask import Flask, jsonify
import requests
from flask_cors import CORS
from models import db, WatchedEpisode

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    return 'Hello, World!'


@app.route('/continue-watching')
def continue_watching():
    series = watch_again()
    watched_episodes = series["series"][0]["episodes"]

    response = requests.get("https://api.tvmaze.com/shows/33352/episodes")
    if response.status_code == 200:
        data = response.json()
        ids = [d['id'] for d in data]
        print(ids)
        print(watched_episodes)
        diff = []
        for episode_id in ids:
            if episode_id not in watched_episodes:
                diff.append(episode_id)

        print(diff)
    else:
        print(f"Failed to get data: {response.status_code}")

    return jsonify(diff)

from models import WatchedEpisode

def get_or_create_watched_episode(user_id, episode_id):
    # Try to find an existing record
    watched_episode = WatchedEpisode.query.filter_by(user_id=user_id, episode_id=episode_id).first()
    
    # If it doesn't exist, create a new one
    if not watched_episode:
        watched_episode = WatchedEpisode(user_id=user_id, episode_id=episode_id, progress=0)
        db.session.add(watched_episode)
        db.session.commit()
    
    return watched_episode


@app.route('/continue-watching/update-progress/<user_id>/<episode_id>/<progress>')
def update_progress(user_id, episode_id, progress):
    # Get or create the watched episode record
    watched_episode = get_or_create_watched_episode(user_id, episode_id)
    
    # Update the progress
    watched_episode.progress = progress
    db.session.commit()

    return jsonify(watched_episode.dict())

def watch_again():
    return {
        "series": [
            {
                "title": "The rings of power",
                "id": 33352,
                "episodes": [2141182]
            }
        ]
    }

if __name__ == '__main__':
    app.run(debug=True)
