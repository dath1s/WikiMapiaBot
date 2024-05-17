import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

password: str = config['DEFAULT']['password']
username: str = config['DEFAULT']['username']
bot_token: str = config['DEFAULT']['bot_token']
