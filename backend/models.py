from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    photos = db.relationship(
        "Photo",
        back_populates="user",
        uselist=True
    )
    collections = db.relationship(
        "Collection",
        back_populates="user",
        uselist=True
    )
    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        uselist=True
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def serialize(self, include_photos=False):
        data = {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
        }
        if include_photos:
            data["photos"] = [photo.serialize() for photo in self.photos]
        return data


class Photo(db.Model):
    __tablename__ = "photos"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    user = db.relationship(
        "User",
        back_populates="photos",
        uselist=False
    )
    url = db.Column(db.String(128))

    def __repr__(self) -> str:
        return f"<Photo {self.id}>"

    def serialize(self, include_user=False):
        data = {
            "id": self.id,
            "url": self.url,
        }
        if include_user:
            data["user"] = self.user.serialize()
        return data


class Collection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    user = db.relationship(
        "User",
        back_populates="collections",
        uselist=False
    )


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    user = db.relationship(
        "User",
        back_populates="favorites",
        uselist=False
    )
    favorite_type = db.Column(db.String(20))  # 'planet' or 'people'
    favorite_id = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_type": self.favorite_type,
            "favorite_id": self.favorite_id
        }


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    height = db.Column(db.String(16))
    mass = db.Column(db.String(16))
    hair_color = db.Column(db.String(64))
    skin_color = db.Column(db.String(64))
    eye_color = db.Column(db.String(64))
    birth_year = db.Column(db.String(32))
    gender = db.Column(db.String(32))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }


class Planet(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    diameter = db.Column(db.String(32))
    climate = db.Column(db.String(128))
    gravity = db.Column(db.String(64))
    terrain = db.Column(db.String(128))
    population = db.Column(db.String(64))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "population": self.population
        }
