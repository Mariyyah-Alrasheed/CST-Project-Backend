from pydantic import BaseModel
from datetime import date
from typing import Optional


# === Beneficiary ===
class BeneficiaryBase(BaseModel):
    name: str
    national_id: str
    phone: str
    nationality: str

class BeneficiaryCreate(BeneficiaryBase):
    pass

class BeneficiaryOut(BeneficiaryBase):
    id: int
    class Config:
        from_attributes = True


# === Suspended Beneficiary ===
class SuspendedBeneficiaryCreate(BaseModel):
    beneficiary_id: int
    suspended_at: date

class SuspendedBeneficiaryOut(SuspendedBeneficiaryCreate):
    id: int
    class Config:
        from_attributes = True


class SuspendedBeneficiaryWithBeneficiaryOut(SuspendedBeneficiaryOut):
    beneficiary: BeneficiaryOut

    class Config:
        from_attributes = True


class SuspendedBeneficiaryListResponse(BaseModel):
    data: list[SuspendedBeneficiaryWithBeneficiaryOut]
    total: int
# === Company ===
class CompanyBase(BaseModel):
    name: str
    commercial_number: str
    unified_number: str
    type: str  # "sales" or "installation"

class CompanyCreate(CompanyBase):
    pass

class CompanyOut(CompanyBase):
    id: int

    class Config:
        from_attributes = True

class CompanyListResponse(BaseModel):
    data: list[CompanyOut]
    total: int


# === Company Employee ===
class CompanyEmployeeBase(BaseModel):
    name: str
    national_id: str
    job_number: str
    nationality: str
    phone: str
    company_id: int

class CompanyEmployeeCreate(CompanyEmployeeBase):
    pass

class CompanyEmployeeOut(CompanyEmployeeBase):
    id: int
    class Config:
        from_attributes = True

# === Employee List Response ===
class EmployeeListResponse(BaseModel):
    data: list[CompanyEmployeeOut]
    total: int

# === Suspended Employee ===
class SuspendedEmployeeCreate(BaseModel):
    employee_id: int
    suspended_at: date

class CompanySimpleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        
class CompanyEmployeeWithCompanyOut(BaseModel):
    id: int
    name: str
    national_id: str
    job_number: str
    nationality: str
    phone: str
    company: CompanySimpleOut  # بدل company_id

    class Config:
        from_attributes = True
class SuspendedEmployeeOut(BaseModel):
    id: int
    suspended_at: date
    employee: CompanyEmployeeWithCompanyOut

    class Config:
        from_attributes = True

# === Suspended Employee List Response ===
class SuspendedEmployeeListResponse(BaseModel):
    data: list[SuspendedEmployeeOut]
    total: int


# === Service Provider ===
class ServiceProviderBase(BaseModel):
    name: str
    code: str
    company_id: int

class ServiceProviderCreate(ServiceProviderBase):
    pass

class ServiceProviderOut(ServiceProviderBase):
    id: int
    class Config:
        from_attributes = True


# === Employee Service Provider ===
class EmployeeServiceProviderCreate(BaseModel):
    employee_id: int
    provider_id: int
    assigned_at: date

class EmployeeServiceProviderOut(EmployeeServiceProviderCreate):
    id: int
    class Config:
        from_attributes = True

# class CompanySimpleOut(BaseModel):
#     id: int
#     name: str

#     class Config:
#         from_attributes = True
# class CompanyEmployeeWithCompanyOut(BaseModel):
#     id: int
#     name: str
#     national_id: str
#     job_number: str
#     nationality: str
#     phone: str
#     company: CompanySimpleOut  # بدل company_id

#     class Config:
#         from_attributes = True
# class SuspendedEmployeeOut(BaseModel):
#     id: int
#     suspended_at: date
#     employee: CompanyEmployeeWithCompanyOut

#     class Config:
#         from_attributes = True

# class SuspendedEmployeeListResponse(BaseModel):
#     data: list[SuspendedEmployeeOut]
#     total: int
