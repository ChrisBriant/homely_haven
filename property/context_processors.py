from django.conf import settings

def globalsettings(request):

    return {
       'BASE_URL': settings.BASE_URL,
       'MEDIA_URL' : settings.MEDIA_URL,
    }