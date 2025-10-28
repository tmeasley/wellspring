# Wellspring Mountain Booking System - Deployment Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Wellspring Mountain"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and set your passwords:
   # PUBLIC_PASSWORD=your_public_password
   # STAFF_PASSWORD=your_staff_password
   ```

4. **Initialize the database**
   ```bash
   python init_database.py
   ```

5. **Test configuration**
   ```bash
   python config.py
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will be available at `http://localhost:8501`

---

## Streamlit Cloud Deployment

### Step 1: Prepare Repository

1. Ensure all files are committed to Git
2. Push to GitHub, GitLab, or Bitbucket

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `app.py`

### Step 3: Configure Secrets

In Streamlit Cloud dashboard:
1. Go to your app settings
2. Navigate to "Secrets" section
3. Add your environment variables:

```toml
PUBLIC_PASSWORD = "your_public_password_here"
STAFF_PASSWORD = "your_staff_password_here"
```

### Step 4: Deploy

Click "Deploy" and wait for the app to build and launch.

---

## Alternative Deployment Options

### Heroku Deployment

1. **Create Procfile**
   ```bash
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku config:set PUBLIC_PASSWORD=your_password
   heroku config:set STAFF_PASSWORD=your_password
   ```

### Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py"]
   ```

2. **Build and run**
   ```bash
   docker build -t wellspring-booking .
   docker run -p 8501:8501 \
     -e PUBLIC_PASSWORD=your_password \
     -e STAFF_PASSWORD=your_password \
     wellspring-booking
   ```

### DigitalOcean App Platform

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `streamlit run app.py --server.port=8080`
4. Add environment variables in the dashboard
5. Deploy

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PUBLIC_PASSWORD` | Yes | `public123` | Password for public booking access |
| `STAFF_PASSWORD` | Yes | `staff123` | Password for staff dashboard access |
| `DATABASE_PATH` | No | `wellspring_bookings.db` | Path to SQLite database |
| `DEBUG_MODE` | No | `false` | Enable debug logging |

---

## Database Management

### Backup Database

```bash
# Create backup
cp wellspring_bookings.db wellspring_bookings_backup_$(date +%Y%m%d).db

# Or use SQLite dump
sqlite3 wellspring_bookings.db .dump > backup.sql
```

### Restore Database

```bash
# From backup file
cp wellspring_bookings_backup_20240101.db wellspring_bookings.db

# From SQL dump
sqlite3 wellspring_bookings.db < backup.sql
```

### Reset Database

```bash
# Warning: This will delete all data!
rm wellspring_bookings.db
python init_database.py
```

---

## Security Best Practices

1. **Strong Passwords**
   - Use strong, unique passwords for PUBLIC_PASSWORD and STAFF_PASSWORD
   - Never commit passwords to version control
   - Rotate passwords periodically

2. **Environment Variables**
   - Keep .env file out of version control (already in .gitignore)
   - Use secure secret management in production (Streamlit Secrets, AWS Secrets Manager, etc.)

3. **Database Security**
   - Regular backups (daily recommended)
   - Restrict file system access to database file
   - Consider encryption for sensitive data

4. **Access Control**
   - Use HTTPS in production (Streamlit Cloud provides this automatically)
   - Monitor access logs
   - Implement rate limiting if needed

---

## Monitoring and Maintenance

### Health Checks

```bash
# Test database connection
python -c "from database.models import get_db_connection; conn = get_db_connection(); print('Database OK'); conn.close()"

# Test all operations
python -c "from database.operations import BookingOperations; print('Operations:', BookingOperations.get_booking_summary())"
```

### Logs

Streamlit Cloud logs are available in the dashboard.

For local/custom deployments:
```bash
# View Streamlit logs
streamlit run app.py --logger.level=info
```

### Performance Optimization

1. **Database Indexing** (if needed for large datasets)
   ```sql
   CREATE INDEX idx_booking_dates ON booking_requests(check_in, check_out);
   CREATE INDEX idx_booking_status ON booking_requests(status);
   ```

2. **Caching** (already implemented)
   - Database initialization is cached
   - Consider adding more caching for frequently accessed data

---

## Troubleshooting

### Common Issues

**Issue: "Module not found" errors**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Database locked errors**
```bash
# Solution: Check for other processes accessing the database
# Close other connections or restart the application
```

**Issue: Authentication not working**
```bash
# Solution: Verify environment variables
python config.py
```

**Issue: Streamlit won't start**
```bash
# Solution: Check port availability
# Try a different port
streamlit run app.py --server.port=8502
```

### Getting Help

1. Check the [README.md](README.md) for basic documentation
2. Review [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md) for architecture details
3. Open an issue in the repository
4. Contact system administrator

---

## Scaling Considerations

### Current System Limitations

- SQLite is suitable for up to ~100 concurrent users
- Single-server deployment
- No horizontal scaling

### Migration Path for Growth

1. **Database**: SQLite → PostgreSQL
2. **File Storage**: Local → S3/Cloud Storage
3. **Authentication**: Simple password → OAuth/SSO
4. **Deployment**: Single instance → Load balanced cluster

---

## Version History

- **v1.0** (Initial): Basic booking system
- **v2.0** (Current): Property management system added

---

## Support and Maintenance

### Regular Tasks

- [ ] Weekly: Review and respond to booking requests
- [ ] Monthly: Backup database
- [ ] Quarterly: Review and update passwords
- [ ] Annually: Review and update dependencies

### Emergency Contacts

- System Administrator: [contact info]
- Technical Support: [contact info]
- Wellspring Mountain Office: (555) 123-4567

---

## License

Copyright © 2024 Wellspring Mountain. All rights reserved.
