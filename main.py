from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Contact Form API",
    description="API for handling contact form submissions with email notifications",
    version="1.0.0"
)

# Add rate limit exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the sender")
    email: EmailStr = Field(..., description="Email address of the sender")
    subject: str = Field(..., min_length=1, max_length=200, description="Subject of the message")
    message: str = Field(..., min_length=1, max_length=5000, description="Message content")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Inquiry about your services",
                "message": "Hello, I would like to know more about your services."
            }
        }

# Brevo API configuration
def get_brevo_client():
    """Initialize and return Brevo API client"""
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        raise ValueError("BREVO_API_KEY not found in environment variables")

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    return sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_email_via_brevo(contact_data: ContactForm):
    """Send email using Brevo API"""
    try:
        api_instance = get_brevo_client()

        # Get sender email from environment (must be verified in Brevo)
        sender_email = os.getenv("SENDER_EMAIL", "noreply@yourdomain.com")
        sender_name = os.getenv("SENDER_NAME", "Contact Form")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "dumilakshan4878@gmail.com")

        # Create email content
        html_content = f"""
        <html>
            <body>
                <h2>New Contact Form Submission</h2>
                <p><strong>From:</strong> {contact_data.name}</p>
                <p><strong>Email:</strong> {contact_data.email}</p>
                <p><strong>Subject:</strong> {contact_data.subject}</p>
                <hr>
                <h3>Message:</h3>
                <p>{contact_data.message}</p>
            </body>
        </html>
        """

        text_content = f"""
        New Contact Form Submission

        From: {contact_data.name}
        Email: {contact_data.email}
        Subject: {contact_data.subject}

        Message:
        {contact_data.message}
        """

        # Create email object
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": recipient_email}],
            sender={"email": sender_email, "name": sender_name},
            reply_to={"email": contact_data.email, "name": contact_data.name},
            subject=f"Contact Form: {contact_data.subject}",
            html_content=html_content,
            text_content=text_content
        )

        # Send email
        api_response = api_instance.send_transac_email(send_smtp_email)
        return api_response

    except ApiException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Contact Form API is running",
        "endpoints": {
            "POST /contact": "Submit a contact form (Rate limit: 1 request per hour per IP)"
        }
    }

@app.post("/contact", status_code=200)
@limiter.limit("1/hour")  # 1 request per hour per IP address
async def contact(request: Request, contact_form: ContactForm):
    """
    Submit a contact form.

    Rate limit: 1 request per hour per IP address.

    - **name**: Your full name
    - **email**: Your email address
    - **subject**: Subject of your message
    - **message**: Your message content
    """
    try:
        # Send email via Brevo
        result = send_email_via_brevo(contact_form)

        return {
            "status": "success",
            "message": "Your message has been sent successfully!",
            "data": {
                "name": contact_form.name,
                "email": contact_form.email,
                "subject": contact_form.subject
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
