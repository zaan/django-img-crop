from django.conf.urls.defaults import *


urlpatterns = patterns('django_img_crop.views',
	url(r'^upload_img/$', 'upload_img', name="dic-upload-img"),
	url(r'^crop_img/$', 'crop_img', name="dic-crop-img"),
)
