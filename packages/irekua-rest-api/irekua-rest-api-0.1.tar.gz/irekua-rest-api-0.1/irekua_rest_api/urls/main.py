from rest_framework import routers
from irekua_rest_api import views


main_router = routers.DefaultRouter()
main_router.register(
    r'annotations',
    views.AnnotationViewSet)
main_router.register(
    r'collections',
    views.CollectionViewSet)
main_router.register(
    r'devices',
    views.DeviceViewSet)
main_router.register(
    r'items',
    views.ItemViewSet)
main_router.register(
    r'sampling_events',
    views.SamplingEventViewSet)
main_router.register(
    r'sites',
    views.SiteViewSet)
main_router.register(
    r'terms',
    views.TermTypeViewSet)
main_router.register(
    r'users',
    views.UserViewSet)
