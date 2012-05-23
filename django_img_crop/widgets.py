
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class ImageCropWidget(forms.HiddenInput):
	
	def __init__(self, *args, **kwargs):
		self.width = kwargs.pop('width')
		self.height = kwargs.pop('height')
		super(ImageCropWidget, self).__init__(*args, **kwargs)
	
	def render(self, name, value, attrs=None):
		output = super(ImageCropWidget, self).render(name, value, attrs)
		image_url = '%s%s' % (settings.MEDIA_URL, value)
		if value is None:
			return mark_safe(u'%s <a href="%s?w=%s&h=%s" id="img_upload_popup">%s</a>' % (output, reverse('dic-upload-img'), self.width, self.height, _(u'Send image')))
		return mark_safe(u'%s <img src="%s" /> <a href="%s?w=%s&h=%s" id="img_upload_popup">%s</a>' % (output, image_url, reverse('dic-upload-img'), self.width, self.height, _(u'Send image')))
	
	class Media:
		js = ('%sjs/img_crop.js' % settings.STATIC_URL,)
