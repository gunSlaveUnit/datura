from utils.crypt import crypt_context


async def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)
