from django.conf import settings
from django.contrib import admin
from django.db import models
from render_doc import models as render_doc_models
from django import forms
from codemirror import CodeMirrorTextarea
from django.forms import TextInput, Textarea
from simple_history.admin import SimpleHistoryAdmin

codemirror_widget = CodeMirrorTextarea(
    mode="yaml",
    config={
        'inputStyle': 'contenteditable',
        'spellcheck': True,
        'lineWrapping': True,
    },
)
class TemplateAdminForm(forms.ModelForm):
    data = forms.CharField(
        widget=codemirror_widget,
        help_text="Enter data in valid yaml.", required=False)
    class Meta:
        model = render_doc_models.Block
        fields = "__all__"
class MyAdmin(SimpleHistoryAdmin):
    # form = TemplateAdminForm
    search_fields = ['title', 'tag', 'data']
    save_as = True
    change_form_template = 'render_doc/admin_block_detail.html'

    list_display = ['title', 'id', 'tag']
    list_filter = ['tag']

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 100})},
        models.TextField: {'widget': Textarea(attrs={
            # 'rows': 40, 
            # 'cols': 140,
            'style': 'font-family: monospace; width: 95%; height: 700px'})},
    }
admin.site.register(render_doc_models.Block, MyAdmin)