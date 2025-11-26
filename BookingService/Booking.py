from fastapi import APIRouter, HTTPException, status
from .schemas import FlightBooking, FlightBookingCreate
from BookingService.modelsdb import init_db

@app.on_event("startup")
def on_startup():
    init_db()

FlightService = APIRouter()

bookings = []

@FlightService.post("/api/flights/book", status_code=status.HTTP_201_CREATED)
def create_booking(booking: FlightBookingCreate):
    new_booking = FlightBooking(booking_id=len(bookings) + 1, **booking.model_dump())
    bookings.append(new_booking)
    return new_booking

@FlightService.get("/api/flights", status_code=status.HTTP_200_OK)
def get_all_bookings():
    return {"bookings": bookings, "count": len(bookings)}

@FlightService.get("/api/flights/{booking_id}", status_code=status.HTTP_200_OK)
def get_booking(booking_id: int):
    for b in bookings:
        if b.booking_id == booking_id:
            return b
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Booking not found"
    )

@FlightService.put("/api/flights/{booking_id}", status_code=status.HTTP_200_OK)
def update_booking(booking_id: int, updated: FlightBookingCreate):
    for idx, b in enumerate(bookings):
        if b.booking_id == booking_id:
            bookings[idx] = FlightBooking(booking_id=booking_id, **updated.model_dump())
            return {
                "message": f"Booking {booking_id} updated successfully", 
                "booking": bookings[idx]
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Booking not found"
    )

@FlightService.delete("/api/flights/book/{booking_id}", status_code=status.HTTP_200_OK)
def delete_booking(booking_id: int):
    for booking in bookings:
        if booking.booking_id == booking_id:
            bookings.remove(booking)
            return {
                "message": "Booking deleted successfully",
                "booking_id": booking_id
            }
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Booking not found"
    )