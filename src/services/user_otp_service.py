from fastapi import Depends, HTTPException, status
import logging

# Updated imports for the new structure
from src.services.user_repository import (
    UserRepository,
)  # Assuming repository handles data access
from src.services.user_otp_repository import (
    UserOtpRepository,
)  # Assuming repository handles data access
from src.models.users import User, UserOTP  # Import models

# Setup logger
logger = logging.getLogger(__name__)


class UserOTPService:
    """Provides services for managing User One-Time Passwords (OTP)."""

    def __init__(
        self,
        user_otp_repository: UserOtpRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        """Initializes the UserOTPService with necessary repositories."""
        self.__user_otp_repository = user_otp_repository
        self.__user_repository = user_repository

    async def _get_user_or_404(self, user_id: int) -> User:
        """Retrieves a user by ID or raises HTTPException 404 if not found."""
        user = await self.__user_repository.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found.",
            )
        return user

    async def create_user_otp(self, user_id: int, otp_code: int) -> UserOTP:
        """Creates a new OTP record for a given user."""
        await self._get_user_or_404(user_id)  # Ensure user exists
        await self.delete_user_otps(user_id)
        try:
            user_otp = await self.__user_otp_repository.create_user_otp(
                user_id=user_id, otp_code=otp_code
            )
            logger.info(f"Created OTP for user ID {user_id}.")
            return user_otp
        except Exception as e:
            logger.error(f"Error creating OTP for user ID {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create OTP. ",
            )

    async def get_valid_user_otp(self, user_id: int) -> UserOTP | None:
        await self._get_user_or_404(user_id)
        user_otp = await self.__user_otp_repository.get_user_otp_by_user_id(user_id)
        if user_otp and not user_otp.is_expired():
            return user_otp
        return None

    async def delete_user_otps(self, user_id: int) -> None:
        """Deletes all OTP records associated with a user ID."""
        await self._get_user_or_404(user_id)
        try:
            await self.__user_otp_repository.delete_user_otps(user_id=user_id)
            logger.info(f"Deleted all OTPs for user ID {user_id}.")
        except Exception as e:
            logger.error(f"Error deleting OTPs for user ID {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not delete OTPs.",
            )

    async def check_user_otp(self, user_id: int, otp_code: int) -> bool:
        """Checks if the provided OTP is valid for the user and activates the user if valid."""
        user = await self._get_user_or_404(user_id)
        is_valid = await self.__user_otp_repository.check_user_otp(
            user_id=user_id, otp_code=otp_code
        )

        if is_valid:
            logger.info(f"Valid OTP provided for user ID {user_id}. Activating user.")
            # Activate user upon successful OTP verification
            await self.__user_repository.activate_user(user_id)
            # Optionally delete the used OTP
            await self.delete_user_otps(user_id)
            return True
        else:
            logger.warning(f"Invalid or expired OTP provided for user ID {user_id}.")
            return False
