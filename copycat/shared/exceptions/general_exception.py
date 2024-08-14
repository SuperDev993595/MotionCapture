class GeneralException(Exception):
    def __init__(self):
        super().__init__("This exception throws a general error")
