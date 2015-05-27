import os

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'imdb')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'imdb')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'imdb')

DEBUG = True

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

PAGINATION_DEFAULT = 10

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']


# Our API will expose resource (MongoDB collections): 'movies'.
# In order to allow for proper data validation, we define beaviour
# and structure.

movies = {

	# 'title' tag used in item links.
	'item_title': 'movie',

	# Only allow admins and user to read.
	'allowed_read_roles': ['admin', 'user'],
	# Only allow admin to write.
	'allowed_write_roles': ['admin'],

	# DataSource
	'datasource': {'default_sort': [('_created', -1)]},

	# Schema definition, based on Cerberus grammar. Check the Cerberus project
	# (https://github.com/nicolaiarocci/cerberus) for details.
	'schema': {
	    # name of the movie
	    'name': {
	        'type': 'string',
	        'minlength': 1,
	        'maxlength': 100,
	        'required': True,
	    },
	    # name of the director
	    'director': {
	        'type': 'string',
	        'minlength': 1,
	        'maxlength': 50,
	        'required': True,
	    },
	    # 99popularity is a integer with max value 99.
	    '99popularity': {
	        'type': 'integer',
	        'max': 99,
	        'required': True,
	    },
	    # imdb score is a floating point number with max value 99.
	    'imdb_score': {
	        'type': 'float',
	        'max': 10,
	        'required': True,
	    },
	    # Genre is a list of strings.
	    'genre': {
	        'type': 'list',
	        'schema': {
	            'type': 'string',
	        }
	    }
	}
}

users = {
	'additional_lookup': {
	    'url': 'regex("[\w]+")',
	    'field': 'username',
	},
	# We also disable endpoint caching as we don't want client apps to
	# cache account data.
	'cache_control': '',
	'cache_expires': 0,

	# Only allow admins.
	'allowed_roles': ['admin'],

	'schema': {
		'firstname': {
			'type': 'string'
		},
		'lastname': {
			'type': 'string'
		},
		'username': {
			'type': 'string',
			'unique': True,
			'required': True,
		},
		'password': {
			'type': 'string',
			'required': True,
		},
		'roles': {
			'type': 'list',
			'allowed': ['user', 'admin'],
			'required': True,
		}
	}
}

DOMAIN = {'movies': movies,
		  'users': users}
