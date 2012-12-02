from texting_wall import settings as django_settings

def analytics(request):
    return {'GOOGLE_ANALYTICS': django_settings.GOOGLE_ANALYTICS}
