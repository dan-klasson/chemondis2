from django.urls import path, include
from rest_auth.views import LoginView, LogoutView
from rest_auth.registration.views import RegisterView
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'interviews', views.InterviewViewSet)

slots_router = routers.NestedDefaultRouter(
    router,
    r'interviews',
    lookup='interview'
)
slots_router.register(
    r'slots',
    views.SlotView,
    basename='timeslot'
)

urlpatterns = [
    path('login/', LoginView.as_view(), name="user-login"),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('', include(router.urls)),
    path('', include(slots_router.urls)),
]
