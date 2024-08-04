from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str = None
    date_of_birth: datetime = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CustomerProfileBase(BaseModel):
    customer_id: int
    profile_data: str

class CustomerProfileCreate(CustomerProfileBase):
    pass

class CustomerProfile(CustomerProfileBase):
    profile_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CustomerSegmentBase(BaseModel):
    customer_id: int
    segment_id: int

class CustomerSegmentCreate(CustomerSegmentBase):
    pass

class CustomerSegment(CustomerSegmentBase):
    customer_segment_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ActivityBase(BaseModel):
    customer_id: int
    activity_type: str
    activity_data: str = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    activity_id: int
    occurred_at: datetime

    class Config:
        orm_mode = True

class SalesTransactionBase(BaseModel):
    customer_id: int
    product_id: int
    sale_date: datetime
    sale_price: float
    quantity: int
    total_amount: float

class SalesTransactionCreate(SalesTransactionBase):
    pass

class SalesTransaction(SalesTransactionBase):
    transaction_id: int

    class Config:
        orm_mode = True

class CompetitorPricingBase(BaseModel):
    competitor_id: int
    product_id: int
    competitor_price: float

class CompetitorPricingCreate(CompetitorPricingBase):
    pass

class CompetitorPricing(CompetitorPricingBase):
    competitor_pricing_id: int
    date_collected: datetime

    class Config:
        orm_mode = True

class MarketTrendBase(BaseModel):
    product_id: int
    trend_data: str

class MarketTrendCreate(MarketTrendBase):
    pass

class MarketTrend(MarketTrendBase):
    trend_id: int
    collected_at: datetime

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    product_name: str
    category: str
    base_price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PricingStrategyBase(BaseModel):
    product_id: int
    segment_id: int
    strategy_description: str

class PricingStrategyCreate(PricingStrategyBase):
    pass

class PricingStrategy(PricingStrategyBase):
    strategy_id: int
    effective_date: datetime

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict(), created_at=datetime.utcnow())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.post("/customer_profiles/", response_model=CustomerProfile)
def create_customer_profile(profile: CustomerProfileCreate, db: Session = Depends(get_db)):
    db_profile = CustomerProfile(**profile.dict(), created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.get("/customer_profiles/{profile_id}", response_model=CustomerProfile)
def read_customer_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(CustomerProfile).filter(CustomerProfile.profile_id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@app.post("/customer_segments/", response_model=CustomerSegment)
def create_customer_segment(segment: CustomerSegmentCreate, db: Session = Depends(get_db)):
    db_segment = CustomerSegment(**segment.dict(), created_at=datetime.utcnow())
    db.add(db_segment)
    db.commit()
    db.refresh(db_segment)
    return db_segment

@app.get("/customer_segments/{customer_segment_id}", response_model=CustomerSegment)
def read_customer_segment(customer_segment_id: int, db: Session = Depends(get_db)):
    db_segment = db.query(CustomerSegment).filter(CustomerSegment.customer_segment_id == customer_segment_id).first()
    if db_segment is None:
        raise HTTPException(status_code=404, detail="Segment not found")
    return db_segment

@app.post("/activities/", response_model=Activity)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = Activity(**activity.dict(), occurred_at=datetime.utcnow())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@app.get("/activities/{activity_id}", response_model=Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = db.query(Activity).filter(Activity.activity_id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@app.post("/sales_transactions/", response_model=SalesTransaction)
def create_sales_transaction(transaction: SalesTransactionCreate, db: Session = Depends(get_db)):
    db_transaction = SalesTransaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/sales_transactions/{transaction_id}", response_model=SalesTransaction)
def read_sales_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(SalesTransaction).filter(SalesTransaction.transaction_id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.post("/competitor_pricing/", response_model=CompetitorPricing)
def create_competitor_pricing(pricing: CompetitorPricingCreate, db: Session = Depends(get_db)):
    db_pricing = CompetitorPricing(**pricing.dict(), date_collected=datetime.utcnow())
    db.add(db_pricing)
    db.commit()
    db.refresh(db_pricing)
    return db_pricing

@app.get("/competitor_pricing/{competitor_pricing_id}", response_model=CompetitorPricing)
def read_competitor_pricing(competitor_pricing_id: int, db: Session = Depends(get_db)):
    db_pricing = db.query(CompetitorPricing).filter(CompetitorPricing.competitor_pricing_id == competitor_pricing_id).first()
    if db_pricing is None:
        raise HTTPException(status_code=404, detail="Competitor pricing not found")
    return db_pricing

@app.post("/market_trends/", response_model=MarketTrend)
def create_market_trend(trend: MarketTrendCreate, db: Session = Depends(get_db)):
    db_trend = MarketTrend(**trend.dict(), collected_at=datetime.utcnow())
    db.add(db_trend)
    db.commit()
    db.refresh(db_trend)
    return db_trend

@app.get("/market_trends/{trend_id}", response_model=MarketTrend)
def read_market_trend(trend_id: int, db: Session = Depends(get_db)):
    db_trend = db.query(MarketTrend).filter(MarketTrend.trend_id == trend_id).first()
    if db_trend is None:
        raise HTTPException(status_code=404, detail="Market trend not found")
    return db_trend

@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict(), created_at=datetime.utcnow())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.post("/pricing_strategies/", response_model=PricingStrategy)
def create_pricing_strategy(strategy: PricingStrategyCreate, db: Session = Depends(get_db)):
    db_strategy = PricingStrategy(**strategy.dict(), effective_date=datetime.utcnow())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@app.get("/pricing_strategies/{strategy_id}", response_model=PricingStrategy)
def read_pricing_strategy(strategy_id: int, db: Session = Depends(get_db)):
    db_strategy = db.query(PricingStrategy).filter(PricingStrategy.strategy_id == strategy_id).first()
    if db_strategy is None:
        raise HTTPException(status_code=404, detail="Pricing strategy not found")
    return db_strategy

