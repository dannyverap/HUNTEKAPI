from typing import Optional
from pydantic import UUID4, BaseModel

# Shared properties
class RoleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    name: Optional[str]
    description: Optional[str]


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class Role(RoleInDBBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "traveler",
                "description": "traveler can only book your own trips",
            }
        }


class RoleInDB(RoleInDBBase):
    pass


# Shared properties
class UserRoleBase(BaseModel):
    user_id: Optional[UUID4]
    role_id: Optional[UUID4]


# Properties to receive via API on creation
class UserRoleCreate(UserRoleBase):
    pass


# Properties to receive via API on update
class UserRoleUpdate(BaseModel):
    role_id: UUID4


class UserRoleInDBBase(UserRoleBase):
    role: Role

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserRole(UserRoleInDBBase):
    pass


class UserRoleInDB(UserRoleInDBBase):
    pass
