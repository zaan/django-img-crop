
django.jQuery(document).ready(function() {
	django.jQuery('#img_upload_popup').click(function() {
		var img_field = django.jQuery('#img_upload_popup').siblings('input');
		var win = window.open(this.href, img_field.attr('id'), 'height=650,width=900,resizable=yes,scrollbars=yes');
		win.focus();
		return false;
	});
	
});
