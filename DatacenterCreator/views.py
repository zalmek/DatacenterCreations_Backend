import psycopg2
from django.shortcuts import render, redirect

from DatacenterCreator.models import Components


# Create your views here.

def GetComponent(request, id):
    component = Components.objects.get(componentid=id)
    print(component)
    return render(request,
                  'component.html',
                  {'component': component}
                  )


def sendText(request):
    input_text = request.GET.get('text')
    if input_text is None:
        input_text = ""
    components = Components.objects.all().filter(componentname__icontains=input_text).filter(componentstatus=1)
    return render(request,
                  'components.html',
                  {'components': components,
                   'input': input_text}
                  )


def deleteComponent(request):
    input_text = request.POST["id"]
    print(input_text)
    conn = psycopg2.connect(
        host="localhost",
        database="datacenterCreator",
        user="postgres",
        password="De23ni04s",)
    cursor = conn.cursor()
    cursor.execute("""UPDATE components  SET componentstatus=0 WHERE componentid=(%s)""", (input_text,))
    conn.commit()
    conn.close()
    return redirect("sendText")
