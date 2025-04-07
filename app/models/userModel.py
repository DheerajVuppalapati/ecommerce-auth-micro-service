import uuid
from datetime import datetime

from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, Enum, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum


from app.enums.roles_enums import RoleEnum
from app.enums.user_status_enums import UserStatusEnum
from app.cores.database import Base

class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(SqlEnum(RoleEnum, name="role_enum"), nullable=False)
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    status = Column(SqlEnum(UserStatusEnum, name="user_status_enum"), default="active")
    created_on = Column(TIMESTAMP, default=datetime.utcnow)
    modified_on = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    password_hash = Column(String, nullable=False)

    role = relationship("Role", back_populates="users")
    addresses = relationship("Address", back_populates="user")
    auth_tokens = relationship("AuthToken", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    logs = relationship("AuditLog", back_populates="user")
    login_methods = relationship("UserLoginMethod", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"
    address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    entity_type = Column(Enum("user", "business", name="entity_type_enum"), nullable=False)
    address_type = Column(Enum("home", "work", name="address_type_enum"), nullable=False)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")

class AuthToken(Base):
    __tablename__ = "auth_tokens"
    auth_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    provider = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="auth_tokens")

class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    login_method_id = Column(Integer, ForeignKey("login_methods.login_method_id"), nullable=False)
    session_token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expires_at = Column(TIMESTAMP, nullable=False)
    status = Column(Enum("active", "expired", "revoked", name="session_status_enum"), default="active")

    user = relationship("User", back_populates="sessions")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    event_type = Column(String, nullable=False)
    event_details = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")

class OTPVerification(Base):
    __tablename__ = "otp_verification"
    otp_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    otp_code = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expires_at = Column(TIMESTAMP, nullable=False)
    purpose = Column(Enum("login", "signup", "password_reset", name="otp_purpose_enum"), nullable=False)

class UserLoginMethod(Base):
    __tablename__ = "user_login_methods"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    login_method_id = Column(Integer, ForeignKey("login_methods.login_method_id"), primary_key=True)
    details = Column(JSON, nullable=True)

    user = relationship("User", back_populates="login_methods")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expires_at = Column(TIMESTAMP, nullable=False)

class LoginMethod(Base):
    __tablename__ = "login_methods"
    login_method_id = Column(Integer, primary_key=True, index=True)
    method_name = Column(String, unique=True, nullable=False)
