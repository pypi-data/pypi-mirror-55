from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.models.base import IrekuaModelBase


class DeviceType(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for device type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of device type'),
        blank=False)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Icon for device type'),
        upload_to='images/device_types/',
        blank=True,
        null=True)

    mime_types = models.ManyToManyField(
        'MimeType',
        db_column='mime_types',
        verbose_name=_('mime types'),
        help_text=_(
            'Possible mime types for files generated by devices'
            'of this type'),
        blank=True)

    class Meta:
        verbose_name = _('Device Type')
        verbose_name_plural = _('Device Types')

        ordering = ['name']

    def validate_mime_type(self, mime_type):
        try:
            self.mime_types.get(mime_type=mime_type)
        except self.mime_types.model.DoesNotExist:
            msg = _(
                'Device type %(device_type)s does not '
                'support files of mime type %(mime_type)s'
            )
            params = dict(
                device_type=self.name,
                mime_type=mime_type)
            raise ValidationError(msg, params=params)

    def __str__(self):
        return self.name
