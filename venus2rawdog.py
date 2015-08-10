import configparser
import os
import sys


RAWDOG_TEMPLATE = """
feed 30m {0}
    define_name {1}
    define_username {2}
    define_gravatar {3}"""


class Venus2Rawdog:

    def __init__(self):
        self.config = configparser.ConfigParser()

    def migrate(self, conf):
        self.config.read(conf)
        converted_feeds = []
        for section in self.config.sections():
            url = section
            try:
                name = self.config[section]['name']
                username = self.config[section]['username']
                gravatar = self.config[section]['gravatar']
            except KeyError:
                pass
            converted_feeds.append(
                RAWDOG_TEMPLATE.format(url, name, username, gravatar))
        return converted_feeds


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Not enough arguments. Please add path to config.")
        sys.exit(1)
    venus_conf = sys.argv[1]
    config = Venus2Rawdog()
    if os.path.isfile(venus_conf):
        feeds = config.migrate(conf=venus_conf)
        for feed in feeds:
            print(feed, end="")
    else:
        files_list = [os.path.join(dirpath, f) for dirpath, dirnames, fnames in os.walk(venus_conf) for f in fnames]
        for conf_file in files_list:
            feeds = config.migrate(conf=conf_file)
            for feed in feeds:
                print(feed, end="")
