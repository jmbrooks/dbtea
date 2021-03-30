class DbteaException(Exception):
    """Exception related to dbtea configuration, processing or compatibility."""

    exit_code = 100

    def __init__(self, name: str, title: str, detail: str):
        self.type: str = "/errors/" + name
        self.title = title
        self.detail = detail

    def __repr__(self) -> str:
        return self.title

    def __str__(self) -> str:
        return self.title + " " + self.detail
