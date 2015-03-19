import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_string'
	STOCK_TRACKER_ADMIN = os.environ.get('STOCK_TRACKER_ADMIN')

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQL_ALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class PythonAnywhereConfig(Config):
    DEBUG = True
    SQL_ALCHEMY_DATABASE_URI = os.environ.get('PA_DATABASE_URL')


class TestingConfig(Config):
	TESTING = True
	SQL_ALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class ProductionConfig(Config):
	SQL_ALCHEMY_DATABASE_URI = os.environ.get('SQL_ALCHEMY_DATABASE_URI')


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}