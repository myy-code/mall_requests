


class ResultBase:
    def __init__(self):
        self.success: bool = False
        self.msg: str = ""
        self.error: str = ""
        self.response = None
        self.token : str = ""
        self.code : int = 200
