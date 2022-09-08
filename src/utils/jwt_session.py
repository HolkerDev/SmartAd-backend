from asyncio.log import logger
import jwt

# Please, don't use it :(
SECRET = "test-secret"


def generate_token(claims: dict) -> str:
    """Method generates jwt token based on [claims] param"""
    return jwt.encode(payload=claims, key=SECRET)


def is_valid_token(token: str) -> bool:
    try:
        jwt.decode(token, key=SECRET, algorithms=["HS256"])
    except jwt.DecodeError as err:
        logger.error("Error during jwt validation '%s'", err)
        return False
    return True
