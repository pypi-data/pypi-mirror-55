from notazz.base import NotazzBase


class NFeWrapper(NotazzBase):

    def __init__(self, *args, **kwargs):
        super(NFeWrapper, self).__init__(*args, **kwargs)
        raise NotImplemented('This is not implemented baby! :)')
