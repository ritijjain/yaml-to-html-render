from django.urls import path
from render_doc import views as render_doc_views

urlpatterns = [
    path('render_html/<slug:block_id>', render_doc_views.render_doc_html, name='render_doc_html'),
    path('render_send_to_gh/<slug:block_id>', render_doc_views.render_send_to_gh, name='render_send_to_gh'),
]