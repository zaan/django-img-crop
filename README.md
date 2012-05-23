# Django Image Crop

Simple app for cropping images in django admin.

## Installation
Add django_img_crop to your INSTALLED_APPS in settings.py

    INSTALLED_APPS = (
        ...
        'django_img_crop',
    )
   
Add django_img_crop urls in urls.py

    urlpatterns = patterns('',
        ...
        url(r'^admin/crop-img/', include('django_img_crop.urls')),
        url(r'^admin/', include(admin.site.urls)),
     )

## Configuration
In file dic_settings.py there's some options you might want to customize to fit your needs.

+ DIC_IMG_SIZE - before cropping, uploaded image is resized to dimensions defined in this setting, 
+ DIC_IMG_DEFAULT_CROP_SIZE - global size of cropped image, it can be overwritten by using *size* argument of *django_img_crop.fields.ImageCropField* class constructor
+ DIC_IMG_DISPLAY_RATIO - if normal and cropped images are too big to fit in popup window, you can make them to display proportionally smaller by manipulating this setting
+ DIC_UPLOAD - path for uploaded images
+ DIC_IMG_URL - URL of uploaded image

## Usage
Use *django_img_crop.fields.ImageCropField* in your model:

    from django_img_crop.fields import ImageCropField
    
    class MyModel(models.Model):
        name = models.CharField(max_length=20)
        image = ImageCropField(size=(260, 180))

By default, all cropped images are stored in directory defined in DIC_UPLOAD setting. If you don't want to store them all in one directory, but for example depending on model using cropping, you'll have to implement it by your own in models *save* method.
