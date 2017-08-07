from django.http import HttpResponse


def Image(request):
    print request.path
    path = request.path.split('/')
    png = path[-1]
    with open('static/image/' + png, 'r') as f:
        c = f.read()
    return HttpResponse(c, content_type='image/jpeg')
