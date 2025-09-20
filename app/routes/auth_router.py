from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenRefreshRequest, LogoutRequest
from app.core.dependencies import get_auth_service
from app.core.security.token_service import TokenService
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.register(data.email, data.username, data.password)
    return {"id": user.id, "email": user.email, "username": user.username}


@router.post("/login")
def login(data: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(data.email, data.password)


@router.post("/refresh")
def refresh_tokens(data: TokenRefreshRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.refresh_tokens(data.refresh_token)


@router.post("/refresh-access")
def refresh_access(data: TokenRefreshRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.refresh_access_token(data.refresh_token)


@router.post("/logout")
def logout(data: LogoutRequest, auth_service: AuthService = Depends(get_auth_service)):
    payload = TokenService().decode_token(data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    auth_service.logout(user_id, data.refresh_token)
    return {"detail": "Successfully logged out"}
