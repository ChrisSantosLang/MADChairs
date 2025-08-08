from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='MADChairs_session', num_demo_participants=None, app_sequence=['WaitingRoom', 'MADChairs', 'PostGame'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['time', 'skill_rating', 'disconnected', 'finished']
SESSION_FIELDS = ['prolific_completion_url']
ROOMS = [dict(name='mc', display_name='mc')]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


