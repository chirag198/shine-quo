from django.db.models import Q
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import StudentProfile, MentorProfile
from .models import User
from .models import UserMentorMatch
from .serializers import StudentProfileSerializer, MentorProfileSerializer
from .serializers import UserMentorMatchSerializer
from .serializers import UserSignupSerializer, UserLoginSerializer


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]


class MentorProfileViewSet(viewsets.ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated]


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email__iexact=serializer.validated_data['email'])

        if not user.check_password(serializer.validated_data['password']):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSignupSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '')
        return User.objects.filter(
            Q(email__iexact=keyword) | Q(username__icontains=keyword)
        )


class MatchRequestViewSet(viewsets.ModelViewSet):
    queryset = UserMentorMatch.objects.all()
    serializer_class = UserMentorMatchSerializer

    def create(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user')
        to_user = User.objects.get(id=to_user_id)
        if UserMentorMatch.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
            return Response({"error": "match request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        match_request = UserMentorMatch.objects.create(from_user=from_user, to_user=to_user, status='pending')
        return Response(UserMentorMatchSerializer(match_request).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='pending')
    def pending_requests(self, request):
        pending_requests = UserMentorMatch.objects.filter(to_user=request.user, status='pending')
        return Response(UserMentorMatchSerializer(pending_requests, many=True).data)

    @action(detail=False, methods=['get'], url_path='all-matches')
    def all_matches(self, request):
        all_matches = UserMentorMatch.objects.filter(
            Q(from_user=request.user, status='accepted') |
            Q(to_user=request.user, status='accepted')
        )
        matched_users = [req.from_user if req.to_user == request.user else req.to_user for req in all_matches]
        return Response(UserSignupSerializer(matched_users, many=True).data)

    @action(detail=True, methods=['post'], url_path='accept')
    def accept_request(self, request, pk=None):
        match_request = self.get_object()
        if match_request.to_user != request.user:
            return Response({"error": "You cannot accept this match request"}, status=status.HTTP_400_BAD_REQUEST)
        match_request.status = 'accepted'
        match_request.save()
        return Response(UserMentorMatchSerializer(match_request).data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject_request(self, request, pk=None):
        match_request = self.get_object()
        if match_request.to_user != request.user:
            return Response({"error": "You cannot reject this match request"}, status=status.HTTP_400_BAD_REQUEST)
        match_request.status = 'rejected'
        match_request.save()
        return Response(UserMentorMatchSerializer(match_request).data)
