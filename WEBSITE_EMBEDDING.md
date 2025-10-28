# Embedding Wellspring Booking in Your Website

## Quick Start - Simple iframe

Add this HTML code to your website where you want the booking system:

```html
<iframe
    src="https://your-app-name.streamlit.app?embedded=true"
    width="100%"
    height="1000"
    frameborder="0"
    style="border: none; border-radius: 8px;"
></iframe>
```

**Replace `your-app-name` with your actual Streamlit Cloud URL**

---

## Complete Example Page

```html
<!DOCTYPE html>
<html>
<head>
    <title>Book Your Stay - Wellspring Mountain</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }
        .booking-container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .booking-wrapper {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="booking-container">
        <h1>🏔️ Book Your Stay at Wellspring Mountain</h1>

        <div class="booking-wrapper">
            <iframe
                src="https://your-app-name.streamlit.app?embedded=true"
                width="100%"
                height="1200"
                frameborder="0"
                style="border: none;"
                title="Wellspring Mountain Booking"
            ></iframe>
        </div>
    </div>
</body>
</html>
```

---

## WordPress Integration

### Method 1: Custom HTML Block

1. Edit your page in WordPress
2. Click **+ Add Block**
3. Search for **Custom HTML**
4. Paste this code:

```html
<div style="max-width: 1200px; margin: 0 auto;">
    <iframe
        src="https://your-app-name.streamlit.app?embedded=true"
        width="100%"
        height="1200"
        frameborder="0"
        style="border: none; border-radius: 8px;"
    ></iframe>
</div>
```

### Method 2: Using Elementor

1. Add **HTML Widget**
2. Paste the iframe code
3. Save and preview

---

## Responsive Design (Mobile-Friendly)

```html
<style>
    .booking-iframe {
        width: 100%;
        height: 1200px;
        border: none;
        border-radius: 8px;
    }

    @media (max-width: 768px) {
        .booking-iframe {
            height: 1500px;
        }
    }
</style>

<iframe
    class="booking-iframe"
    src="https://your-app-name.streamlit.app?embedded=true"
    title="Wellspring Booking"
></iframe>
```

---

## URL Parameters

Add these to customize the embed:

- `?embedded=true` - Hides Streamlit branding (recommended)
- `&theme=light` - Force light theme
- `&theme=dark` - Force dark theme

**Example:**
```
https://your-app-name.streamlit.app?embedded=true&theme=light
```

---

## Custom Domain (Optional)

Instead of `your-app.streamlit.app`, use your own domain like `booking.wellspring-mountain.org`

**Setup:**
1. In Streamlit Cloud: Settings → Custom Domain
2. Enter: `booking.wellspring-mountain.org`
3. In DNS provider, add CNAME record:
   ```
   booking → your-app.streamlit.app
   ```
4. Wait 24 hours for DNS propagation
5. SSL is automatic

**Then use in iframe:**
```html
<iframe src="https://booking.wellspring-mountain.org?embedded=true"></iframe>
```

---

## Recommended Heights

Different pages need different heights:

- **Booking form:** 1200px
- **Availability only:** 800px
- **Mobile:** 1500px

**Adjust as needed for your layout**

---

## Troubleshooting

### iframe Not Showing
- Check Streamlit app is deployed
- Verify URL is correct
- Disable ad-blockers
- Try different browser

### Content Cut Off
- Increase height: `height="1500"`
- Test on mobile devices
- Check browser console for errors

### Scrolling Issues
- Remove `overflow: hidden` from parent containers
- Add `min-height: 100vh` to iframe

---

## Security

✅ **Safe to embed:**
- HTTPS encryption included
- Data goes directly to your Turso database
- Streamlit Cloud doesn't store bookings
- Staff dashboard remains password-protected

---

## Your Next Steps

1. **Deploy to Streamlit Cloud** ([see QUICK_START_DEPLOY.md](QUICK_START_DEPLOY.md))
2. **Get your app URL** from Streamlit Cloud dashboard
3. **Copy iframe code** from this guide
4. **Paste into your website**
5. **Replace** `your-app-name` with your actual URL
6. **Test** on desktop and mobile
7. **Adjust height** if needed

**Your booking system will be embedded and ready to use!**

---

## Need Help?

- Streamlit Embedding: https://docs.streamlit.io/develop/concepts/configuration
- iframe Guide: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe
