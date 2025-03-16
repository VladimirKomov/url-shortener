from fastapi import HTTPException

class URLNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Short URL not found")

class URLAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="This URL is already shortened")