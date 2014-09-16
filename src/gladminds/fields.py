from django import forms
from django.db import models
from django.core.validators import ValidationError
from .widgets import FolderNameInput
import re


class FolderNameFormField(forms.CharField):
    """
    A form field to accept a foldername for this site
    """
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = FolderNameInput()
        super(FolderNameFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """
        return value stripped of leading/trailing whitespace, and lowercased
        """
        return value.strip().lower()

    def validate(self, value):
        """
        Validates the folder name is a valid Python package name
        Verifies if the folder name exists by trying to 
        do an import
        """
        super(FolderNameFormField, self).validate(value)

        if re.search(r"[^a-z0-9_]", value):
            raise ValidationError('The folder name must only contain letters, numbers, or underscores')
#         try:
#             __import__("sites.%s" % value)
#         except ImportError:
#             raise ValidationError('The folder sites/%s/ does not exist or is missing the __init__.py file' % value)


class FolderNameField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = "Folder name for this site's files.  The name may only consist of lowercase characters, numbers (0-9), and/or underscores"
        kwargs['max_length'] = 64
        super(FolderNameField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class':FolderNameFormField}
        defaults.update(kwargs)
        return super(FolderNameField, self).formfield(**defaults)
