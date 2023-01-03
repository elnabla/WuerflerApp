class ImageNotReadableError(Exception):
    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(ImageNotReadableError, self).__init__(arg1)


class LinesNotFoundError(Exception):
    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(LinesNotFoundError, self).__init__(arg1)


class CellExtractionError(Exception):
    def __init__(self, arg1, arg2=None):
        self.arg1 = arg1
        self.arg2 = arg2
        super(CellExtractionError, self).__init__(arg1)
