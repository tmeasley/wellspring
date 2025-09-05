# System Design - Wellspring Mountain Booking System

## Architecture Overview

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Database**: SQLite (file-based, cloud-friendly)
- **Deployment**: Streamlit Cloud
- **Authentication**: Session-based with password protection

### User Types & Access Levels

1. **Public Users** (Password Protected)
   - Submit booking requests
   - View availability calendar
   - Specify booking type (refuge/respite/retreat)

2. **Staff Users** (Admin Password Protected)  
   - View all booking requests
   - Manage availability
   - Update booking status
   - View occupancy dashboard

### Booking Flow

```
Public User → Password Entry → Booking Type Selection → 
Date/Duration → Lodging Selection → Contact Info → 
Request Submission → Staff Review → Phone Confirmation
```

## Database Schema

### Tables

#### `lodging_units`
- `id` (PRIMARY KEY)
- `name` (VARCHAR) - e.g., "Lodge Room 1"
- `location` (VARCHAR) - Lodge/Uptown/Downtown/A-frame
- `type` (VARCHAR) - private/shared/dorm/classroom
- `capacity` (INTEGER) - number of beds
- `is_active` (BOOLEAN)

#### `booking_requests`
- `id` (PRIMARY KEY)  
- `guest_name` (VARCHAR)
- `email` (VARCHAR)
- `phone` (VARCHAR)
- `booking_type` (VARCHAR) - refuge/respite/retreat
- `check_in` (DATE)
- `check_out` (DATE)
- `guests` (INTEGER)
- `lodging_unit_id` (FOREIGN KEY)
- `status` (VARCHAR) - pending/confirmed/cancelled
- `notes` (TEXT)
- `created_at` (TIMESTAMP)

#### `availability_calendar`
- `id` (PRIMARY KEY)
- `lodging_unit_id` (FOREIGN KEY)
- `date` (DATE)
- `is_available` (BOOLEAN)
- `notes` (TEXT)

### Business Logic

#### Booking Rules
- **Refuge**: Up to 3 months duration
- **Respite**: Up to 3 weeks duration  
- **Retreat**: Group bookings, flexible duration
- No double-booking prevention at request level (staff handles conflicts)

#### Availability Logic
- Real-time availability checking
- Staff can manually block dates
- Automatic calendar updates based on confirmed bookings

## User Interface Design

### Public Interface (`/booking`)
1. **Authentication Page**: Password entry
2. **Booking Type**: Refuge/Respite/Retreat selection
3. **Date Selection**: Check-in/out with duration limits
4. **Accommodation**: Available lodging options
5. **Guest Info**: Contact details and requirements
6. **Confirmation**: Request summary and submission

### Staff Interface (`/staff`)  
1. **Dashboard**: Current occupancy and pending requests
2. **Booking Management**: View/update request status
3. **Availability Management**: Block/unblock dates
4. **Reports**: Occupancy rates and booking analytics

## Security Considerations

- Password-based authentication (stored in environment variables)
- No user registration/accounts (session-based)
- Input validation and sanitization
- No financial data storage
- Secure deployment practices for Streamlit Cloud

## Deployment Architecture

### Streamlit Cloud Deployment
- Automatic deployment from Git repository
- Environment variables for sensitive data
- SQLite database persistence via cloud storage
- Session state management for user authentication

### Configuration Files
- `streamlit_config.toml`: Streamlit settings
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (local development)

## Future Enhancements

- Email notifications for booking confirmations
- Calendar integration (Google Calendar, Outlook)
- SMS notifications for staff
- Advanced reporting and analytics
- Integration with existing property management systems
- Mobile-responsive design improvements