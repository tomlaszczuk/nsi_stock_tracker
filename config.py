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


class TestingConfig(Config):
	TESTING = True


class ProductionConfig(Config):
	pass


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}