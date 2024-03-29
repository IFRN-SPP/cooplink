from django.shortcuts import render
from .ajax import *
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

class InstitutionList(JsonListView):
    template_name = 'institution/institution-list.html'
    partial_list = 'partials/institution/list.html'
    model = Institution
        
class InstitutionCreate(JsonCreateView, InstitutionList):
    template_name = 'partials/institution/create.html'
    form_class = InstitutionForm

class InstitutionUpdate(JsonUpdateView, InstitutionList):
    template_name = 'partials/institution/update.html'
    form_class = InstitutionForm

class InstitutionDelete(JsonDeleteView, InstitutionList):
    template_name = 'partials/institution/delete.html'