from flask_restplus import Api

from .auth_controller import api as auth
from .first_admin_controller import api as first
from .user_controller import api as user
from .user_upit_controller import api as user_upit
from .admin_controller import api as admin

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'Basic Auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='Gym API',
    version='1.0.0',
    description='Sveučilište u Zadru - Studij informacijskih tehnologija - Razvoj web aplikacija',
    contact='filip.vukic55@gmail.com',
    authorizations=authorizations,
    serve_challenge_on_401=False
)

api.add_namespace(first)
api.add_namespace(auth)
api.add_namespace(user)
api.add_namespace(user_upit)
api.add_namespace(admin)