from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ProfileData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=2, max_length=80)
    phone: str = Field(default="", max_length=25)
    address: str = Field(default="", max_length=250)


class RegisterData(ProfileData):
    model_config = ConfigDict(str_strip_whitespace=False)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value):
        return value.strip() if isinstance(value, str) else value


class LoginData(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class CartItemData(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=1, le=99)


class OrderData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    request_id: str = Field(min_length=10, max_length=100)
    items: list[CartItemData] = Field(min_length=1, max_length=100)
    name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=10, max_length=25)
    delivery: Literal["pickup", "courier"]
    address: str = Field(default="", max_length=250)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not 10 <= len("".join(filter(str.isdigit, value))) <= 15:
            raise ValueError("Укажите телефон: от 10 до 15 цифр")
        return value
