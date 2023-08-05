from django.conf.urls import url, include

from .additional import additional_router
from .main import main_router
from .object_types import object_types_router



urlpatterns = [
    url(r'^', include(main_router.urls)),
    url(r'^types/', include(object_types_router.urls)),
    url(r'^additional/', include(additional_router.urls)),
]
