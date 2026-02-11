from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from auth.auth_manager import auth_manager

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip docs and openapi
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)

        # Get Bearer token from Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid Authorization header")

        token = auth_header.replace("Bearer ", "").strip()
        
        # Validate the token using auth_manager
        is_valid, user_data, error_message = auth_manager.validate_token_for_middleware(token)
        
        if not is_valid:
            raise HTTPException(status_code=401, detail=f"Unauthorized: {error_message}")

        # Store user data in request state for use in endpoints
        request.state.user = user_data
        request.state.token = token

        response = await call_next(request)
        return response