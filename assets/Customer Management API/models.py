from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship
from database import Base
from datetime import datetime, date


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(15))
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    profiles = relationship("CustomerProfile", back_populates="customer")
    segments = relationship("CustomerSegment", back_populates="customer")
    activities = relationship("Activity", back_populates="customer")
    sales_transactions = relationship("SalesTransaction", back_populates="customer")

class CustomerProfile(Base):
    __tablename__ = 'customer_profiles'

    profile_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    profile_data = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="profiles")

class CustomerSegment(Base):
    __tablename__ = 'customer_segments'

    customer_segment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    segment_id = Column(Integer, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="segments")
    pricing_strategies = relationship("PricingStrategy", back_populates="segment")

    __table_args__ = (UniqueConstraint('segment_id', name='_segment_id_uc'),)

class Activity(Base):
    __tablename__ = 'activities'

    activity_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    activity_type = Column(String(100), nullable=False)
    activity_data = Column(String(500))
    occurred_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="activities")

class SalesTransaction(Base):
    __tablename__ = 'sales_transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)
    sale_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates="sales_transactions")
    product = relationship("Product", back_populates="sales_transactions")

class CompetitorPricing(Base):
    __tablename__ = 'competitor_pricing'

    competitor_pricing_id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    competitor_price = Column(Float, nullable=False)
    date_collected = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="competitor_pricing")

class MarketTrend(Base):
    __tablename__ = 'market_trends'

    trend_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    trend_data = Column(String(500), nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="market_trends")

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    base_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales_transactions = relationship("SalesTransaction", back_populates="product")
    competitor_pricing = relationship("CompetitorPricing", back_populates="product")
    market_trends = relationship("MarketTrend", back_populates="product")
    pricing_strategies = relationship("PricingStrategy", back_populates="product")

class PricingStrategy(Base):
    __tablename__ = 'pricing_strategies'

    strategy_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    segment_id = Column(Integer, ForeignKey('customer_segments.customer_segment_id'), nullable=False)
    strategy_description = Column(String(500), nullable=False)
    effective_date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="pricing_strategies")
    segment = relationship("CustomerSegment", back_populates="pricing_strategies")
