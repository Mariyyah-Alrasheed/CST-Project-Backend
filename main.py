from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from datetime import date, datetime
import models
import schemas
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from sqlalchemy import func
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from models import CompanyTypeEnum  # Assuming it's already imported
from sqlalchemy import cast, String
from sqlalchemy.orm import joinedload




app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكنك تحديد النطاقات المسموح بها هنا
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API متاحة. استخدمي المسارات مثل /company_employees و /stop_requests"}

@app.get("/service_providers", response_model=List[schemas.ServiceProviderOut])
async def list_service_providers(db: Session = Depends(get_db)):
    providers = db.query(models.ServiceProvider).all()
    return providers


# --- إدخال بيانات شركة ---
@app.post("/companies", response_model=schemas.CompanyOut)
async def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

# --- إدخال بيانات موظف في شركة ---
@app.post("/company_employees", response_model=schemas.CompanyEmployeeOut)
async def create_company_employee(company_employee: schemas.CompanyEmployeeCreate, db: Session = Depends(get_db)):
    db_company_employee = models.CompanyEmployee(**company_employee.dict())
    db.add(db_company_employee)
    db.commit()
    db.refresh(db_company_employee)
    return db_company_employee

# --- إدخال بيانات موظف موقوف ---
@app.post("/suspended_employees", response_model=schemas.SuspendedEmployeeOut)
async def create_suspended_employee(suspended_employee: schemas.SuspendedEmployeeCreate, db: Session = Depends(get_db)):
    db_suspended_employee = models.SuspendedEmployee(**suspended_employee.dict())
    db.add(db_suspended_employee)
    db.commit()
    db.refresh(db_suspended_employee)
    return db_suspended_employee


# --- إدخال بيانات مستفيد ---
@app.post("/beneficiaries", response_model=schemas.BeneficiaryOut)
async def create_beneficiary(beneficiary: schemas.BeneficiaryCreate, db: Session = Depends(get_db)):
    db_beneficiary = models.Beneficiary(**beneficiary.dict())
    db.add(db_beneficiary)
    db.commit()
    db.refresh(db_beneficiary)
    return db_beneficiary

# --- إدخال بيانات مستفيد موقوف ---
@app.post("/suspended_beneficiaries", response_model=schemas.SuspendedBeneficiaryOut)
async def create_suspended_beneficiary(suspended_beneficiary: schemas.SuspendedBeneficiaryCreate, db: Session = Depends(get_db)):
    db_suspended_beneficiary = models.SuspendedBeneficiary(**suspended_beneficiary.dict())
    db.add(db_suspended_beneficiary)
    db.commit()
    db.refresh(db_suspended_beneficiary)
    return db_suspended_beneficiary

# --- إدخال بيانات مزود خدمة ---
@app.post("/service_providers", response_model=schemas.ServiceProviderOut)
async def create_service_provider(service_provider: schemas.ServiceProviderCreate, db: Session = Depends(get_db)):
    db_service_provider = models.ServiceProvider(**service_provider.dict())
    db.add(db_service_provider)
    db.commit()
    db.refresh(db_service_provider)
    return db_service_provider

# --- تعيين موظف إلى مزود خدمة ---
@app.post("/employee_service_provider", response_model=schemas.EmployeeServiceProviderOut)
async def assign_employee_service_provider(employee_service_provider: schemas.EmployeeServiceProviderCreate, db: Session = Depends(get_db)):
    db_assignment = models.EmployeeServiceProvider(**employee_service_provider.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@app.get("/company_employees", response_model=schemas.EmployeeListResponse)
async def list_company_employees(
    skip: int = 0,
    limit: int = 100,
    search: str = Query("", description="Search by name, national_id, or job_number"),
    company_id: int = Query(None, description="Optional filter by company ID"),
    company_type: str = Query(None, description="Filter by company type: sales or installation"),
    db: Session = Depends(get_db)
):
    query = db.query(models.CompanyEmployee).join(models.Company)

    # Filter by company ID
    if company_id is not None:
        query = query.filter(models.CompanyEmployee.company_id == company_id)
        company_name = db.query(models.Company.name).filter(models.Company.id == company_id).scalar()
        

    # Filter by company type (sales or installation)
    if company_type:
        try:
            enum_value = CompanyTypeEnum(company_type)
            query = query.filter(models.Company.type == enum_value)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid company_type. Use 'sales' or 'installation'.")

    # Search by name, national_id, or job_number
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(models.CompanyEmployee.name).like(search_term),
                func.lower(models.CompanyEmployee.national_id).like(search_term),
                func.lower(models.CompanyEmployee.job_number).like(search_term),
            )
        )

    total = query.count()
    if total == 0:
        raise HTTPException(status_code=404, detail="No company employees found")

    employees = query.offset(skip).limit(limit).all()
    return {"total": total, "data": employees}

