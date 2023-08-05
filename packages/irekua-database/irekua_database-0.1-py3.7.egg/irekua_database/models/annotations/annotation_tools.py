from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema

from irekua_database.models.base import IrekuaModelBase


class AnnotationTool(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of annotation tool'),
        blank=False)
    version = models.CharField(
        max_length=16,
        db_column='version',
        verbose_name=_('version'),
        help_text=_('Version of annotation tool'),
        blank=True)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of annotation tool'),
        blank=False)
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Annotation tool logo'),
        upload_to='images/annotation_tools/',
        blank=True,
        null=True)
    website = models.URLField(
        db_column='website',
        verbose_name=_('website'),
        help_text=_('Annotation tool website'),
        blank=True,
        null=True)
    configuration_schema = JSONField(
        db_column='configuration_schema',
        verbose_name=_('configuration schema'),
        help_text=_('JSON schema for annotation tool configuration info'),
        blank=True,
        null=False,
        validators=[validate_JSON_schema],
        default=simple_JSON_schema)

    class Meta:
        verbose_name = _('Annotation Tool')
        verbose_name_plural = _('Annotation Tools')

        unique_together = (('name', 'version'))

        ordering = ['name']

    def __str__(self):
        msg = self.name
        if self.version:
            msg += ' - ' + self.version
        return msg

    def validate_configuration(self, configuration):
        try:
            validate_JSON_instance(
                schema=self.configuration_schema,
                instance=configuration)
        except ValidationError as error:
            msg = _('Invalid annotation tool configuration. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)
