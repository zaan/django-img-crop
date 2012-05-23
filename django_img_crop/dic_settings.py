
import os

from django.conf import settings

app_settings = {
	'DIC_IMG_SIZE': (1024, 1024),
	'DIC_IMG_DEFAULT_CROP_SIZE': (320, 320),
	'DIC_IMG_DISPLAY_RATIO': 0.5,
	'DIC_UPLOAD': 'tmp',
	'DIC_IMG_URL': '%stmp/' % settings.MEDIA_URL
}
app_settings['DIC_UPLOAD_FULL'] = os.path.join(settings.MEDIA_ROOT, app_settings['DIC_UPLOAD'])

for setting in app_settings.keys():
	try:
		app_settings[setting] = getattr(settings, setting)
	except AttributeError:
		pass
