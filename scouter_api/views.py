from django.http import HttpResponse, Http404
from django.conf import settings

def index(request):
    return HttpResponse(open(settings.SCOUTER_INDEX_LOCATION))

def build_file(request, filename):
    try:
        return HttpResponse(open(os.path.join(settings.SCOUTER_WEB_LOCATION, filename)))
    except:
        raise Http404
