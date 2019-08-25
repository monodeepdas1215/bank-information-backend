import configparser


def get_config(filename):
    config_dict = dict()
    config = configparser.ConfigParser()
    config.read(filename)

    for section in config.sections():
        config_dict.update(config[section].items())

    return config_dict


app_config = get_config('app_config.conf')