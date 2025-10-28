# 🏔️ Wellspring Mountain Booking System

**Production-ready booking and property management system for Wellspring Mountain retreat center.**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.48+-red.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Turso](https://img.shields.io/badge/Database-Turso-green.svg)](https://turso.tech)

---

## 🎯 Overview

Complete booking system with cloud database, staff management, and website embedding capabilities.

### What This System Does

**For Guests:**
- 🌿 Submit booking inquiries (Respite, Refuge, Retreat)
- 📅 View available dates
- 📝 Provide special requests
- ✉️ Get email confirmations

**For Staff:**
- 🔑 Review and manage inquiries
- 🏠 Assign specific rooms to guests
- ➕ Create direct bookings (staff, family, blocks)
- 📊 Track active stays and occupancy
- 🔧 Manage property maintenance
- 📈 Generate reports

---

## ✨ Key Features

### Booking Management
- ✅ **Public Booking** - NO password required for guests
- ✅ **Staff Dashboard** - Password-protected admin panel
- ✅ **Direct Booking** - Book without inquiry system
- ✅ **Room Assignment** - Assign specific rooms to inquiries
- ✅ **Active Stays Tracking** - Monitor current guests
- ✅ **Real-time Availability** - Check across 25 bookable units

### Property Management
- 🔧 **Maintenance Tasks** - Track repairs and improvements
- 📝 **Property Notes** - Document building information
- ✅ **Todo Lists** - Organize tasks by priority
- 📁 **File Management** - Upload photos and documents
- 🔍 **Inspections** - Record property inspections
- 📊 **Dashboard** - Overview of all properties

### Production Features
- ☁️ **Cloud Database** - Turso (LibSQL) permanent storage
- 🌐 **Web Embeddable** - iframe for your website
- 📧 **Email Notifications** - Automated alerts
- 🔒 **Secure** - Encrypted data, private by design
- 📱 **Mobile Responsive** - Works on all devices
- 🆓 **Free Hosting** - Streamlit Cloud + Turso

---

## 🏠 Lodging Inventory (25 Units)

### Lodge (9 rooms)
- Lodge Room 1-7 (1 bed each)
- Lodge Dormroom (6 beds)

### Uptown (5 cabins)
- Uptown Cabin 1-5 (1 bed each)

### Downtown (4 cabins)
- Woodshed, Craft, Caboose, Woodshop (1 bed each)

### A-frame (4 cabins)
- A-frame Cabin 1-4 (3 beds each)

### Residential (2 houses)
- Neighbor House (4 beds)
- Easley House (4 beds)

### Other
- A-frame (Mountain Serenity) - 15 capacity for groups
- Artist Studio (1 bed)

---

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd "Wellspring Mountain"

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

**Access at:** http://localhost:8501

**Default passwords:**
- Staff: `staff2024` (change immediately!)

---

## 📦 Deploy to Production (5 Minutes)

### Step 1: Push to GitHub

```bash
git push origin master
```

**Make repo PUBLIC** (required for Streamlit Cloud free tier)

### Step 2: Deploy to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click **New app**
4. Select your repo, branch: `master`, file: `app.py`
5. Add **Secrets** (see below)
6. Click **Deploy**

### Step 3: Configure Secrets

In Streamlit Cloud → App Settings → Secrets:

```toml
# Staff authentication
STAFF_PASSWORD = "your-secure-password"

# Turso cloud database (production)
USE_TURSO = "true"
TURSO_DATABASE_URL = "libsql://wellspring-tmeasley.aws-us-east-1.turso.io"
TURSO_AUTH_TOKEN = "your-turso-token-here"

# Email (optional)
# SMTP_SERVER = "smtp.protonmail.com"
# SMTP_PORT = "587"
# SMTP_USERNAME = "SpringMountainWellness@proton.me"
# SMTP_PASSWORD = "your-email-password"
# FROM_EMAIL = "SpringMountainWellness@proton.me"
```

**See [streamlit_secrets_template.toml](streamlit_secrets_template.toml) for your pre-configured credentials.**

### Step 4: Populate Turso Database

```bash
python migrate_to_turso.py
```

**That's it!** Your app is live with permanent cloud storage.

**Full guide:** [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md)

---

## 🌐 Embed on Your Website

Add this iframe to your website:

```html
<iframe
    src="https://your-app-name.streamlit.app?embedded=true"
    width="100%"
    height="1000"
    frameborder="0"
    style="border: none;"
></iframe>
```

**Complete embedding guide:** [WEBSITE_EMBEDDING.md](WEBSITE_EMBEDDING.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md) | Deploy to production in 5 minutes |
| [WEBSITE_EMBEDDING.md](WEBSITE_EMBEDDING.md) | Embed booking system on your website |
| [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) | Complete production setup guide |
| [BOOKING_AND_MAINTENANCE_GUIDE.md](BOOKING_AND_MAINTENANCE_GUIDE.md) | Staff workflow documentation |
| [WEB_DEPLOYMENT_GUIDE.md](WEB_DEPLOYMENT_GUIDE.md) | Web deployment options |

---

## 🏗️ Project Structure

```
wellspring-mountain/
├── app.py                          # Main application
├── config.py                       # Configuration & validation
├── migrate_to_turso.py            # Database migration script
├── database/
│   ├── models.py                   # Schema & initialization
│   ├── operations.py               # Booking operations
│   ├── property_operations.py     # Property management
│   └── connection.py              # Cloud/local DB connection
├── pages/
│   ├── booking.py                  # Public booking (no password)
│   ├── staff.py                    # Staff dashboard
│   └── property_management.py     # Property management
├── utils/
│   ├── auth.py                     # Authentication
│   ├── helpers.py                  # Helper functions
│   ├── styles.py                   # Custom CSS
│   └── email_notifications.py    # Email system
└── .streamlit/
    └── config.toml                 # Streamlit configuration
```

---

## 💻 Technology Stack

- **Framework:** Streamlit 1.48.1
- **Database:**
  - Local: SQLite (development)
  - Cloud: Turso/LibSQL (production)
- **Hosting:** Streamlit Cloud (free tier)
- **Language:** Python 3.8+
- **Styling:** Custom CSS (modern, Airbnb-inspired)

---

## 🔒 Security & Privacy

### Data Security
- ✅ Database file NOT in GitHub (private local only)
- ✅ Production data in Turso cloud (encrypted)
- ✅ Staff dashboard password-protected
- ✅ Public repo safe (no guest data in code)
- ✅ Turso credentials in Streamlit secrets (encrypted)

### Privacy
- ✅ Guest data never in git/GitHub
- ✅ HTTPS/SSL automatic (Streamlit + Turso)
- ✅ Input sanitization prevents SQL injection
- ✅ Session management secure

---

## 💰 Cost

**Total: $0/month** 🎉

| Service | Plan | Cost |
|---------|------|------|
| Streamlit Cloud | Free tier | $0 |
| Turso Database | Free tier (1GB, 1B reads) | $0 |
| GitHub | Public repo | $0 |

**Your booking system runs entirely on free tiers!**

---

## 🎯 Use Cases

### Respite (3 days - 3 weeks)
Free nature-based refuge with private room, shared kitchen, community support.

### Refuge (Up to 3 months)
Medium-term housing for those experiencing homelessness or transitioning from difficult situations.

### Retreat (Groups)
Corporate teams, nonprofits, churches, schools - workshops, meetings, conferences.

---

## 📞 Contact

**Wellspring Mountain**
- Phone: 743-241-6310
- Email: SpringMountainWellness@proton.me

---

## 📝 License

Copyright © 2025 Wellspring Mountain. All rights reserved.

---

## 🙏 Acknowledgments

Built with [Claude Code](https://claude.com/claude-code) - AI-powered development assistant.

---

## 🚀 Get Started Now

1. **Local:** `streamlit run app.py`
2. **Production:** See [QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md)
3. **Embed:** See [WEBSITE_EMBEDDING.md](WEBSITE_EMBEDDING.md)

**Your booking system is ready to deploy!** 🎊
