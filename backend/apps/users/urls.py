from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'curves', CurveViewSet, basename='curves')
router.register(r'contents', ContentViewSet, basename='contents')
router.register(r'youtube', YouTubeContentViewSet, basename='youtube')
router.register(r'valuetypes', ValueTypeViewSet, basename='valuetypes')
router.register(r'requests', RequestViewSet, basename='requests')
urlpatterns = router.urls
urlpatterns += url(r'sign_s3/$', sign_s3),
