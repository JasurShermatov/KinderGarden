from fastapi import APIRouter, Depends, status
from src.services.authentication_service import AuthenticationService
from src.schemas.users_schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserConfirmationSchema,
    UserResendSchema,
    UserLoginSchema,
    UserReadSchemaWithToken,
    RefreshTokenSchema,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserReadSchema,
    summary="Register a new user",
)
async def register_user(
    payload: UserCreateSchema,
    auth_service: AuthenticationService = Depends(),
):
    return await auth_service.register_user(payload)


@router.post(
    "/otp/confirm/",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
    summary="Confirm user registration with OTP",
)
async def confirm_otp(
    payload: UserConfirmationSchema,
    auth_service: AuthenticationService = Depends(),
) -> UserReadSchema:
    return await auth_service.confirm_otp(payload)


@router.post(
    "/otp/resend/",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
    summary="Resend OTP for user confirmation",
)
async def resend_otp(
    payload: UserResendSchema,
    auth_service: AuthenticationService = Depends(),
) -> UserReadSchema:
    return await auth_service.resend_otp(payload)


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchemaWithToken,
    summary="Login a user",
)
async def login_user(
    payload: UserLoginSchema,
    auth_service: AuthenticationService = Depends(),
) -> UserReadSchemaWithToken:
    return await auth_service.login_user(payload)


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
)
async def refresh_token(
    payload: RefreshTokenSchema,
    auth_service: AuthenticationService = Depends(),
):
    return await auth_service.refresh_tokens(payload.refresh_token)
