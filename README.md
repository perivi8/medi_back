# Medical Insurance ML Dashboard - Backend

This is the FastAPI backend for the Medical Insurance ML Dashboard, designed to be deployed on Render.

## Features

- FastAPI REST API
- Machine Learning model for insurance claim prediction
- User authentication with JWT
- Supabase database integration
- Claims analysis and statistics
- Admin panel functionality
- Email reports via HTTP-based services (SendGrid, Mailgun)

## Deployment on Render

### Prerequisites

1. A Render account
2. A Supabase project with database setup
3. Environment variables configured

### Environment Variables

Set these environment variables in your Render service:

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
JWT_SECRET_KEY=your_jwt_secret_key
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
ENVIRONMENT=production
# For email functionality (recommended for Render):
SENDGRID_API_KEY=your_sendgrid_api_key
# Alternative Gmail credentials (may timeout on Render):
GMAIL_EMAIL=your-gmail@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
```

### Email Service on Render

**Important**: Render blocks SMTP ports (25, 465, 587) which prevents direct Gmail SMTP connections. To fix email functionality:

1. **Recommended**: Use SendGrid HTTP API
   - Sign up at [SendGrid](https://sendgrid.com/) (free tier: 100 emails/day)
   - Get an API key
   - Add `SENDGRID_API_KEY` to Render environment variables
   - See [SENDGRID_SETUP_GUIDE.md](SENDGRID_SETUP_GUIDE.md) for detailed instructions

2. **Alternative**: Use Mailgun HTTP API
   - Sign up at [Mailgun](https://www.mailgun.com/)
   - Get API key and domain
   - Add to Render environment:
     ```
     MAILGUN_API_KEY=your_mailgun_api_key
     MAILGUN_DOMAIN=your_mailgun_domain
     ```

3. **Fallback**: Gmail with timeout controls
   - Emails may timeout but will be stored locally
   - Set `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD` in Render environment

### Deployment Steps

1. **Connect Repository**: Connect your GitHub repository to Render
2. **Create Web Service**: 
   - Build Command: `pip install -r requirements-render.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1`
   - Environment: Python 3.11
3. **Set Environment Variables**: Add all required environment variables
4. **Deploy**: Render will automatically deploy your service

### Health Check

The API includes a health check endpoint at `/health` for monitoring.

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /signup` - User registration
- `POST /login` - User login
- `GET /me` - Get current user info
- `POST /predict` - ML prediction
- `GET /stats` - Dataset statistics
- `GET /claims-analysis` - Claims analysis
- `GET /model-info` - Model information
- `POST /send-prediction-email` - Send prediction report via email
- `POST /admin/upload-dataset` - Upload dataset (Admin)
- `POST /admin/retrain-model` - Retrain model (Admin)

### Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env` file
3. Run: `uvicorn app:app --reload`

### Database Setup

The application uses Supabase for data storage. Make sure to:

1. Create a Supabase project
2. Run the SQL schema from `supabase_schema.sql`
3. Set the connection details in environment variables

## Support

For issues and questions, please check the main project documentation.