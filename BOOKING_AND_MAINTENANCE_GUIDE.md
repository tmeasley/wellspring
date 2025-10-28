# Wellspring Mountain - Booking & Maintenance Guide

## Booking System Overview

### How It Works:

**For Guests (Public Booking):**
1. Guests submit an **inquiry** (not a reservation)
2. They can express preferences for specific rooms, but this is optional
3. The inquiry includes their needs, dates, and any special requests

**For Staff (Staff Dashboard):**
1. Review incoming inquiries in "Booking Requests"
2. Contact guest within 1-2 business days
3. **Staff assigns the actual room** using "Assign Rooms" page based on:
   - Availability (system shows only available units for requested dates)
   - Guest needs and special requests
   - Best fit for the situation
   - Capacity requirements
4. Update inquiry status: pending → confirmed (after room assignment)
5. Track active stays in "Active Stays" dashboard

### Room Assignment is ALWAYS Done by Staff

Guests cannot self-book specific rooms. Staff use their judgment to:
- Match guests with appropriate accommodations
- Balance capacity across different areas
- Consider special needs or circumstances
- Ensure community compatibility

### Staff Dashboard Features:

**Booking Requests** - Review and respond to new inquiries
**Active Stays** - Monitor guests currently checked in
**Assign Rooms** - Assign specific rooms to pending inquiries
**Manage Bookings** - View and export all bookings
**Availability** - Check room availability calendar

### Coming Soon:
- Guest agreement form (will be required before inquiry submission)

---

## Staff Room Assignment & Stay Tracking

### How to Assign Rooms to Inquiries:

1. **Navigate to "Assign Rooms"** in Staff Dashboard
2. **View pending inquiries** that need room assignment
3. **System automatically shows** only available accommodations for each inquiry's dates
4. **Review guest information:**
   - Dates requested
   - Number of guests
   - Special requests or needs
   - Booking type (refuge, respite, retreat)
5. **Select appropriate room** from available options grouped by location
6. **Click "Assign"** to assign the room
7. **Confirm the booking** to finalize

### Active Stays Dashboard:

**What It Shows:**
- All confirmed bookings where today falls between check-in and check-out dates
- Guest name and contact information
- Assigned room and location
- Days in residence and days remaining
- Special requests and notes

**What You Can Do:**
- Update notes about the guest's stay
- End a stay early if needed
- View full booking details
- Monitor all currently occupied rooms

### Room Assignment Best Practices:

1. **Check special requests first** - Accessibility needs, preferences
2. **Consider booking type:**
   - Refuge: Longer stays, may need more space
   - Respite: Short-term, balance community and privacy
   - Retreat: Groups, proximity matters
3. **Balance occupancy** across different areas
4. **Leave notes** for other staff about the assignment

---

## Maintenance/Work Request System

### How Work Requests Work:

**Creating a Maintenance Task:**
1. Staff Dashboard → Property Management → Maintenance tab
2. Click "Create New Maintenance Task"
3. Select building/facility (including Road Maintenance)
4. Fill in details:
   - Task description
   - Type (plumbing, electrical, etc.)
   - Priority (low, medium, high, critical)
   - Scheduled date
   - Estimated cost

**What Happens When You Create a Task:**

1. **Immediate Display:**
   - Task appears in Property Management > Maintenance tab
   - Grouped by building type
   - Shows in "Tasks by Building Type" section

2. **Email Notification:**
   - Logs to `notification_log.txt` immediately
   - Email sent to SpringMountainWellness@proton.me (when SMTP configured)
   - Includes all task details and priority

3. **Persistence:**
   - Task stays in system until marked completed
   - Shows as "pending" with ⏳ emoji
   - Updates to "in_progress" 🛠️ when work starts
   - Moves to "completed" ✅ when finished

4. **Visibility:**
   - Overview dashboard shows count of pending tasks
   - Individual building view shows task history
   - Can filter by status, priority, or building

**Priority Levels Explained:**

- 🟢 **Low**: Can wait, no urgency
- 🟡 **Medium**: Address soon, schedule within week
- 🔴 **High**: Urgent, needs attention within 1-2 days
- 🚨 **Critical**: Emergency, immediate action required

**Task Statuses:**

- ⏳ **Pending**: Not yet started
- 🛠️ **In Progress**: Currently being worked on
- ✅ **Completed**: Finished

### Road Maintenance Requests:

"Road Maintenance" is a special facility type for infrastructure:
- Accessible in Property Management > Maintenance
- Same process as building maintenance
- Use for: road repairs, drainage, signage, access issues
- Automatically triggers notifications
- Persistent until resolved

### Maintenance Request Flow:

