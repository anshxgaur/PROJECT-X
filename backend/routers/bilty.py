from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
import models
from schemas import BiltyCreate, BiltyResponse, BiltyUpdate, BiltyStatusEnum

router = APIRouter(prefix="/api/bilty", tags=["Bilty"])

@router.post("/create", response_model=BiltyResponse, status_code=status.HTTP_201_CREATED)
def create_bilty(bilty: BiltyCreate, db: Session = Depends(get_db)):
    """Create a new bilty (transport document)"""
    # Verify company exists
    company = db.query(models.Company).filter(models.Company.id == bilty.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify route exists
    route = db.query(models.Route).filter(models.Route.id == bilty.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Calculate total amount
    total_amount = route.distance_km * bilty.rate_per_km
    
    # Create bilty
    db_bilty = models.Bilty(
        bilty_number=bilty.bilty_number,
        company_id=bilty.company_id,
        route_id=bilty.route_id,
        sender_name=bilty.sender_name,
        sender_address=bilty.sender_address,
        receiver_name=bilty.receiver_name,
        receiver_address=bilty.receiver_address,
        goods_description=bilty.goods_description,
        weight_kg=bilty.weight_kg,
        rate_per_km=bilty.rate_per_km,
        total_amount=total_amount,
        scheduled_pickup=bilty.scheduled_pickup,
        scheduled_delivery=bilty.scheduled_delivery,
        status=BiltyStatusEnum.PENDING
    )
    
    db.add(db_bilty)
    db.commit()
    db.refresh(db_bilty)
    return db_bilty

@router.get("/{bilty_id}", response_model=BiltyResponse)
def get_bilty(bilty_id: int, db: Session = Depends(get_db)):
    """Get bilty by ID"""
    bilty = db.query(models.Bilty).filter(models.Bilty.id == bilty_id).first()
    if not bilty:
        raise HTTPException(status_code=404, detail="Bilty not found")
    return bilty

@router.get("", response_model=list[BiltyResponse])
def list_bilties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all bilties"""
    bilties = db.query(models.Bilty).offset(skip).limit(limit).all()
    return bilties

@router.put("/{bilty_id}", response_model=BiltyResponse)
def update_bilty(bilty_id: int, bilty_update: BiltyUpdate, db: Session = Depends(get_db)):
    """Update bilty"""
    db_bilty = db.query(models.Bilty).filter(models.Bilty.id == bilty_id).first()
    if not db_bilty:
        raise HTTPException(status_code=404, detail="Bilty not found")
    
    if bilty_update.status:
        db_bilty.status = bilty_update.status
    if bilty_update.sender_name:
        db_bilty.sender_name = bilty_update.sender_name
    if bilty_update.receiver_name:
        db_bilty.receiver_name = bilty_update.receiver_name
    if bilty_update.goods_description:
        db_bilty.goods_description = bilty_update.goods_description
    
    db_bilty.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_bilty)
    return db_bilty

@router.delete("/{bilty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bilty(bilty_id: int, db: Session = Depends(get_db)):
    """Delete bilty"""
    db_bilty = db.query(models.Bilty).filter(models.Bilty.id == bilty_id).first()
    if not db_bilty:
        raise HTTPException(status_code=404, detail="Bilty not found")
    
    db.delete(db_bilty)
    db.commit()
    return None
