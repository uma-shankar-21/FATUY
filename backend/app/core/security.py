from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext


# ==========================================================
# DJANGO PASSWORD HASH SUPPORT
# ==========================================================

password_context = CryptContext(
    schemes=[
        "django_pbkdf2_sha256",
        "django_pbkdf2_sha1",
        "django_bcrypt_sha256",
        "django_argon2",
        "bcrypt",
    ],
    deprecated="auto",
)


# ==========================================================
# JWT CONFIG
# ==========================================================

SECRET_KEY = "CHANGE_THIS_TO_YOUR_ENV_SECRET"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ==========================================================
# PASSWORD
# ==========================================================

def hash_password(
    password: str,
) -> str:

    return password_context.hash(
        password,
        scheme="bcrypt",
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return password_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# ACCESS TOKEN
# ==========================================================

def create_access_token(
    data: dict,
) -> str:

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload.update({
        "exp": expire,
        "type": "access",
    })

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ==========================================================
# REFRESH TOKEN
# ==========================================================

def create_refresh_token(
    data: dict,
) -> str:

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    payload.update({
        "exp": expire,
        "type": "refresh",
    })

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ==========================================================
# DECODE TOKEN
# ==========================================================

def decode_token(
    token: str,
) -> dict:

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:

        raise ValueError(
            "Invalid or expired token."
        )