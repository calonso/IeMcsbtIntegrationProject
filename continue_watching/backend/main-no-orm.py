from flask import Flask, jsonify
import requests
from flask_cors import CORS
from models import db, WatchedEpisode
from sqlalchemy.pool import NullPool
import oracledb
from sqlalchemy import create_engine, text

app = Flask(__name__)
CORS(app)

un = '<Username>'
pw = '<password>'
dsn = '<dsn, copied from oracle cloud>'

pool = oracledb.create_pool(user=un, password=pw,
                            dsn=dsn)

engine = create_engine("oracle+oracledb://", creator=pool.acquire, poolclass=NullPool, future=True, echo=True)

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

def get_or_create_watched_episode(user_id, episode_id, connection):
    # Try to find an existing record
    select_query = text(
        """
        SELECT * FROM watched_episode WHERE user_id=:user_id AND episode_id=:episode_id
        """
    )
    
    watched_episode = connection.execute(select_query, {"user_id": user_id, "episode_id": episode_id}).mappings().fetchone()
    
    # If it doesn't exist, create a new one
    if not watched_episode:
        insert_query = text(
            """
            INSERT INTO watched_episode(id, user_id, episode_id, progress)
            VALUES (watched_episode_id_seq.NEXTVAL, :user_id, :episode_id, 0)
            """
        )
        connection.execute(insert_query, { "user_id": user_id, "episode_id":episode_id })

        watched_episode = connection.execute(select_query, { "user_id": user_id, "episode_id": episode_id }).mappings().fetchone()

    return watched_episode


@app.route('/continue-watching/update-progress/<user_id>/<episode_id>/<progress>')
def update_progress(user_id, episode_id, progress):
    with engine.connect() as connection:
        # Get or create the watched episode record
        watched_episode = get_or_create_watched_episode(user_id, episode_id, connection)
        
        # Update the progress
        update_query = text(
            """
            UPDATE watched_episode SET progress=:progress WHERE id=:id
            """
        )
        connection.execute(update_query, { "progress": progress, "id": watched_episode["id"] })
        connection.commit()

    return jsonify(dict(watched_episode))

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
