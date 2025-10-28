# Wellspring Mountain - Updates Summary

## Contact Information Updated

✅ **Email**: SpringMountainWellness@proton.me
✅ **Phone**: 743-241-6310

Updated in:
- Main application sidebar
- Email notification system
- All documentation

---

## Facilities Database Completely Reorganized

### New Total: 36 Units

#### Residential Houses (2 units - Bookable)
- House 1 (Neighbor House) - 4 beds
- House 2 (Easley House) - 4 beds

#### Lodge Rooms (9 units - Bookable)
**Downstairs:**
- Lodge Room 1-4 (Private rooms)
- Lodge Dormroom (6 people capacity - 3 bunkbeds)

**Upstairs:**
- Lodge Room 5-7 (Private rooms)
- Lodge Shared Room (4 people - 2 bunkbeds)

#### Lodge Facilities (2 units - Non-bookable)
- Lodge Upstairs (Facilities)
- Lodge Downstairs (Facilities)

#### Uptown Cabins (5 units - Bookable)
- Uptown Cabin 1-5
- Uptown Cabins Area (Facilities)

#### Downtown Cabins (4 units - Bookable)
- Downtown Cabin 1 (Woodshed)
- Downtown Cabin 2 (Craft)
- Downtown Cabin 3 (Caboose)
- Downtown Cabin 4 (Woodshop)

#### A-frame Cabins (4 units - Bookable)
- A-frame Cabin 1-4 (3 beds each)

#### Common Facilities (9 units - Non-bookable)
- A-frame Classroom (15 capacity)
- Artist Studio (1 bed)
- Showerhouse (Facilities)
- Community Kitchen
- Dining Hall (Facilities)
- Laundry Room
- Apothecary
- Shop
- Road Maintenance

---

## Email Notification System

### Automatic Notifications For:
✅ Property notes created
✅ Maintenance tasks created
✅ New booking requests
✅ Road maintenance requests

### Where Notifications Show Up:
1. **Email** - Sent to SpringMountainWellness@proton.me (when SMTP configured)
2. **Log File** - notification_log.txt (current active method)
3. **Staff Dashboard** - Visible in Property Management sections

### To Enable Email Sending:
Add to `.env` file:
```
SMTP_SERVER=smtp.protonmail.com
SMTP_PORT=587
SMTP_USERNAME=SpringMountainWellness@proton.me
SMTP_PASSWORD=your_app_password
```

Then uncomment the email sending code in `utils/email_notifications.py`

---

## Property Management Enhancements

### All Facilities Now Have:
✅ **Info/Notes Section** - Document utilities, improvements, specifications
✅ **Maintenance Request Area** - Submit and track issues
✅ **Outstanding Issues Display** - View open problems
✅ **Resolution Documentation** - Mark issues as resolved with notes
✅ **Photo Upload Capability** - Add photos to any facility
✅ **File Attachments** - Store manuals, warranties, documents

### Accessing Facility Management:
1. Login to Staff Dashboard (`staff2024`)
2. Navigate to "Property Management"
3. Choose tab:
   - **Overview**: Quick metrics
   - **Maintenance**: All maintenance tasks
   - **Notes**: Property documentation
   - **Files**: Photo and document uploads
   - **Buildings**: Individual facility management

### Individual Building View:
Each facility has dedicated tabs:
- 📝 **Notes**: Building-specific documentation
- 📁 **Files**: Photos, manuals, documents
- 🔧 **Maintenance**: Task history and open issues

---

## Road Maintenance System

Special facility type for infrastructure requests:
- Submit road/infrastructure maintenance requests
- Track priority and status
- Automatic email notifications
- Visible in Property Management > Maintenance

---

## File Uploads & Photos

### Supported File Types:
- Photos: JPG, PNG
- Documents: PDF, DOC, TXT

### File Categories:
- Photos (building images)
- Documents (contracts, permits)
- Manuals (equipment guides)
- Warranties
- Floor Plans

### Where to Upload:
1. Property Management > Files tab (global)
2. Property Management > Buildings > Select building > Files tab (per-building)

---

## Database Changes

