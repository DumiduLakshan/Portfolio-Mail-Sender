# Contact Form API with FastAPI

A secure FastAPI application that handles contact form submissions and sends emails via Brevo API with rate limiting.

## Features

- ✅ POST endpoint for contact form submissions
- ✅ Email notifications via Brevo API
- ✅ Rate limiting (1 request per hour per IP)
- ✅ Input validation with Pydantic
- ✅ Environment-based configuration
- ✅ CORS support
- ✅ Auto-generated API documentation

## Prerequisites

- Python 3.8 or higher
- Brevo account (free tier available)

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Brevo Account and Get API Key

1. Go to [Brevo](https://www.brevo.com/) (formerly Sendinblue)
2. Sign up for a free account
3. Verify your email address
4. Navigate to **SMTP & API** section:
   - Click on your profile (top right)
   - Select **SMTP & API**
   - Click **Generate a new API key** or **Create a new API key**
   - Copy the API key (save it securely - you won't see it again!)

### 3. Verify Your Sender Email (Important!)

Brevo requires you to verify the sender email address:

1. In your Brevo dashboard, go to **Senders**
2. Click **Add a new sender**
3. Enter your email address and name
4. Verify it by clicking the link sent to your email

**Note:** You can use any verified email as the sender. If you don't have a domain email, you can use your personal email (like Gmail) as the sender, but:

- You must verify it in Brevo
- Update `SENDER_EMAIL` in your `.env` file with this verified email

### 4. Configure Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` file with your actual credentials:

```env
# Brevo API Configuration
BREVO_API_KEY=your_actual_brevo_api_key_here

# Email Configuration
SENDER_EMAIL=your_verified_email@example.com
SENDER_NAME=Contact Form
RECIPIENT_EMAIL=dumilakshan4878@gmail.com
```

**Important:**

- `BREVO_API_KEY`: Your Brevo API key from step 2
- `SENDER_EMAIL`: Must be verified in your Brevo account
- `RECIPIENT_EMAIL`: Where contact form submissions will be sent (already set to dumilakshan4878@gmail.com)

### 5. Run the Application

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### POST /contact

Submit a contact form with rate limiting (1 request per hour per IP).

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Inquiry about your services",
  "message": "Hello, I would like to know more about your services."
}
```

**Response (Success):**

```json
{
  "status": "success",
  "message": "Your message has been sent successfully!",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Inquiry about your services"
  }
}
```

**Response (Rate Limit Exceeded):**

```json
{
  "error": "Rate limit exceeded: 1 per 1 hour"
}
```

### GET /

Root endpoint - API information

### GET /health

Health check endpoint

## Testing with curl

```bash
curl -X POST "http://localhost:8000/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Test Subject",
    "message": "This is a test message."
  }'
```

## Testing with Python

```python
import requests

url = "http://localhost:8000/contact"
data = {
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Test Subject",
    "message": "This is a test message."
}

response = requests.post(url, json=data)
print(response.json())
```

## Rate Limiting

- Each IP address can make **1 request per hour** to the `/contact` endpoint
- After exceeding the limit, users must wait 1 hour before submitting again
- Rate limiting is based on IP address

## Security Features

- ✅ Environment variables for sensitive data
- ✅ Input validation with Pydantic
- ✅ Email validation
- ✅ Rate limiting to prevent abuse
- ✅ `.gitignore` to prevent committing secrets
- ✅ CORS configuration (adjust for production)

## Production Deployment Tips

1. **CORS**: Update the `allow_origins` in `main.py` to your specific frontend domain

```python
allow_origins=["https://yourdomain.com"],
```

2. **HTTPS**: Always use HTTPS in production

3. **Environment Variables**: Use proper secret management (AWS Secrets Manager, Azure Key Vault, etc.)

4. **Rate Limiting**: Consider using Redis for distributed rate limiting if deploying multiple instances

5. **Logging**: Add proper logging for monitoring and debugging

6. **Error Handling**: Customize error messages for production

## Troubleshooting

### "BREVO_API_KEY not found in environment variables"

- Make sure you created the `.env` file
- Verify the API key is correctly set in `.env`
- Restart the application after changing `.env`

### "Failed to send email"

- Verify your Brevo API key is correct
- Ensure sender email is verified in Brevo
- Check your Brevo account status and quota
- Review Brevo API logs in your dashboard

### Rate limit issues during testing

- Wait 1 hour between requests from the same IP
- Or restart the application (rate limit resets)
- Consider temporarily adjusting the rate limit during development

## License

MIT License

## Support

For issues or questions, please open an issue in the repository.
