"""
Module: Hotel Reservation System
This module provides classes and methods
for managing hotels, customers, and reservations.
"""

import json
import os
from typing import List
import unittest


class Hotel:
    """
    Class representing a hotel with attributes
    for identification, location, and rooms.
    """
    def __init__(self, hotel_id: int, name: str, location: str, rooms: int):
        """Initialize a new Hotel instance."""
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms
        self.reservations = []

    def to_dict(self):
        """Convert the Hotel instance to a dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
            "reservations": self.reservations
        }

    @staticmethod
    def from_dict(data: dict):
        """Create a Hotel instance from a dictionary."""
        hotel = Hotel(data['hotel_id'],
                      data['name'], data['location'], data['rooms'])
        hotel.reservations = data['reservations']
        return hotel


class Customer:
    """
    Class representing a customer
    with attributes like ID, name, and email.
    """
    def __init__(self, customer_id: int, name: str, email: str):
        """Initialize a new Customer instance."""
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Convert the Customer instance to a dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def from_dict(data: dict):
        """Create a Customer instance from a dictionary."""
        return Customer(data['customer_id'], data['name'], data['email'])


class Reservation:
    """Class representing a reservation with customer and hotel references."""
    def __init__(self, reservation_id: int, customer_id: int, hotel_id: int):
        """Initialize a new Reservation instance."""
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convert the Reservation instance to a dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id
        }

    @staticmethod
    def from_dict(data: dict):
        """Create a Reservation instance from a dictionary."""
        return Reservation(data['reservation_id'],
                           data['customer_id'], data['hotel_id'])


class DataManager:
    """Class to manage data persistence with file operations."""
    @staticmethod
    def save_to_file(filename: str, data: List[dict]):
        """Save a list of dictionaries to a specified file."""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file)

    @staticmethod
    def load_from_file(filename: str):
        """Load a list of dictionaries from a specified file."""
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading file {filename}: {e}")
            return []


class HotelReservationSystem:
    """
    Main system to manage hotels,
    customers, and reservations.
    """
    HOTELS_FILE = 'hotels.json'
    CUSTOMERS_FILE = 'customers.json'
    RESERVATIONS_FILE = 'reservations.json'

    def __init__(self):
        """Initialize the HotelReservationSystem by loading existing data."""
        self.hotels = [
            Hotel.from_dict(h)
            for h in DataManager.load_from_file(self.HOTELS_FILE)
        ]
        self.customers = [
            Customer.from_dict(c)
            for c in DataManager.load_from_file(self.CUSTOMERS_FILE)
        ]
        self.reservations = [
            Reservation.from_dict(r)
            for r in DataManager.load_from_file(self.RESERVATIONS_FILE)
        ]

    def _save_all(self):
        """
        Save all hotels, customers,
        and reservations to their respective files.
        """
        DataManager.save_to_file(self.HOTELS_FILE, [
            h.to_dict()
            for h in self.hotels
            ]
            )
        DataManager.save_to_file(self.CUSTOMERS_FILE, [
            c.to_dict()
            for c in self.customers
            ]
            )
        DataManager.save_to_file(self.RESERVATIONS_FILE, [
            r.to_dict()
            for r in self.reservations
            ]
            )

    def create_hotel(self, hotel: Hotel):
        """Create a new hotel and save changes."""
        self.hotels.append(hotel)
        self._save_all()

    def delete_hotel(self, hotel_id: int):
        """Delete a hotel by its ID and save changes."""
        self.hotels = [h for h in self.hotels if h.hotel_id != hotel_id]
        self._save_all()

    def display_hotel(self, hotel_id: int):
        """Display hotel information by ID."""
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                return hotel.to_dict()
        return None

    def modify_hotel(self, hotel_id: int, name: str = None,
                     location: str = None, rooms: int = None):
        """Modify hotel details based on provided parameters."""
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                if name:
                    hotel.name = name
                if location:
                    hotel.location = location
                if rooms:
                    hotel.rooms = rooms
        self._save_all()

    def reserve_room(self, reservation: Reservation):
        """Create a reservation and add it to the system."""
        self.reservations.append(reservation)
        for hotel in self.hotels:
            if hotel.hotel_id == reservation.hotel_id:
                hotel.reservations.append(reservation.customer_id)
        self._save_all()

    def cancel_reservation(self, reservation_id: int):
        """Cancel an existing reservation."""
        self.reservations = [
            r for r in self.reservations
            if r.reservation_id != reservation_id
        ]
        for hotel in self.hotels:
            hotel.reservations = [
                cid for cid in hotel.reservations
                if cid != reservation_id
            ]
        self._save_all()

    def create_customer(self, customer: Customer):
        """Create a new customer and save changes."""
        self.customers.append(customer)
        self._save_all()

    def delete_customer(self, customer_id: int):
        """Delete a customer by ID."""
        self.customers = [
            c for c in self.customers
            if c.customer_id != customer_id
            ]
        self._save_all()

    def display_customer(self, customer_id: int):
        """Display customer information by ID."""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer.to_dict()
        return None

    def modify_customer(self, customer_id: int,
                        name: str = None, email: str = None):
        """Modify customer details based on provided parameters."""
        for customer in self.customers:
            if customer.customer_id == customer_id:
                if name:
                    customer.name = name
                if email:
                    customer.email = email
        self._save_all()


class TestHotelReservationSystem(unittest.TestCase):
    """Test suite for the HotelReservationSystem class."""
    def setUp(self):
        """Set up the test environment."""
        self.system = HotelReservationSystem()
        self.hotel = Hotel(1, "Test Hotel", "Test City", 10)
        self.customer = Customer(1, "Test User", "test.user@example.com")
        self.reservation = Reservation(1, 1, 1)

    def test_create_hotel(self):
        """Test creating a new hotel."""
        self.system.create_hotel(self.hotel)
        self.assertEqual(self.system.display_hotel(1)['name'], "Test Hotel")

    def test_create_customer(self):
        """Test creating a new customer."""
        self.system.create_customer(self.customer)
        self.assertEqual(self.system.display_customer(1)['name'], "Test User")

    def test_create_reservation(self):
        """Test creating a new reservation."""
        self.system.create_hotel(self.hotel)
        self.system.create_customer(self.customer)
        self.system.reserve_room(self.reservation)
        self.assertTrue(any(
            r.reservation_id == 1 for r in self.system.reservations
            )
            )

    def test_modify_hotel(self):
        """Test modifying hotel details."""
        self.system.create_hotel(self.hotel)
        self.system.modify_hotel(1, name="Updated Hotel")
        self.assertEqual(self.system.display_hotel(1)['name'], "Updated Hotel")

    def test_delete_customer(self):
        """Test deleting a customer."""
        self.system.create_customer(self.customer)
        self.system.delete_customer(1)
        self.assertIsNone(self.system.display_customer(1))

    def test_cancel_reservation(self):
        """Test canceling a reservation."""
        self.system.create_hotel(self.hotel)
        self.system.create_customer(self.customer)
        self.system.reserve_room(self.reservation)
        self.system.cancel_reservation(1)
        self.assertFalse(any(
            r.reservation_id == 1 for r in self.system.reservations
            )
            )


if __name__ == "__main__":
    unittest.main()
