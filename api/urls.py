from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StudentProfileViewSet, MentorProfileViewSet
from .views import UserSignupView, UserLoginView, UserSearchView, MatchRequestViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'match-requests', MatchRequestViewSet, basename='match-request')
router.register(r'student-profiles', StudentProfileViewSet)
router.register(r'mentor-profiles', MentorProfileViewSet)

# Define URL patterns
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('', include(router.urls)),  # Include the router URLs
]
