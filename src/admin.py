import os
from flask_admin import Admin
from models import db, Users, Characters, Planets, FavoritePlanets, FavoriteCharacters  # cada modelos que vaya creando tendre que irlo escibiendo en esta linea
from flask_admin.contrib.sqla import ModelView

# todo lo de arriba es para exportar lo que necesitemos


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Users, db.session))  # You can duplicate that line to add mew models
    admin.add_view(ModelView(Characters, db.session))
    admin.add_view(ModelView(Planets, db.session))
    admin.add_view(ModelView(FavoriteCharacters, db.session))
    admin.add_view(ModelView(FavoritePlanets, db.session))
    # al igual que la linea 3 escribimos todos los modelos que vamos creando, tendremos que escribirlo aqui, 
    # igual que el codigo de arriba
    # admin.add_view(ModelView(YourModelName, db.session))