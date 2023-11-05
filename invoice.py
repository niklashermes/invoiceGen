class Invoice(object):
    def __init__(self, *args, **kwargs):
        self._service = ""
        self._pretty_service = ""
        self._shipping = ""
        self._pretty_shipping = ""
        self._specials = ""
        self._pretty_specials = ""
        self._setup = ""
        self._pretty_setup = ""
        self._email_header = ""
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        result = ""
        for i in range(8):
            if "_pretty" in self.__dir__()[i] and getattr(self, self.__dir__()[i]) != "":
                result += getattr(self, self.__dir__()[i]) + "\n"
        return result.rstrip()

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    @service.deleter
    def service(self):
        del self._service

    @property
    def pretty_service(self):
        return self._pretty_service

    @pretty_service.setter
    def pretty_service(self, pretty_service):
        self._pretty_service = pretty_service

    @pretty_service.deleter
    def pretty_service(self):
        del self._pretty_service

    @property
    def shipping(self):
        return self._shipping

    @shipping.setter
    def shipping(self, shipping):
        self._shipping = shipping

    @shipping.deleter
    def shipping(self):
        del self._shipping

    @property
    def pretty_shipping(self):
        return self._pretty_shipping

    @pretty_shipping.setter
    def pretty_shipping(self, pretty_shipping):
        self._pretty_shipping = pretty_shipping

    @pretty_shipping.deleter
    def pretty_shipping(self):
        del self._pretty_shipping

    @property
    def specials(self):
        return self._specials

    @specials.setter
    def specials(self, specials):
        self._specials = specials

    @specials.deleter
    def specials(self):
        del self._specials

    @property
    def pretty_specials(self):
        return self._pretty_specials

    @pretty_specials.setter
    def pretty_specials(self, pretty_specials):
        self._pretty_specials = pretty_specials

    @pretty_specials.deleter
    def pretty_specials(self):
        del self._pretty_specials

    @property
    def setup(self):
        return self._setup

    @setup.setter
    def setup(self, setup):
        self._setup = setup

    @setup.deleter
    def setup(self):
        del self._setup

    @property
    def pretty_setup(self):
        return self._pretty_setup

    @pretty_setup.setter
    def pretty_setup(self, pretty_setup):
        self._pretty_setup = pretty_setup

    @pretty_setup.deleter
    def pretty_setup(self):
        del self._pretty_setup

    @property
    def email_header(self):
        return self._email_header

    @email_header.setter
    def email_header(self, email_header):
        self._email_header = email_header

    @email_header.deleter
    def email_header(self):
        del self._email_header


