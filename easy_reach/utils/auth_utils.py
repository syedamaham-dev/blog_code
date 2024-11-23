import requests
import jwt
from jwt import PyJWTError
from functools import wraps
from django.http import JsonResponse
from clerk_backend_api import Clerk
import logging
from django.conf import settings
from jose import jwt, jwk

logger = logging.getLogger(__name__)


CLERK_ISSUER = settings.CLERK_ISSUER
CLERK_SECRET_KEY = settings.CLERK_SECRET_KEY
CLERK_JWKS_URL=settings.CLERK_JWKS_URL


clerk = Clerk(bearer_auth=CLERK_SECRET_KEY)



# Function to fetch JWKS
def get_jwks():
    response = requests.get(CLERK_JWKS_URL)
    response.raise_for_status()
    return response.json()


# Function to get public key from JWKS
def get_public_key(kid):
    jwks = get_jwks()
    for key in jwks['keys']:
        if key['kid'] == kid:
            return jwk.construct(key)
    raise ValueError("Invalid token")

# Function to decode and verify token
def decode_token(token):
    try:
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        public_key = get_public_key(kid)
        payload = jwt.decode(
            token,
            public_key.to_pem().decode('utf-8'),
            algorithms=["RS256"],
            audience="clerk",  
            issuer=CLERK_ISSUER
        )
        return payload
    except PyJWTError as e:
        raise ValueError(f"Token verification failed: {str(e)}")


# Decorator for Clerk authentication
def clerk_authenticated(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Extract the Bearer token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Authentication required"}, status=401)

        token = auth_header.split(" ")[1]

        try:
            # Decode and verify the token
            payload = decode_token(token)
            user_id = payload.get("sub")
            if not user_id:
                return JsonResponse({"error": "User ID not found in token"}, status=401)

            # Retrieve user details from Clerk
            clerk_sdk = Clerk(bearer_auth=CLERK_SECRET_KEY)
            user_details = clerk_sdk.users.list(user_id=[user_id])[0]

            # Attach user details to the request for further use
            request.user_details = user_details

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper






