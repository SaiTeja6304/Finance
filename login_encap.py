class Register:
    def __init__(self, usname, usemail, usdob, usnum, uspwd):
        self.usname = usname
        self.usemail = usemail
        self.usdob = usdob
        self.usnum = usnum
        self.uspwd = uspwd

    #setter methods
    def set_usname(self, usname):
        self._usname = usname

    def set_usemail(self, usemail):
        self._usemail = usemail

    def set_usdob(self, usdob):
        self._usdob = usdob

    def set_usnum(self, usnum):
        self._usnum = usnum

    def set_uspwd(self, uspwd):
        self._uspwd = uspwd

    #getter methods
    def get_usname(self):
        return self._usname

    def get_usemail(self):
        return self._usemail

    def get_usdob(self):
        return self._usdob

    def get_usnum(self):
        return self._usnum

    def get_uspwd(self):
        return self._uspwd