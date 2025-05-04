from fastapi import APIRouter

router = APIRouter()

@router.post(
    '/register', 
    summary="Register a new user",
    description=""
)
async def register(): 
    ...

@router.post(
    '/login', 
    summary="Login and receive access/refresh tokens",
    description=""
)
async def login(): 
    ...
    

@router.post(
    '/refresh', 
    summary="Refresh access token",
    description=""
)
async def refresh(): 
    ...

@router.get(
    '/me', 
    summary="Get current user profile",
    description=""
)
async def me(): 
    ...
    
@router.get(
    '/logout', 
    summary="Logout and invalidate refresh token",
    description=""
)
async def logout(): 
    ...