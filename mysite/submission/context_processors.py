from django.conf import settings # import the settings file

def url_extension(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'url_extension': settings.URL_EXTENSION}