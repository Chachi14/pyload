from pyload.plugins.MultiHoster import MultiHoster

class Premium4Me(MultiHoster):
    __name__ = "Premium4Me"
    __version__ = "0.03"
    __type__ = "account"
    __config__ = [("activated", "bool", "Activated", "False"),
                  ("hosterListMode", "all;listed;unlisted", "Use for downloads from supported hosters:", "all"),
                  ("hosterList", "str", "Hoster list (comma separated)", "")]
    __description__ = """Premium.to account plugin"""
    __author_name__ = ("RaNaN", "zoidberg", "stickell")
    __author_mail__ = ("RaNaN@pyload.org", "zoidberg@mujmail.cz", "l.stickell@yahoo.it")

    def loadAccountInfo(self, user, req):
        traffic = req.load("http://premium.to/api/traffic.php?authcode=%s" % self.authcode)

        account_info = {"trafficleft": int(traffic) / 1024,
                        "validuntil": -1}

        return account_info

    def login(self, user, data, req):
        self.authcode = req.load("http://premium.to/api/getauthcode.php?username=%s&password=%s" % (
                                 user, data["password"])).strip()

        if "wrong username" in self.authcode:
            self.wrongPassword()

    def loadHosterList(self, req):
        page = req.load("http://premium.to/api/hosters.php?authcode=%s" % self.authcode)
        return [x.strip() for x in page.replace("\"", "").split(";")]
