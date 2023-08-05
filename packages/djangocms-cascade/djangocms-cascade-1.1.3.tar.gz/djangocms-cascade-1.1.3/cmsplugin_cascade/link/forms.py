import re
import requests
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.admin.sites import site as admin_site
from django.db.models.fields.related import ManyToOneRel
from django.forms import fields, Media, ModelChoiceField
from django.forms.widgets import RadioSelect
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import HeavySelect2Widget
from cms.models import Page
from entangled.forms import EntangledModelFormMixin, get_related_object
from filer.models.filemodels import File as FilerFileModel
from filer.fields.file import AdminFileWidget, FilerFileField
from cms.utils import get_current_site


def format_page_link(*args, **kwargs):
    return format_html("{} ({})", *args, **kwargs)


class HeavySelectWidget(HeavySelect2Widget):
    @property
    def media(self):
        parent_media = super().media
        # append jquery.init.js to enforce select2.js into the global 'jQuery' namespace
        js = list(parent_media._js) + ['admin/js/jquery.init.js']
        return Media(css=parent_media._css, js=js)


class LinkSearchField(ModelChoiceField):
    widget = HeavySelectWidget(data_view='admin:get_published_pagelist')

    def __init__(self, *args, **kwargs):
        queryset = Page.objects.public()
        try:
            queryset = queryset.on_site(get_current_site())
        except:
            pass  # can happen if database is not ready yet
        kwargs.setdefault('queryset', queryset)
        super().__init__(*args, **kwargs)


class SectionChoiceField(fields.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', [('', _("Page Root"))])
        super().__init__(*args, **kwargs)

    def valid_value(self, value):
        """
        The optgroup is adjusted dynamically accroding to the selected cms_page, so always returns True
        and let `LinkForm` validate this value.
        """
        return True


class LinkForm(EntangledModelFormMixin):
    LINK_TYPE_CHOICES = [
        ('cmspage', _("CMS Page")),
        ('download', _("Download File")),
        ('exturl', _("External URL")),
        ('email', _("Mail To")),
    ]

    link_type = fields.ChoiceField(
        label=_("Link"),
        help_text=_("Type of link"),
    )

    cms_page = LinkSearchField(
        required=False,
        label='',
        help_text=_("An internal link onto any CMS page of this site"),
    )

    section = SectionChoiceField(
        required=False,
        label='',
        help_text=_("Page bookmark"),
    )

    download_file = ModelChoiceField(
        label='',
        queryset=FilerFileModel.objects.all(),
        widget=AdminFileWidget(ManyToOneRel(FilerFileField, FilerFileModel, 'id'), admin_site),
        required=False,
        help_text=_("An internal link onto a file from filer"),
    )

    ext_url = fields.URLField(
        required=False,
        label=_("URL"),
        help_text=_("Link onto external page"),
    )

    mail_to = fields.EmailField(
        required=False,
        label=_("Email"),
        help_text=_("Open Email program with this address"),
    )

    link_target = fields.ChoiceField(
        choices=[
            ('', _("Same Window")),
            ('_blank', _("New Window")),
            ('_parent', _("Parent Window")),
            ('_top', _("Topmost Frame")),
        ],
        label=_("Link Target"),
        widget=RadioSelect,
        required=False,
        help_text=_("Open Link in other target."),
    )

    link_title = fields.CharField(
        label=_("Title"),
        required=False,
        help_text=_("Link's Title"),
    )

    class Meta:
        entangled_fields = {'glossary': ['link_type', 'cms_page', 'section', 'download_file', 'ext_url', 'mail_to',
                                         'link_target', 'link_title']}

    def __init__(self, *args, **kwargs):
        link_type_choices = []
        if not getattr(self, 'require_link', True):
            link_type_choices.append(('', _("No Link")))
            self.declared_fields['link_type'].required = False
        link_type_choices.extend(self.LINK_TYPE_CHOICES)
        self.declared_fields['link_type'].choices = link_type_choices
        self.declared_fields['link_type'].initial = link_type_choices[0][0]
        instance = kwargs.get('instance')
        if instance and instance.glossary.get('link_type') == 'cmspage':
            self._preset_section(instance)
        super().__init__(*args, **kwargs)

    def _preset_section(self, instance):
        """
        Field ``cms_page`` may refer onto any CMS page, which itself may contain bookmarks. This method
        creates the list of bookmarks.
        """
        self.base_fields['section'].choices = self.base_fields['section'].choices[:1]
        try:
            cascade_page = get_related_object(instance.glossary, 'cms_page').cascadepage
            for key, val in cascade_page.glossary.get('element_ids', {}).items():
                self.base_fields['section'].choices.append((key, val))
        except (AttributeError, ObjectDoesNotExist):
            pass

    def clean(self):
        cleaned_data = super().clean()
        link_type = cleaned_data.get('link_type')
        error = None
        if link_type == 'cmspage':
            if cleaned_data['cms_page'] is None:
                error = ValidationError(_("CMS page to link to is missing."))
                self.add_error('cms_page', error)
        elif link_type == 'download':
            if cleaned_data['download_file'] is None:
                error = ValidationError(_("File for download is missing."))
                self.add_error('download_file', error)
        elif link_type == 'exturl':
            ext_url = cleaned_data['ext_url']
            if ext_url:
                try:
                    response = requests.head(ext_url, allow_redirects=True)
                    if response.status_code != 200:
                        error = ValidationError(_("No external page found on {url}.").format(url=ext_url))
                except Exception as exc:
                    error = ValidationError(_("Failed to connect to {url}.").format(url=ext_url))
            else:
                error = ValidationError(_("No external URL provided."))
            if error:
                self.add_error('ext_url', error)
        elif link_type == 'email':
            mail_to = cleaned_data['mail_to']
            if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', mail_to):
                error = ValidationError(_("'{email}' is not a valid email address.").format(email=mail_to))
                self.add_error('mail_to', error)
        if error:
            raise error
        return cleaned_data

    @classmethod
    def unset_required_for(cls, sharable_fields):
        """
        Fields borrowed by `SharedGlossaryAdmin` to build its temporary change form, only are
        required if they are declared in `sharable_fields`. Otherwise just deactivate them.
        """
        if 'link_content' in cls.base_fields and 'link_content' not in sharable_fields:
            cls.base_fields['link_content'].required = False
        if 'link_type' in cls.base_fields and 'link' not in sharable_fields:
            cls.base_fields['link_type'].required = False
