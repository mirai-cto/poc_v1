import os

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = False
    TESTING = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'step', 'stp'}
    
    # Feature detection settings
    FEATURE_TOLERANCE = 0.001  # 1 micron tolerance for coordinate comparison
    MESH_DEFLECTION = 0.1  # Linear deflection for mesh generation

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    # Production-specific settings
    DEBUG = False
    # Add production-specific settings here
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # DATABASE_URL = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 