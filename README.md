# Wellspring Mountain Booking System

A comprehensive, production-ready booking and property management system built with Streamlit.

## Overview

This system manages bookings for various lodging options at Wellspring Mountain, including:
- 🏠 **Refuge** stays (up to 3 months)
- 🌿 **Respite** stays (up to 3 weeks)
- 👥 **Group retreats** for nonprofits/corporations

## Key Features

### Booking Management
- Password-protected public booking interface
- Staff dashboard for managing bookings and availability
- Real-time availability checking across 31+ lodging units
- No payment processing - contact-based confirmation
- Comprehensive booking status tracking and reporting

### Property Management System ✨ NEW
- 🔧 **Maintenance Tracking**: Task management with priorities and scheduling
- 📝 **Property Notes**: Documentation system for all buildings
- ✅ **Task Management**: Todo lists with categories and assignments
- 📁 **File Management**: Upload and organize building documents/photos
- 📊 **Dashboard Analytics**: Metrics and summaries
- 🏗️ **Individual Building Management**: Dedicated views for each property
- 🔍 **Inspection Records**: Track property inspections and compliance

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

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd "Wellspring Mountain"

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit .env and set your passwords
# PUBLIC_PASSWORD=your_secure_password
# STAFF_PASSWORD=your_secure_password
```

### 3. Initialize Database

```bash
python init_database.py
```

### 4. Run Tests

```bash
python test_system.py
```

### 5. Start Application

```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

## Deployment

### Streamlit Cloud (Recommended)
See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

Quick steps:
1. Push to GitHub
2. Connect to share.streamlit.io
3. Configure secrets in dashboard
4. Deploy!

### Other Platforms
- **Heroku**: Uses Procfile and setup.sh
- **Docker**: Uses Dockerfile and docker-compose.yml
- **DigitalOcean**: App Platform compatible

Full deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

## Documentation

- 📖 **[User Manual](USER_MANUAL.md)** - Complete user guide
- 🚀 **[Deployment Guide](DEPLOYMENT.md)** - Deployment instructions
- ✅ **[Production Checklist](PRODUCTION_CHECKLIST.md)** - Pre-deployment checklist
- 🏗️ **[System Design](SYSTEM_DESIGN.md)** - Architecture overview

## Database

Uses SQLite for simplicity and cloud compatibility.

**Schema includes:**
- Lodging units and capacity
- Booking requests and status tracking
- Property notes and documentation
- Maintenance tasks and schedules
- Todo lists and assignments
- File attachments
- Property inspections

## Testing

Automated test suite included:

```bash
python test_system.py
```

Tests cover:
- Database operations
- Booking workflows
- Property management
- Helper functions
- Configuration validation

## Project Structure

```
├── app.py                          # Main application
├── config.py                       # Configuration management
├── test_system.py                  # Automated tests
├── database/
│   ├── models.py                   # Database schema
│   ├── operations.py               # Booking operations
│   └── property_operations.py     # Property management ops
├── pages/
│   ├── booking.py                  # Public interface
│   ├── staff.py                    # Staff dashboard
│   └── property_management.py     # Property management
├── utils/
│   ├── auth.py                     # Authentication
│   ├── helpers.py                  # Helper functions
│   └── styles.py                   # UI styling
├── .streamlit/
│   ├── config.toml                 # Streamlit config
│   └── secrets.toml.example       # Secrets template
├── Dockerfile                      # Docker configuration
├── docker-compose.yml             # Docker Compose
├── Procfile                        # Heroku configuration
├── DEPLOYMENT.md                   # Deployment guide
├── USER_MANUAL.md                 # User documentation
└── PRODUCTION_CHECKLIST.md        # Pre-deployment checklist
```

## Technology Stack

- **Framework**: Streamlit 1.48.1
- **Database**: SQLite3
- **Python**: 3.8+
- **Styling**: Custom CSS (Airbnb-inspired)
- **Testing**: Custom test suite

## Security

- Password-protected access (public & staff)
- Input sanitization on all user inputs
- SQL injection prevention
- Environment variable management
- Secure session handling

See [DEPLOYMENT.md](DEPLOYMENT.md) for security best practices.

## Support

- **System Issues**: Open an issue in the repository
- **Wellspring Mountain**: (555) 123-4567
- **Email**: info@wellspringmountain.org

## Version History

- **v2.0** (Current): Property management system, production features
- **v1.0** (Initial): Basic booking system

## License

Copyright © 2025 Wellspring Mountain. All rights reserved.

---

## Contributors

Built with [Claude Code](https://claude.com/claude-code)