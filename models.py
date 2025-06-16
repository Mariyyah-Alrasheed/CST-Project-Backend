from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import date
import enum


class CompanyTypeEnum(enum.Enum):
    sales = "sales"
    installation = "installation"


class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    national_id = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    nationality = Column(String, nullable=False)

    suspended = relationship("SuspendedBeneficiary", back_populates="beneficiary")

    def __repr__(self):
        return f"<Beneficiary(id={self.id}, name='{self.name}', national_id='{self.national_id}')>"


class SuspendedBeneficiary(Base):
    __tablename__ = "suspended_beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    beneficiary_id = Column(Integer, ForeignKey("beneficiaries.id"), nullable=False)
    suspended_at = Column(Date, default=date.today, nullable=False)

    beneficiary = relationship("Beneficiary", back_populates="suspended")

    def __repr__(self):
        return f"<SuspendedBeneficiary(id={self.id}, beneficiary_id={self.beneficiary_id})>"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    commercial_number = Column(String, nullable=False)
    unified_number = Column(String, nullable=False)
    type = Column(Enum(CompanyTypeEnum, name="company_type"), nullable=False)

    employees = relationship("CompanyEmployee", back_populates="company")
    service_providers = relationship("ServiceProvider", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', type='{self.type.name}')>"


class CompanyEmployee(Base):
    __tablename__ = "company_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    national_id = Column(String, unique=True, index=True, nullable=False)
    job_number = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = relationship("Company", back_populates="employees")
    suspended = relationship("SuspendedEmployee", back_populates="employee")
    services = relationship("EmployeeServiceProvider", back_populates="employee")

    def __repr__(self):
        return f"<CompanyEmployee(id={self.id}, name='{self.name}', national_id='{self.national_id}')>"


class SuspendedEmployee(Base):
    __tablename__ = "suspended_employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("company_employees.id"), nullable=False)
    suspended_at = Column(Date, default=date.today, nullable=False)

    employee = relationship("CompanyEmployee", back_populates="suspended")

    def __repr__(self):
        return f"<SuspendedEmployee(id={self.id}, employee_id={self.employee_id})>"


class ServiceProvider(Base):
    __tablename__ = "service_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = relationship("Company", back_populates="service_providers")
    assigned_employees = relationship("EmployeeServiceProvider", back_populates="provider")

    def __repr__(self):
        return f"<ServiceProvider(id={self.id}, name='{self.name}', code='{self.code}')>"


class EmployeeServiceProvider(Base):
    __tablename__ = "employee_service_provider"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("company_employees.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("service_providers.id"), nullable=False)
    assigned_at = Column(Date, default=date.today, nullable=False)

    employee = relationship("CompanyEmployee", back_populates="services")
    provider = relationship("ServiceProvider", back_populates="assigned_employees")

    def __repr__(self):
        return f"<EmployeeServiceProvider(id={self.id}, employee_id={self.employee_id}, provider_id={self.provider_id})>"
