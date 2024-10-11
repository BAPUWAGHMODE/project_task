from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet, basename='projects')

urlpatterns = router.urls
