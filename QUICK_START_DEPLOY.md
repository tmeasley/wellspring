# 🚀 Quick Start - Deploy to Production

Your Wellspring Mountain booking system is ready to deploy with **permanent cloud database storage**!

## ✅ What's Already Set Up

- ✅ Turso cloud database created
- ✅ Database credentials configured  
- ✅ Code ready for Streamlit Cloud
- ✅ 25 bookable rooms loaded
- ✅ Multi-staff access enabled

## 🎯 Deploy in 5 Minutes

### Step 1: Push to GitHub

```bash
git push origin master
```

**⚠️ IMPORTANT:** Make your GitHub repo **PRIVATE** to protect guest data!

### Step 2: Deploy to Streamlit Cloud (FREE)

1. Go to **https://streamlit.io/cloud**
2. Sign in with GitHub
3. Click **New app**
4. Configure:
   - **Repository:** Wellspring Mountain
   - **Branch:** `master`
   - **Main file:** `app.py`

### Step 3: Add Secrets

Click **Advanced settings** → **Secrets**

Paste this (from `streamlit_secrets_template.toml`):

```toml
PUBLIC_PASSWORD = "wellspring2024"
STAFF_PASSWORD = "staff2024"

USE_TURSO = "true"
TURSO_DATABASE_URL = "libsql://wellspring-tmeasley.aws-us-east-1.turso.io"
TURSO_AUTH_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NjE2NjI5MjYsImlkIjoiNjVjNDgwM2ItY2VlYS00N2IwLTk1YWUtOWE5MGYyYzY0YjYzIiwicmlkIjoiYTlmNWFlYTgtZWQzOC00YmYyLThlOTktODNmNjk5YWY3MjIyIn0.TaSXzPClMfrgphBw29scFP_vy0_XgQgyukM45xwdaDoZ6SOqjDpmNyp0HKzqn6FN1-NcYH66uDB6rOjvw0S0Cg"
```

### Step 4: Deploy!

Click **Deploy** and wait 2-5 minutes.

You'll get a URL like: `https://wellspring-mountain-xxxxx.streamlit.app`

### Step 5: Change Passwords! 🔒

1. Test login with default passwords
2. Go back to Streamlit Cloud → App Settings → Secrets
3. Change both passwords to strong ones
4. Save (app auto-restarts)

## 📊 How It Works

**Your Setup:**
- **Database:** Turso (LibSQL cloud) - permanent storage ✅
- **Hosting:** Streamlit Cloud - free tier ✅
- **Data:** Syncs across all staff ✅

**What happens when staff use it:**
1. Staff logs in from anywhere
2. Creates/manages bookings
3. Data saves to Turso cloud database
4. All other staff see updates instantly
5. Data persists forever (no resets!)

## 🔄 Making Updates

```bash
# Make changes locally
git add -A
git commit -m "Your update"
git push

# Streamlit Cloud auto-deploys in ~2 minutes
```

## 📱 Access Your App

**Public Booking Page:**
- URL: `https://your-app.streamlit.app`
- Password: (whatever you set for PUBLIC_PASSWORD)

**Staff Dashboard:**
- Same URL, choose "Staff Dashboard"
- Password: (whatever you set for STAFF_PASSWORD)

## ✨ Features Ready to Use

- ✅ Public inquiry/booking system
- ✅ Staff room assignment
- ✅ Direct booking (family, staff, blocks)
- ✅ Active stays tracking
- ✅ Property management
- ✅ Maintenance tasks
- ✅ 25 rooms organized by priority

## 🔒 Security Checklist

- [ ] GitHub repo is **PRIVATE**
- [ ] Changed default passwords
- [ ] Only sharing URL with authorized staff
- [ ] Using strong passwords (16+ characters)

## 📞 Need Help?

- **Streamlit Community:** https://discuss.streamlit.io/
- **Turso Docs:** https://docs.turso.tech
- **Your code is ready - just push and deploy!** 🎉

---

**That's it! Your production booking system is ready to go live.**
