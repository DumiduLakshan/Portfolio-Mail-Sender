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

## Docker Deployment

### Building the Docker Image

```bash
docker build -t contact-form-api .
```

### Running with Docker

```bash
docker run -p 8000:8000 \
  -e BREVO_API_KEY=your_api_key \
  -e SENDER_EMAIL=your_verified_email@example.com \
  -e SENDER_NAME="Contact Form" \
  -e RECIPIENT_EMAIL=dumilakshan4878@gmail.com \
  contact-form-api
```

Or use the `.env` file:

```bash
docker run -p 8000:8000 --env-file .env contact-form-api
```

### Running with Docker Compose

```bash
docker-compose up -d
```

To stop:

```bash
docker-compose down
```

To view logs:

```bash
docker-compose logs -f
```

## Deploying to Coolify

Coolify is a self-hosted platform that makes deployment easy. Here's how to deploy this application:

### Prerequisites

- A running Coolify instance
- Your GitHub repository connected to Coolify
- Brevo API credentials

### Deployment Steps

#### 1. Connect Your Repository

1. Log in to your Coolify dashboard
2. Go to **Projects** → **New Project**
3. Select **GitHub** as the source
4. Connect and authorize your GitHub account
5. Select this repository: `DumiduLakshan/Portfolio-Mail-Sender`

#### 2. Configure the Application

1. After selecting the repository, Coolify will detect the Dockerfile automatically
2. Set the **Build Pack** to **Dockerfile**
3. Configure the **Port**: `8000`
4. Set the **Health Check** endpoint: `/health`

#### 3. Set Environment Variables

In Coolify's Environment Variables section, add:

```
BREVO_API_KEY=your_actual_brevo_api_key
SENDER_EMAIL=your_verified_email@example.com
SENDER_NAME=Contact Form
RECIPIENT_EMAIL=dumilakshan4878@gmail.com
```

**Important:** Mark `BREVO_API_KEY` as **secret** to hide it from logs.

#### 4. Configure Domain (Optional)

1. Go to **Domains** tab
2. Add your custom domain or use the Coolify-provided domain
3. Enable **SSL/TLS** (Let's Encrypt is automatic)

#### 5. Deploy

1. Click **Deploy** button
2. Coolify will:
   - Clone your repository
   - Build the Docker image
   - Start the container
   - Set up SSL/TLS
   - Configure health checks

#### 6. Monitor Deployment

- View **Logs** tab for build and runtime logs
- Check **Deployments** tab for deployment history
- Use **Health Check** to ensure the app is running

### Coolify Configuration Tips

#### Auto-Deploy on Git Push

Enable automatic deployments:

1. Go to **General** settings
2. Enable **Auto Deploy**
3. Select branch: `main`
4. Now every push to `main` triggers a deployment

#### Resource Limits

Set resource limits in Coolify:

```yaml
Memory Limit: 512MB
CPU Limit: 0.5 cores
```

#### Custom Docker Build Args (if needed)

If you need custom build arguments:

1. Go to **Build** settings
2. Add **Build Args**:
   ```
   PYTHON_VERSION=3.11
   ```

#### Persistent Storage (if needed in future)

If you need to persist data:

1. Go to **Storage** tab
2. Add a volume:
   - **Source**: `/app/data`
   - **Destination**: `/app/data`

### Environment Variable Management in Coolify

- **Secrets**: Use for API keys (not visible in logs)
- **Public**: Use for non-sensitive config
- **Build-time**: Variables needed during Docker build
- **Runtime**: Variables needed when container runs

### Coolify Deployment Checklist

- ✅ Repository connected to Coolify
- ✅ Dockerfile detected
- ✅ Port 8000 configured
- ✅ Health check endpoint `/health` set
- ✅ Environment variables configured
- ✅ `BREVO_API_KEY` marked as secret
- ✅ Domain configured (optional)
- ✅ SSL/TLS enabled
- ✅ Auto-deploy enabled (optional)

### Troubleshooting Coolify Deployment

#### Build Fails

- Check **Build Logs** in Coolify
- Verify Dockerfile syntax
- Ensure all dependencies in `requirements.txt`

#### Container Crashes

- Check **Runtime Logs**
- Verify environment variables are set correctly
- Test health check endpoint: `curl https://yourdomain.com/health`

#### Health Check Fails

- Ensure `/health` endpoint is accessible
- Check if port 8000 is correctly exposed
- Verify the container is actually running

#### Rate Limiting Issues

The app uses in-memory rate limiting, which resets on container restart. For production:

1. Consider using Redis for persistent rate limiting
2. Or accept that rate limits reset on deployment

### Accessing Your Deployed API

Once deployed, your API will be available at:

- **Coolify subdomain**: `https://your-app.coolify.yourdomain.com`
- **Custom domain**: `https://api.yourdomain.com` (if configured)

Test it:

```bash
curl -X POST "https://your-app.coolify.yourdomain.com/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Test from Coolify",
    "message": "This is a test message from my deployed app!"
  }'
```

### Updating Your Deployment

**Manual Update:**

1. Push changes to GitHub
2. Go to Coolify dashboard
3. Click **Redeploy** button

**Automatic Update:**

- If auto-deploy is enabled, just push to `main` branch
- Coolify will automatically rebuild and redeploy

## Support

For issues or questions, please open an issue in the repository.
