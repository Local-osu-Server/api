from fastapi import Request


def get_database_engine(request: Request):
    return request.app.state.db
