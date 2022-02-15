from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy_media import StoreManager, FileSystemStore, Image, ImageAnalyzer, ImageValidator, ImageProcessor




## HOX, Fix many to one and one to many relationships correctly!

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    game_id = db.Colum(db.Integer, db.ForeignKey('game.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Tournament')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    time = db.Column(db.Time(timezone=False))
    team_ids = db.Column(db.Integer, db.ForeignKey('team.id'))
    game_id = db.relationship('Tournament')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(150))
    players = db.Column(db.Integer, db.ForeignKey('player.id'))
    win = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    game_id = db.relationship('Game')

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    image = db.Column(ProfileImage.as_mutable(Json))
    win = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    game_id = db.relationship('Team')


class Json(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, engine):
        return json.dumps(value)

    def process_result_value(self, value, engine):
        if value is None:
            return None

        return json.loads(value)


class ProfileImage(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(80, 80),
            maximum=(800, 600),
            min_aspect_ratio=1.2,
            content_types=['image/jpeg', 'image/png']
        ),
        ImageProcessor(
            fmt='jpeg',
            width=120,
            crop=dict(
                left='10%',
                top='10%',
                width='80%',
                height='80%',
            )
        )
    ]

