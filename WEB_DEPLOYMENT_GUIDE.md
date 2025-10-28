# Web Deployment Guide - Wellspring Mountain Booking System

## Overview

This guide explains how to deploy your Wellspring Mountain booking system to the web so staff can access it from anywhere.

## Important: Database & Privacy

**⚠️ CRITICAL INFORMATION:**

The database file (`wellspring_bookings.db`) is now included in Git and will be pushed to GitHub. This means:

- ✅ All staff can access and modify bookings from the web
- ✅ Database persists across deployments
- ⚠️ **Guest data will be in your GitHub repository**
- 🔒 **Your GitHub repository MUST be PRIVATE**

### Make Your Repository Private

1. Go to your GitHub repository
2. Click **Settings** (top right)
3. Scroll down to **Danger Zone**
4. Click **Change visibility**
5. Select **Make private**

## Deployment to Streamlit Cloud (Recommended - FREE)

Streamlit Cloud is perfect for this application:
- ✅ Free hosting
- ✅ Automatic deploys from GitHub
- ✅ SSL/HTTPS included
- ✅ Easy password management
- ✅ SQLite database works out of the box

### Step 1: Push to GitHub

```bash
# Make sure all changes are committed
git add -A
git commit -m "Prepare for web deployment"

# Push to GitHub (creates remote if needed)
git push -u origin master
```

### Step 2: Sign Up for Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click **Sign up** (use your GitHub account)
3. Authorize Streamlit Cloud to access your GitHub

### Step 3: Deploy Your App

1. Click **New app** button
2. Fill in the deployment form:
   - **Repository:** Select your `Wellspring Mountain` repo
   - **Branch:** `master`
   - **Main file path:** `app.py`
   - **App URL:** Choose something like `wellspring-mountain`

3. Click **Advanced settings**

4. Add your secrets in the **Secrets** section:
```toml
PUBLIC_PASSWORD = "wellspring2024"
STAFF_PASSWORD = "staff2024"
```

5. Click **Deploy!**

### Step 4: Wait for Deployment

- Initial deployment takes 2-5 minutes
- You'll see a unique URL like: `https://wellspring-mountain-xxxxx.streamlit.app`
- Streamlit auto-detects `requirements.txt` and installs dependencies

### Step 5: Test Your Deployment

1. Visit your app URL
2. Test public booking page (password: `wellspring2024`)
3. Test staff dashboard (password: `staff2024`)
4. Create a test booking
5. Verify it appears in staff dashboard

### Step 6: Update Passwords (IMPORTANT!)

**Change the default passwords immediately:**

1. In Streamlit Cloud dashboard, go to your app
2. Click **Settings** → **Secrets**
3. Update the passwords:
```toml
PUBLIC_PASSWORD = "your-secure-public-password"
STAFF_PASSWORD = "your-secure-staff-password"
```
4. Click **Save**
5. App will restart automatically

## Database Persistence

### How It Works

Streamlit Cloud has **limited persistence**:
- ✅ Database file is deployed from your git repo
- ✅ Changes persist during a session
- ⚠️ **Database resets when app restarts** (every few days or on deploy)
- ❌ Not suitable for long-term production use

### Better Option: External Database (For Production)

For production use with permanent data storage, consider:

#### Option A: Turso (Recommended - LibSQL/SQLite Compatible)
- Free tier: 500 databases, 1GB storage
- Full SQLite compatibility
- Built for edge deployment
- Setup: https://turso.tech/

#### Option B: PostgreSQL (More Setup Required)
- Use services like Neon, Supabase, or Railway
- Requires code changes to switch from SQLite to PostgreSQL
- More complex but industry-standard

## Updating Your Deployed App

### Automatic Updates (Recommended)

Every time you push to GitHub, Streamlit Cloud automatically redeploys:

```bash
# Make changes locally
git add -A
git commit -m "Update booking system"
git push

# Streamlit Cloud detects the push and redeploys automatically
```

### Manual Updates

1. Go to Streamlit Cloud dashboard
2. Select your app
3. Click **Reboot** to redeploy from latest GitHub commit

## Custom Domain (Optional)

To use your own domain (e.g., booking.wellspring-mountain.org):

1. In Streamlit Cloud, go to app settings
2. Click **Custom domain**
3. Enter your domain
4. Follow DNS setup instructions (add CNAME record)

## Email Notifications Setup

To enable email notifications:

1. Get SMTP credentials from ProtonMail
2. Add to Streamlit Cloud secrets:
```toml
SMTP_SERVER = "smtp.protonmail.com"
SMTP_PORT = "587"
SMTP_USERNAME = "SpringMountainWellness@proton.me"
SMTP_PASSWORD = "your_protonmail_app_password"
FROM_EMAIL = "SpringMountainWellness@proton.me"
```

3. Update `config.py` to read from Streamlit secrets:
```python
import streamlit as st

class Config:
    PUBLIC_PASSWORD = st.secrets.get("PUBLIC_PASSWORD", os.getenv("PUBLIC_PASSWORD"))
    STAFF_PASSWORD = st.secrets.get("STAFF_PASSWORD", os.getenv("STAFF_PASSWORD"))
    # ... etc
```

## Monitoring & Maintenance

### View Logs

1. Go to your app in Streamlit Cloud
2. Click on the hamburger menu (three lines)
3. Select **Manage app**
4. View real-time logs and errors

### Backup Your Database

Since the database can reset, create backups:

```bash
# From your local machine, pull latest from production
# (If you've added any bookings on the web)

# Add a scheduled backup script or manual process
# Download from GitHub after staff add bookings
```

## Troubleshooting

### App Won't Start

Check logs for errors:
- Missing dependencies in `requirements.txt`
- Syntax errors in Python code
- Missing environment variables

### Database Issues

- Database resets every few days on Streamlit Cloud
- Consider external database for production
- Keep local backups

### Password Not Working

- Check Streamlit Cloud secrets spelling
- Passwords are case-sensitive
- Restart app after changing secrets

## Security Checklist

- [ ] GitHub repository is PRIVATE
- [ ] Changed default passwords from `wellspring2024` and `staff2024`
- [ ] Using strong passwords (12+ characters, mixed case, numbers, symbols)
- [ ] Only sharing URLs with authorized staff
- [ ] Regularly monitoring access logs
- [ ] Have backup of database locally

## Production Readiness

For true production deployment with permanent data:

1. **Migrate to external database** (Turso or PostgreSQL)
2. **Set up automated backups**
3. **Implement audit logging**
4. **Add rate limiting** for security
5. **Set up monitoring** (Sentry, etc.)
6. **Create disaster recovery plan**

## Support

For issues:
- Streamlit Community: https://discuss.streamlit.io/
- Streamlit Docs: https://docs.streamlit.io/
- GitHub Issues: (your repo)/issues

---

**Your app is now ready to deploy to the web!** 🎉

Start with Streamlit Cloud (free) for testing, then consider upgrading to an external database for production use.
