
from django import forms
from django.utils.translation import ugettext_lazy as _


class UploadForm(forms.Form):
	image = forms.ImageField(required=True, label=_(u"Plik graficzny"))
	
	def clean_image(self):
		uploaded_file = self.cleaned_data['image']
		filename_bits = uploaded_file.name.split('.')
		if filename_bits[-1] not in ['jpg', 'jpeg', 'png', 'gif']:
			raise forms.ValidationError(_(u'Invalid image format. Allowed formats: jpg, jpeg, png, gif'))
		return self.cleaned_data['image']
