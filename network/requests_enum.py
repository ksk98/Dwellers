from enum import Enum


class RequestsEnum(Enum):
    # Requests
    # - Objects
    REQUEST_OBJECT_LOBBY = 100
    # - General
    REQUEST_GENERAL_JOIN = 200
    REQUEST_GENERAL_EXIT = 201
    REQUEST_GENERAL_RENEW = 202

    # Responses
    # - Object
    RESPONSE_OBJECT_LOBBY = 300

    # Updates
    # - Lobby
    UPDATE_LOBBY_JOIN = 400
    UPDATE_LOBBY_EXIT = 401
