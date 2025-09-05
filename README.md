# Wellspring Mountain Booking System

A Streamlit-based booking system for refuge, respite, and retreat center accommodations.

## Overview

This system manages bookings for various lodging options at Wellspring Mountain, including:
- Refuge stays (up to 3 months)
- Respite stays (up to 3 weeks) 
- Group retreats for nonprofits/corporations

## Features

- Password-protected public booking interface
- Staff dashboard for managing bookings and availability
- No payment processing - contact-based confirmation
- Real-time availability checking
- Lodging inventory management

## Lodging Inventory

### Lodge
- **Downstairs**: 4 private rooms + 1 dormroom (6 beds/3 bunkbeds)
- **Upstairs**: 3 private rooms + 1 shared room (4 beds/2 bunkbeds)

### Cabins
- **Uptown**: 5 cabins (1 bed each)
- **Downtown**: 3 cabins (1 bed each)
- **A-frame Camping**: 4 cabins (3 beds each)

### Facilities
- **A-frame Classroom**: Up to 15 people + instructor/guest loft

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

## Environment Variables

Create a `.env` file with:
```
PUBLIC_PASSWORD=your_public_password
STAFF_PASSWORD=your_staff_password
```

## Deployment

Configured for Streamlit Cloud deployment. See `streamlit_config.toml` for configuration.

## Database

Uses SQLite for simplicity and cloud compatibility. Database schema includes:
- Lodging units and capacity
- Booking requests and status
- User sessions and authentication

## Project Structure

```
├── app.py                 # Main Streamlit application
├── database/
│   ├── __init__.py
│   ├── models.py         # Database schema
│   └── operations.py     # Database operations
├── pages/
│   ├── __init__.py
│   ├── booking.py        # Public booking interface
│   └── staff.py          # Staff dashboard
├── utils/
│   ├── __init__.py
│   ├── auth.py          # Authentication utilities
│   └── helpers.py       # Helper functions
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── config.toml      # Streamlit configuration
└── README.md
```