```
1. Create Task
   ↓
2. Email Notification Sent (logged to notification_log.txt)
   ↓
3. Task Shows in:
   - Maintenance tab (all tasks)
   - Building-specific view
   - Overview dashboard (count)
   ↓
4. Staff/Contractor Works on It
   - Update status to "in_progress"
   ↓
5. Mark as Completed
   - Status changes to "completed"
   - Actual cost can be recorded
   - Completion notes added
   ↓
6. Task Archived
   - Still visible in maintenance history
   - Can view in individual building's maintenance tab
```

### Where to Find Maintenance Tasks:

**All Tasks:**
- Property Management > Maintenance tab
- Shows all tasks grouped by building type
- Filter by status (pending/in_progress/completed)

**Building-Specific:**
- Property Management > Buildings > [Select Building] > Maintenance tab
- Shows only tasks for that building
- Includes full history

**Dashboard Summary:**
- Property Management > Overview
- Shows count of pending maintenance
- Shows count of overdue maintenance

**Per-Building Quick View:**
- Property Management > Maintenance
- Expand building type section
- See recent tasks (up to 5 per section)

### Notes vs Maintenance Tasks:

**Notes** are for:
- Observations
- Documentation
- Guest feedback
- General information
- Safety concerns
- Ideas for improvements

**Maintenance Tasks** are for:
- Actual work that needs to be done
- Repairs
- Upgrades
- Scheduled maintenance
- Things with a completion state

Both trigger email notifications!

---

## Email Notifications

### What Gets Notified:

1. **Property Notes** - When staff documents something about a building
2. **Maintenance Tasks** - When a repair/work item is created
3. **Booking Inquiries** - When a guest submits an inquiry
4. **Road Maintenance** - Infrastructure requests

### Where Notifications Go:

**Currently:**
- All notifications log to `notification_log.txt`
- File includes timestamp, type, recipient, subject, full body
- Located in main project directory

**When SMTP Configured:**
- Emails send to SpringMountainWellness@proton.me
- Still also logs to file for backup
- Instant delivery

### Viewing Notification Log:

```bash
# View recent notifications
tail -n 50 notification_log.txt

# Search for specific building
grep "Lodge Room 1" notification_log.txt

# Search for maintenance tasks
grep "maintenance" notification_log.txt
```

### Enable Email Sending:

Add to `.env`:
```
SMTP_SERVER=smtp.protonmail.com
SMTP_PORT=587
SMTP_USERNAME=SpringMountainWellness@proton.me
SMTP_PASSWORD=your_protonmail_app_password
```

Then uncomment sending code in `utils/email_notifications.py`

---

## Booking Status Meanings

### ⏳ PENDING
- Initial inquiry submitted
- Awaiting staff review
- Need to contact guest

### ✅ CONFIRMED
- Staff approved the inquiry
- Room assigned
- Guest knows they're coming

### ❌ CANCELLED
- Guest cancelled
- Or circumstances changed
- No longer happening

### 🚫 REJECTED
- Not a good fit
- No availability
- Doesn't meet criteria

---

## Staff Workflow Example

### New Inquiry Arrives:

1. **Notification:** Check notification_log.txt or email
2. **Review:** Staff Dashboard > Booking Requests
3. **Contact:** Reach out to guest (email or phone)
4. **Discuss:** Ensure good fit, clarify needs
5. **Assign Room:** Update inquiry with specific lodging_unit_id
6. **Confirm:** Change status to "confirmed"
7. **Follow-up:** Send check-in details, any required forms

### Maintenance Issue Reported:

1. **Create Task:** Property Management > Maintenance
2. **Notification:** Auto-logs and emails
3. **Persistent Display:** Shows in relevant sections until completed
4. **Assignment:** Optionally assign to specific person
5. **Work Done:** Update status to "in_progress" then "completed"
6. **Record:** Note actual cost, any issues, completion notes

---

## Quick Reference

### Contact Information:
- **Email:** SpringMountainWellness@proton.me
- **Phone:** 743-241-6310

### Access Passwords:
- **Public Booking:** wellspring2024
- **Staff Dashboard:** staff2024

### Key Locations:
- **Booking Inquiries:** Staff Dashboard > Booking Requests
- **Maintenance Tasks:** Staff Dashboard > Property Management > Maintenance
- **Building Management:** Staff Dashboard > Property Management > Buildings
- **Notification Log:** notification_log.txt (project root)

### Files to Monitor:
- `notification_log.txt` - All email notifications
- `wellspring_bookings.db` - Database file
- `.env` - Configuration (not in git)

---

## Support

For technical issues or questions:
1. Check notification_log.txt
2. Run `python test_system.py`
3. Review UPDATES_SUMMARY.md
4. Check DEPLOYMENT.md

---

*Last Updated: January 2025*
*Version: 2.2 - Workflow Documentation*
