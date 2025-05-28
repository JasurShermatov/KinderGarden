from fastapi import Depends, HTTPException, status
from src.tasks.email import send_verification_email

from src.services.user_otp_service import UserOTPService  # Renamed from controller
from src.services.user_repository import (
    UserRepository,
)
from src.schemas.users_schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserConfirmationSchema,
    UserResendSchema,
    UserLoginSchema,
    UserReadSchemaWithToken,
)
from src.utils.security import JWTHandler, Security


class AuthenticationService:

    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        otp_service: UserOTPService = Depends(),
    ):
        self.__user_repository = user_repository
        self.__user_otp_service = otp_service
        self.__jwt_handler = JWTHandler(self.__user_repository)
        self.__security = Security()

    async def _validate_user_input(self, payload: UserCreateSchema) -> None:
        if not self.__security.email_is_valid(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format."
            )
        if not self.__security.check_password_strength(payload.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet strength requirements.",
            )
        existing_user = await self.__user_repository.get_user_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

    async def _generate_auth_tokens(self, user_data: dict) -> dict:

        payload_data = {
            k: v
            for k, v in user_data.items()
            if k not in ("password", "hashed_password")
        }
        return self.__jwt_handler.create_tokens(payload_data)

    async def register_user(self, payload: UserCreateSchema) -> UserReadSchema:
        await self._validate_user_input(payload)

        hashed_password = self.__security.hash_password(payload.password)
        user_data_to_create = payload.model_dump()
        user_data_to_create["password"] = hashed_password

        new_user = await self.__user_repository.register_user(user_data_to_create)

        otp_code = self.__security.generate_otp()
        await self.__user_otp_service.create_user_otp(new_user.id, otp_code)

        send_verification_email.delay(new_user.email, otp_code)

        return UserReadSchema.model_validate(new_user)

    async def confirm_otp(self, payload: UserConfirmationSchema) -> UserReadSchema:
        """Confirms user registration using the provided OTP."""
        user = await self.__user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        is_valid_otp = await self.__user_otp_service.check_user_otp(
            user.id, payload.otp_code
        )
        if not is_valid_otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP code.",
            )

        return UserReadSchema.model_validate(user)

    async def resend_otp(self, payload: UserResendSchema) -> UserReadSchema:
        user = await self.__user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        otp_code = self.__security.generate_otp()
        await self.__user_otp_service.create_user_otp(user.id, otp_code)
        send_verification_email.delay(user.email, otp_code)

        return UserReadSchema.model_validate(user)

    async def login_user(self, payload: UserLoginSchema) -> UserReadSchemaWithToken:
        """Authenticates a user and returns user data with tokens."""
        user = await self.__user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )

        if not self.__security.verify_password(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )

        user_dict = UserReadSchema.model_validate(user).model_dump()
        tokens = await self._generate_auth_tokens(user_dict)

        return UserReadSchemaWithToken(**user_dict, **tokens)

    async def refresh_tokens(self, refresh_token: str) -> dict[str, str]:
        try:
            new_tokens = self.__jwt_handler.refresh_access_token(refresh_token)
            return new_tokens
        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error refreshing token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not refresh token.",
            )
