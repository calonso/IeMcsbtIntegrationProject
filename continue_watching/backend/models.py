from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WatchedEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.Integer, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'episode_id': self.episode_id,
            'progress': self.progress
        }