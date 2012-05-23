
import os
import Image
from time import time

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from forms import UploadForm
from dic_settings import app_settings

	
	
def upload_img(request):
	form = UploadForm()
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			if not os.path.isdir(app_settings['DIC_UPLOAD_FULL']):
				os.makedirs(app_settings['DIC_UPLOAD_FULL'])
			
			filename = "%s.%s" % (get_file_code(), form.cleaned_data['image'].name.split('.')[-1])
			filepath = os.path.join(app_settings['DIC_UPLOAD_FULL'], filename)
			fileurl = '%s%s' % (app_settings['DIC_IMG_URL'], filename)
			f = open(filepath, 'wb+')
			for chunk in form.cleaned_data['image'].chunks():
				f.write(chunk)
			f.close()
			image = Image.open(filepath)
			if image.size[0] > app_settings['DIC_IMG_SIZE'][0] and image.size[1] > app_settings['DIC_IMG_SIZE'][1]:
				image.thumbnail(app_settings['DIC_IMG_SIZE'], Image.ANTIALIAS)
			print filepath
			image.save(filepath)
			width_b = image.size[0]
			height_b = image.size[1]
			
			width = int(request.GET.get('w'))
			height = int(request.GET.get('h'))
			
			return HttpResponseRedirect('%s?filename=%s&w=%s&h=%s&wb=%s&hb=%s' % (reverse('dic-crop-img'), filename, width, height, width_b, height_b))
	return render_to_response('django_img_crop/upload-img.html', {'form': form, 'is_popup': True}, context_instance=RequestContext(request))


def crop_img(request, template_name='django_img_crop/crop-img.html'):
	
	width = int(request.GET.get('w'))
	height = int(request.GET.get('h'))
	width_b = int(request.GET.get('wb'))
	height_b = int(request.GET.get('hb'))
	DIC_IMG_CROP_SIZE = (width, height)
	DIC_IMG_SIZE = (width_b, height_b)
	
	filename = request.GET.get('filename')
	filename_parts = filename.split('.')
	output_filename = '%s-small.%s' % ("".join(filename_parts[0:-1]), filename_parts[-1])
	image_path = os.path.join(app_settings['DIC_UPLOAD_FULL'], filename)
	image_url = '%s%s' % (app_settings['DIC_IMG_URL'], filename)
	cropped_image_path = os.path.join(app_settings['DIC_UPLOAD_FULL'], output_filename)
	cropped_image_url = '%s%s' % (app_settings['DIC_IMG_URL'], output_filename)
	cropped_image_rel_path = os.path.join(app_settings['DIC_UPLOAD'], output_filename)
	image_size = [int(i * app_settings['DIC_IMG_DISPLAY_RATIO']) for i in DIC_IMG_SIZE]
	select_size = [int(i * app_settings['DIC_IMG_DISPLAY_RATIO']) for i in DIC_IMG_CROP_SIZE]
	
	if request.method == 'POST':
		if not check_post_data(request.POST):
			return render_to_response(template_name, {'error': _(u'Invalid crop parameters'), 'is_popup': True}, context_instance=RequestContext(request))
		try:
			img_obj = Image.open(image_path)
		except IOError:
			return render_to_response(template_name, {'error': _(u'File doesn\'t exists'), 'is_popup': True}, context_instance=RequestContext(request))
		img_cropped = img_obj.crop(get_coords(request.POST))
		img_cropped.thumbnail(DIC_IMG_CROP_SIZE, Image.ANTIALIAS)
		img_cropped.save(cropped_image_path)
		return render_to_response(template_name, {
			'image_url': image_url, 
			'cropped_image_url': cropped_image_url, 
			'cropped_image_rel_path': cropped_image_rel_path,
			'image_size': image_size,
			'select_size': select_size,
			'settings': settings, 
			'DIC_IMG_CROP_SIZE': DIC_IMG_CROP_SIZE, 
			'app_settings': app_settings,
			'can_save': True,
			'is_popup': True}, 
		context_instance=RequestContext(request))
		
	return render_to_response(template_name, {
		'image_url': image_url, 
		'image_size': image_size,
		'select_size': select_size,
		'settings': settings, 
		'DIC_IMG_CROP_SIZE': DIC_IMG_CROP_SIZE, 
		'app_settings': app_settings,
		'is_popup': True}, 
	context_instance=RequestContext(request))


#####

def check_post_data(post):
	digits = ['x1', 'y1', 'x2', 'y2', 'w', 'h']
	for d in digits:
		if not post.get(d,'').isdigit():
			return False
	return True

def get_coords(post):
	coords = ['x1', 'y1', 'x2', 'y2']
	coords_val = []
	for c in coords:
		coords_val.append(int(int(post.get(c)) / app_settings['DIC_IMG_DISPLAY_RATIO']))
	return tuple(coords_val)

def get_file_code():
	return str(time()).replace('.', '')
