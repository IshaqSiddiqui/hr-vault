import os
import httpx
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

AUTH0_DOMAIN   = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ALGORITHMS     = ["RS256"]

bearer_scheme = HTTPBearer()


async def get_jwks() -> dict:
    """Fetch Auth0's public keys to verify JWT signatures."""
    url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        return res.json()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """
    Validate the Bearer JWT from the Authorization header.
    Returns the decoded token payload (claims) if valid.
    Raises HTTP 401 if invalid or expired.
    """
    token = credentials.credentials
    try:
        jwks = await get_jwks()
        payload = jwt.decode(
            token,
            jwks,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_role(payload: dict) -> str:
    """Extract the role from the Auth0 JWT custom claim."""
    # We'll set this namespace in Auth0 Actions (Phase 3)
    return payload.get("https://hr-vault/role", "employee")


def require_role(*allowed_roles: str):
    """
    Dependency factory — use like:
    Depends(require_role("admin", "hr_manager"))
    """
    async def _check(payload: dict = Depends(verify_token)):
        role = get_role(payload)
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' is not permitted for this action"
            )
        return payload
    return _check