from fastapi import APIRouter, Depends, status

from src.services.authentication_service import (
    AuthenticationService,
)
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
    "/otp/confirm",  # Simplified path
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
    summary="Confirm user registration with OTP",
)
async def confirm_otp(
    payload: UserConfirmationSchema,
    auth_service: AuthenticationService = Depends(),
) -> UserReadSchema:
    """Confirms a user's registration using the provided OTP."""
    return await auth_service.confirm_otp(payload)


@router.post(
    "/otp/resend",  # Simplified path
    status_code=status.HTTP_200_OK,  # Typically 200 OK for resend
    response_model=UserReadSchema,  # Or perhaps just a success message?
    summary="Resend OTP for user confirmation",
)
async def resend_otp(
    payload: UserResendSchema,
    auth_service: AuthenticationService = Depends(),
) -> UserReadSchema:
    """Resends the OTP to the user's registered email/phone."""
    # Assuming resend_otp returns the user schema, adjust if needed
    return await auth_service.resend_otp(payload)


@router.post(
    "/login",  # Simplified path
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchemaWithToken,
    summary="Login a user",
)
async def login_user(
    payload: UserLoginSchema,
    auth_service: AuthenticationService = Depends(),
) -> UserReadSchemaWithToken:
    """Authenticates a user and returns access/refresh tokens."""
    return await auth_service.login_user(payload)


@router.post(
    "/refresh",  # Simplified path
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],  # Assuming it returns new tokens
    summary="Refresh access token",
)
async def refresh_token(
    payload: RefreshTokenSchema,
    auth_service: AuthenticationService = Depends(),
):
    return await auth_service.refresh_tokens(payload.refresh_token)
