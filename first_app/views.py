from django.http import HttpResponse

def hello_view(request):
    your_name = "JOHN"
    return HttpResponse(f"<h1>Hello, {your_name}</h1>")
