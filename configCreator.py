import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {'BOT_TOKEN': 'TOKEN',
                     'USERNAME': 'username',
                     'PASSWORD': 'password'}

with open('settings.ini', 'w') as configfile:
    config.write(configfile)
