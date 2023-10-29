from django.shortcuts import render
from store.models import Shoe

# Create your views here.

def index(request):
    Shoes = Shoe.objects.all()

    return render(request, 'store/index.html', context={"Shoes": Shoes})


