from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all incoming requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Log request
        print(f"[REQUEST] {request.method} {request.url.path} from {request.client.host}")
        
        response = await call_next(request)
        
        # Log response
        print(f"[RESPONSE] {response.status_code} for {request.method} {request.url.path}")
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting (in production, use Redis)"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_log = {}  # IP: [(timestamp, count)]
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = datetime.utcnow()
        
        # Clean old entries
        if client_ip in self.request_log:
            one_minute_ago = now - timedelta(minutes=1)
            self.request_log[client_ip] = [
                ts for ts in self.request_log[client_ip]
                if ts > one_minute_ago
            ]
        else:
            self.request_log[client_ip] = []
        
        # Check rate limit
        if len(self.request_log[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        
        # Add current request
        self.request_log[client_ip].append(now)
        
        return await call_next(request)
