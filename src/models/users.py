from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import BaseModel

if TYPE_CHECKING:
    from .meals import MealLog


class Role(BaseModel):

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f'<Role(id={self.id}, name="{self.name}")>'

    # Consider using Pydantic schemas for serialization instead of to_dict
    def to_dict(self) -> dict:
        """Returns a dictionary representation of the Role."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class User(BaseModel):
    """Represents a user account in the system."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    profile_picture: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Increased length
    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # Store hashed password
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=False, default=4
    )  # Ensure role ID 4 exists

    # Relationships
    role: Mapped["Role"] = relationship(
        "Role", back_populates="users", lazy="joined"
    )  # Eager load role
    otp_codes: Mapped[List["UserOTP"]] = relationship(
        "UserOTP", back_populates="user", cascade="all, delete-orphan", lazy="select"
    )
    meal_logs: Mapped[List["MealLog"]] = relationship(
        "MealLog", back_populates="user", lazy="select"
    )

    @property
    def full_name(self) -> str:
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def activate_user(self) -> "User":
        self.is_active = True
        return self

    def __repr__(self) -> str:
        return f'<User(id={self.id}, email="{self.email}", is_active={self.is_active})>'

    # Consider using Pydantic schemas for serialization
    def to_dict(self) -> dict:
        """Returns a dictionary representation of the User (excluding password)."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "profile_picture": self.profile_picture,
            "email": self.email,
            "is_active": self.is_active,
            "role_id": self.role_id,
            # Include role name if needed, requires role to be loaded
            "role_name": self.role.name if self.role else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserOTP(BaseModel):
    """Stores One-Time Passwords (OTP) for user verification."""

    __tablename__ = "user_otp"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    otp_code: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # Store OTP as string if needed
    # Use server_default for dynamic defaults like current time + delta
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        # server_default=func.now() + datetime.timedelta(minutes=5) # Use server-side default if possible
        # Python-side default factory (less ideal for distributed systems):
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=5),
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="otp_codes", lazy="select"
    )

    def is_expired(self) -> bool:
        """Checks if the OTP has expired."""
        # Ensure comparison is timezone-aware
        return datetime.datetime.now(datetime.timezone.utc) >= self.expires_at

    def __repr__(self) -> str:
        return f"<UserOTP(id={self.id}, user_id={self.user_id}, expired={self.is_expired()})>"

    # Consider using Pydantic schemas for serialization
    def to_dict(self) -> dict:
        """Returns a dictionary representation of the UserOTP."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            # "otp_code": self.otp_code, # Avoid exposing OTP code
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
