from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'documents', views.DocumentViewSet, base_name='document')
router.register(r'documents/(?P<document_id>[0-9]+)/attachments', views.AttachmentViewSet, base_name='document-attachments')
router.register(r'documents/(?P<document_id>[0-9]+)/revisions', views.RevisionViewSet, base_name='document-revisions')
router.register(r'documents/(?P<document_id>[0-9]+)/annotations', views.AnnotationViewSet, base_name='document-annotations')

urlpatterns = [
    # viewing a specific document identified by FRBR URI fragment,
    # this requires at least 4 components in the FRBR URI,
    # starting with the two-letter country code
    #
    # eg. /za/act/2007/98
    url(r'^(?P<frbr_uri>[a-z]{2}[-/].*)$',
        views.PublishedDocumentDetailView.as_view({'get': 'get'}),
        name='published-document-detail'),

    url(r'^search/documents$', views.SearchView.as_view(scope='documents'), name='search'),
    url(r'^search/works$', views.SearchView.as_view(scope='works'), name='search'),
    url(r'^render$', views.RenderView.as_view(), name='render'),
    url(r'^parse$', views.ParseView.as_view(), name='parse'),
    url(r'^analysis/link-terms$', views.LinkTermsView.as_view(), name='link-terms'),
    url(r'^analysis/link-references$', views.LinkReferencesView.as_view(), name='link-references'),

    url(r'documents/(?P<document_id>[0-9]+)/media/(?P<filename>.*)$', views.attachment_media_view, name='document-media'),
    url(r'documents/(?P<document_id>[0-9]+)/activity', views.DocumentActivityViewSet.as_view({
        'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='document-activity'),

    # rest-based auth
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/new-token/$', views.new_auth_token),

    url(r'^', include(router.urls)),
]
