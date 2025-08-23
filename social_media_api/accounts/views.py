from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.decorators import action
from .serializers import RegisterSerializer, UserSerializer, UserPublicSerializer
from django.contrib.auth import get_user_model

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

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only listing/retrieving users + actions to follow/unfollow and
    list followers/following.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        target = self.get_object()
        me = request.user
        if target == me:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Idempotent follow
        me.following.add(target)
        return Response({"detail": f"You are now following {target.username}."})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        target = self.get_object()
        me = request.user
        if target == me:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Idempotent unfollow
        me.following.remove(target)
        return Response({"detail": f"You unfollowed {target.username}."})

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        qs = user.followers.all()
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        qs = user.following.all()
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)