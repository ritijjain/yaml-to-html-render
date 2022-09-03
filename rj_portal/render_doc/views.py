from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from render_doc import models as render_doc_models
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from render_doc import utils as render_doc_utils
from django.urls import reverse
import weasyprint
import requests
import html
from django.contrib.admin.views.decorators import staff_member_required

def render_doc_html(request, block_id):
    block = get_object_or_404(render_doc_models.Block, pk=block_id)

    if block.public == True:
        pass
    else:
        if request.user.is_authenticated:
            if request.user.is_staff:
                pass
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()

    return render(request, block.template, block.data_inheritance)

@staff_member_required
def render_send_to_gh(request, block_id):
    block = get_object_or_404(render_doc_models.Block, pk=block_id)

    try:
        url = request.build_absolute_uri(reverse('render_doc_html', kwargs={'block_id': block.id}))
        response = block.gh_update_resume(requests.get(url).text)
        return HttpResponse(f'Success: {response}')
    except Exception as e:
        return HttpResponse(f'Failure: {e}')
        

