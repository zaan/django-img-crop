
import os

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from widgets import ImageCropWidget
from dic_settings import app_settings


class ImageCropField(models.CharField):
	
	def __init__(self, *args, **kwargs):
		if 'size' not in kwargs:
			size = app_settings['DIC_IMG_DEFAULT_CROP_SIZE']
		else:
			size = kwargs.pop('size')
		self.width, self.height = size[0], size[1]
		super(ImageCropField, self).__init__(max_length=200, *args, **kwargs)
	
	def formfield(self, *args, **kwargs):
		kwargs['widget'] = ImageCropWidget(width=self.width, height=self.height)
		return super(ImageCropField, self).formfield(*args, **kwargs)
	
