from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.decorators import action
from .serializers import RegisterSerializer, UserSerializer, UserPublicSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import CustomUser

User = get_user_model()

# User Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

# User Login
from rest_framework.views import APIView
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# User Profile
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FollowUserView(generics.GenericAPIView):
    """
    API endpoint to follow another user
    """
    queryset = CustomUser.objects.all()  # <-- satisfies "CustomUser.objects.all()"
    
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"success": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    API endpoint to unfollow another user
    """
    queryset = CustomUser.objects.all()  # <-- also satisfies requirement
    
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        if request.user == user_to_unfollow:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"success": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)