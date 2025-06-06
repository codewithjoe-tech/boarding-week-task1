from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied

class CustomJwtAuthentication(JWTAuthentication) :

    def authenticate(self, request:Request):
        refresh = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')
        if not (refresh and access_token):
            return None
        
        try:
            validated_token = self.get_validated_token(access_token)

        except (InvalidToken , TokenError) as e:
            raise AuthenticationFailed("Invalid or expired access token.") from e
        
        user= self.get_user(validated_token)
        if not user.is_verified:
            raise PermissionDenied("Email is not verified.")
        return user, validated_token


        
