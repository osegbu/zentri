from fastapi import APIRouter, Depends
from models.User import CreateUser, UpdateUser, LoginUser, UserResponse, Auth
from db.db import SessionDep
from api.controller.UserController import create_user, login_user, fetch_user, update_user, auth
from utils.jwt_utils import decode_access_token

user_routes = APIRouter()

@user_routes.post(
    "/users/signup", 
    summary="Register a new user", 
    description="Creates a new user account using the provided registration details."
)
def create_user_endpoint(user_data: CreateUser, session: SessionDep):
    return create_user(user_data, session)

@user_routes.post(
    "/users/login", 
    summary="Login user", 
    description="Authenticates a user with their credentials and provides an access token."
)
def login_user_endpoint(user_data: LoginUser, session: SessionDep):
    return login_user(user_data, session)

@user_routes.get(
    "/users/me", 
    response_model=Auth, 
    summary="Fetch the logged in user", 
    description="Retrieves the details of the currently logged in user"
)
def auth_endpoint(session: SessionDep, token: dict = Depends(decode_access_token)):
    return auth(token['id'], session)


@user_routes.get(
    "/users/{user_name}", 
    response_model=UserResponse, 
    summary="Fetch user details", 
    description="Retrieves the details of a user based on their username."
)
def fetch_user_endpoint(user_name: str, session: SessionDep):
    return fetch_user(user_name, session)

@user_routes.patch(
    "/users/update", 
    summary="Update user information", 
    description="Updates the details of an existing user based on the provided user ID."
)
def update_user_endpoint(user_data: UpdateUser, session: SessionDep, token: dict = Depends(decode_access_token)):
    return update_user(token['id'], user_data, session)
