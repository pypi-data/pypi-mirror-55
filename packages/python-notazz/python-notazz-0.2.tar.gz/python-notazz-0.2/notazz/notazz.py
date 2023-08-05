from notazz.base import NotazzBase
from notazz.nfe import NFeWrapper
from notazz.nfse import NFSeWrapper


class NotazzWrapper(NotazzBase):

    _nfse = None
    _nfe = None

    @property
    def nfe(self):
        if not self._nfe:
            self._nfe = NFeWrapper(self.api_key)
        return self._nfe

    @property
    def nfse(self):
        if not self._nfse:
            self._nfse = NFSeWrapper(self.api_key)
        return self._nfse

