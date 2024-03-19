from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<User: {self.id}>'

    def serialize(self):
        return {"id": self.id,
                "email": self.email,
                "is_active": self.is_active}

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Planet: {self.id}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name}

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Character: {self.id}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name}

class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    user = db.relationship('Users', foreign_keys=[user_id])
    planet = db.relationship('Planets', foreign_keys=[planet_id])

    def __repr__(self):
        return f'<Favorite_Planets: {self.id}>'

    def serialize(self):
        return {"id": self.id,
                "planet_id": self.planet_id,
                "user_id": self.user_id}

class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    user = db.relationship('Users', foreign_keys=[user_id])
    character = db.relationship('Characters', foreign_keys=[character_id])

    def __repr__(self):
        return f'<Favorite_Characters: {self.id}>'

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "character_id": self.character_id}
