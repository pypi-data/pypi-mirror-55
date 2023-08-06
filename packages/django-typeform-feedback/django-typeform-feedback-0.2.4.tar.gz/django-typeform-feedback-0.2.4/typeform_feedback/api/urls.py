from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from .views import UserTypeformViewSet, GenericTypeformApiView

app_name = 'typeform_feedback'

router = DefaultRouter()
router.register(r'', UserTypeformViewSet, base_name='action')

urlpatterns = [
    url(r'^action/', include(router.urls)),
    url(r'^get/(?P<quiz_slug>\w+)/', GenericTypeformApiView.as_view(), name='get-url'),
]
