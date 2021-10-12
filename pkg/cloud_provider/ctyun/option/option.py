from pkg.util.setting import setting


class Option(object):
    def __init__(self, name, access_key, security_key):
        tty_data = setting.get_tty_config()
        self.AccessKey = access_key
        self.SecurityKey = security_key
        self.name = name
        self.url = tty_data.get("Url")
        self.region_id = tty_data.get("RegionId")