### Script Created:
`update_facilities.py` - Run to update/reset facility database

### To Reset Database:
```bash
python update_facilities.py
```

This will:
- Clear old data
- Add all 36 facilities with correct names
- Organize by type and location
- Set appropriate capacities

---

## Booking System Updates

### Dormroom Capacity:
- Lodge Dormroom now correctly shows 6 person capacity
- Description clarifies "3 bunkbeds"

### Shared Room Capacity:
- Lodge Shared Room shows 4 person capacity
- Description clarifies "2 bunkbeds"

### Facility Types:
- Bookable units: houses, lodge rooms, cabins, studio
- Non-bookable: facilities (maintenance/management only)

---

## What Shows Where

### Staff Notes Visibility:

**When You Create a Note:**
1. **Immediate**: Shows in Property Management > Notes tab
2. **Building View**: Shows in specific building's Notes tab
3. **Email**: Notification sent (or logged to notification_log.txt)
4. **Log File**: Permanently recorded with timestamp

**To View Notes:**
- Global view: Property Management > Notes
- Per-building: Property Management > Buildings > [Select building] > Notes tab
- Recent notes: Property Management > Overview dashboard

### Maintenance Tasks Visibility:

**When You Create a Task:**
1. **Immediate**: Shows in Property Management > Maintenance tab
2. **Building View**: Shows in specific building's Maintenance tab
3. **Email**: Notification sent with priority and details
4. **Dashboard**: Count shows in Overview metrics

**To View Tasks:**
- All tasks: Property Management > Maintenance (grouped by building type)
- Per-building: Property Management > Buildings > [Select building] > Maintenance tab
- Priority tasks: Sorted by priority (critical, high, medium, low)

---

## Testing Checklist

### Contact Info:
- [ ] Sidebar shows correct phone: 743-241-6310
- [ ] Sidebar shows correct email: SpringMountainWellness@proton.me

### Facilities:
- [ ] 36 total units in database
- [ ] Correct cabin names (Woodshed, Craft, Caboose, Woodshop)
- [ ] Houses show as "Neighbor House" and "Easley House"
- [ ] Lodge Dormroom shows 6 capacity
- [ ] All 9 new facilities present (Artist Studio, Community Kitchen, etc.)

### Property Management:
- [ ] Can create notes on any facility
- [ ] Can create maintenance tasks
- [ ] Can upload files (photos/documents)
- [ ] Individual building view works
- [ ] Email notifications log to notification_log.txt

### Email Notifications:
- [ ] Creating note generates log entry
- [ ] Creating maintenance task generates log entry
- [ ] Log file contains all details
- [ ] Ready to enable SMTP when configured

---

## Next Steps

### To Fully Enable Email:
1. Get ProtonMail app password
2. Add SMTP credentials to .env
3. Uncomment email sending code
4. Test notifications

### To Add Photos:
1. Navigate to Property Management > Files
2. Select building
3. Choose photo category
4. Upload JPG/PNG file
5. Add description
6. Save

### To Track Maintenance:
1. Go to Property Management > Maintenance
2. Click "Create New Maintenance Task"
3. Select building (including Road Maintenance)
4. Fill in details (type, priority, date)
5. Submit
6. Check notification_log.txt for email log

---

## Files Modified/Created

### Modified:
- `app.py` - Contact info updated
- `database/property_operations.py` - Email notifications integrated
- `.streamlit/config.toml` - Hide sidebar navigation

### Created:
- `update_facilities.py` - Database reorganization script
- `utils/email_notifications.py` - Email notification system
- `UPDATES_SUMMARY.md` - This file

### Database:
- `wellspring_bookings.db` - Completely reorganized with 36 facilities

---

## Support

**Phone**: 743-241-6310
**Email**: SpringMountainWellness@proton.me

**System Access:**
- Public Booking: `wellspring2024`
- Staff Dashboard: `staff2024`

**Technical Issues:**
- Check notification_log.txt for email logs
- Run `python test_system.py` to verify system
- Review DEPLOYMENT.md for configuration help

---

*Last Updated: January 2025*
*Version: 2.1 - Facility Management Enhanced*
