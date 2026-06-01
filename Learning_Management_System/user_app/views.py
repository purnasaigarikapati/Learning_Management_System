from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
import jwt
SECRET_KEY = 'django-insecure-24d^zse0_+&ev+!y7afby+w%oci4s5y%^52b4ow(cliqct$=s='
from .models import User
from .userSerializer import UserSerializer

# Create your views here.
def is_authenticated(func):
    def wrapper(request):
        auth_header=request.headers.get("Authorization")
        if auth_header is None:
            return Response({
                "message":"Token is missing"
            })
        else:
            token=auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=['HS256']
                )
                user = User.objects.filter(email=decoded_token['email']).first()
                if user is None:
                    return Response({
                        "message": "User no longer exists"
                    })
                request.user = user

            except jwt.ExpiredSignatureError:
                return Response({
                    "message": "Token has expired"
                }, status=401)

            except jwt.InvalidTokenError:
                return Response({
                    "message": "Invalid token"
                }, status=401)

            return func(request)

    return wrapper

@api_view(['POST'])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({
                "message": "Email and Password are required"
            }, status=400)
        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"message": "Invalid email"},
                status=404
            )

        if user.password != password:
            return Response(
                {"message": "Invalid password"},
                status=401
            )

        payload = {
            "id": user.user_id,
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "role": user.role
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )

        return Response(
            {
                "message": "User logged in successfully",
                "token": token
            }, status=200
        )

    except Exception as e:
        return Response(
            {
                "message": "Something went wrong",
                "error": str(e)
            },
            status=500
        )

@api_view(['POST'])
def register(request):
    try:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "data": serializer.data
            },
            status=201
        )

    except ValidationError as e:
        return Response(
            {
                "message": "Validation failed",
                "errors": e.detail
            },
            status=404
        )

    except Exception as e:
        return Response(
            {
                "message": str(e)
            },
            status=500
        )

@api_view(['GET'])
@is_authenticated
def profile(request):
    return Response({
        "id": request.user.user_id,
        "name": request.user.name,
        "email": request.user.email,
        "phone": request.user.phone,
        "role": request.user.role
    })

@api_view(['PUT'])
@is_authenticated
def update_profile(request):
    request.user.phone = request.data['phone']
    request.user.save()
    return Response({'message': 'Profile Updated'})

@api_view(['DELETE'])
@is_authenticated
def delete_profile(request):
    user = User.objects.get(user_id=request.user.user_id)
    user.delete()
    return Response({'message': 'User Deleted'})
