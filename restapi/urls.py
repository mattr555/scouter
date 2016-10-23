from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_extensions.routers import ExtendedSimpleRouter
from restapi import views

router = ExtendedSimpleRouter()
router.register(r'users', views.UserViewSet)

team_router = router.register(r'teams', views.TeamViewSet)
team_router.register(r'notes', views.NoteViewSet, base_name='team-notes', parents_query_lookups=['team_id'])


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^', include(router.urls))
]