@app.get("/suspended_employees", response_model=schemas.SuspendedEmployeeListResponse)
async def list_suspended_employees(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search by national_id or job_number"),
    company_type: Optional[CompanyTypeEnum] = Query(None, description="Filter by company type: sales or installation"),
    db: Session = Depends(get_db)
):
    query = db.query(models.SuspendedEmployee).join(models.SuspendedEmployee.employee).join(models.CompanyEmployee.company)

    # فلترة بحسب نوع الشركة
    if company_type:
        query = query.filter(models.Company.type == company_type)

    # فلترة بحسب البحث
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(models.CompanyEmployee.national_id).like(search_term),
                func.lower(models.CompanyEmployee.job_number).like(search_term),
                func.lower(models.CompanyEmployee.name).like(search_term)
            )
        )

    total = query.count()
    if total == 0:
        raise HTTPException(status_code=404, detail="No suspended employees found")

    suspended_employees = query.offset(skip).limit(limit).all()
    return {"total": total, "data": suspended_employees}
# --- مثال: جلب كل مزودي الخدمة ---


# --- مثال: جلب كل الشركات ---
@app.get('/companies', response_model=schemas.CompanyListResponse)
async def list_companies(type: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if type not in ["sales", "installation"]:
        raise HTTPException(status_code=400, detail="Invalid company type")

    company_type = models.CompanyTypeEnum.sales if type == "sales" else models.CompanyTypeEnum.installation

    total = db.query(func.count(models.Company.id))\
              .filter(models.Company.type == company_type)\
              .scalar()

    if total == 0:
        raise HTTPException(status_code=404, detail=f"No {type} companies found")

    companies = db.query(models.Company)\
                  .filter(models.Company.type == company_type)\
                  .offset(skip)\
                  .limit(limit)\
                  .all()

    return {"total": total, "data": companies}


@app.get('/companies_sales', response_model=schemas.CompanyListResponse)
async def list_companies_sales(
    skip: int = 0,
    limit: int = 100,
    search: str = Query("", description="Search term to filter companies"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Company).filter(models.Company.type == models.CompanyTypeEnum.sales)

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(models.Company.name).like(search_term),
                func.lower(models.Company.commercial_number).like(search_term),
                func.lower(models.Company.unified_number).like(search_term)
            )
        )

    total = query.count()
    if total == 0:
        raise HTTPException(status_code=404, detail="No sales companies found")

    companies = query.offset(skip).limit(limit).all()

    return {"total": total, "data": companies}


@app.get('/companies_installation', response_model=schemas.CompanyListResponse)
async def list_companies_installation(
    skip: int = 0,
    limit: int = 100,
    search: str = Query("", description="Search term to filter companies"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Company).filter(models.Company.type == models.CompanyTypeEnum.installation)

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(models.Company.name).like(search_term),
                func.lower(models.Company.commercial_number).like(search_term),
                func.lower(models.Company.unified_number).like(search_term)
            )
        )

    total = query.count()
    if total == 0:
        raise HTTPException(status_code=404, detail="No installation companies found")

    companies = query.offset(skip).limit(limit).all()

    return {"total": total, "data": companies}


@app.get('/companies/{unified_number}', response_model=schemas.CompanyOut)
async def get_company(unified_number: str, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.unified_number == unified_number).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.get('/company_employees/{employee_id}', response_model=schemas.CompanyEmployeeOut)
async def get_company_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.CompanyEmployee).filter(models.CompanyEmployee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Company Employee not found")
    return employee

@app.get('/beneficiaries/{national_id}', response_model=schemas.BeneficiaryOut)
async def get_beneficiary(national_id: str, db: Session = Depends(get_db)):
    beneficiary = db.query(models.Beneficiary).filter(models.Beneficiary.national_id == national_id).first()
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return beneficiary

@app.get('/suspended_beneficiaries/{suspended_id}', response_model=schemas.SuspendedBeneficiaryOut)
async def get_suspended_beneficiary(suspended_id: int, db: Session = Depends(get_db)):
    suspended_beneficiary = db.query(models.SuspendedBeneficiary).filter(models.SuspendedBeneficiary.id == suspended_id).first()
    if not suspended_beneficiary:
        raise HTTPException(status_code=404, detail="Suspended Beneficiary not found")
    return suspended_beneficiary

@app.get('/beneficiaries', response_model=List[schemas.BeneficiaryOut])
async def list_beneficiaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    beneficiaries = db.query(models.Beneficiary).offset(skip).limit(limit).all()
    return beneficiaries

@app.get('/suspended_beneficiaries', response_model=schemas.SuspendedBeneficiaryListResponse)
async def list_suspended_beneficiaries(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.SuspendedBeneficiary).join(models.Beneficiary).filter(
        models.SuspendedBeneficiary.beneficiary_id == models.Beneficiary.id
    ).options(
        joinedload(models.SuspendedBeneficiary.beneficiary)
    )

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(cast(models.SuspendedBeneficiary.beneficiary_id, String)).like(search_term),
                func.lower(models.Beneficiary.name).like(search_term),
                func.lower(models.Beneficiary.national_id).like(search_term),
                func.lower(models.Beneficiary.phone).like(search_term),
            )
        )

    total = query.count()
    results = query.order_by(models.SuspendedBeneficiary.suspended_at.desc()).offset(skip).limit(limit).all()

    return {"total": total, "data": results}