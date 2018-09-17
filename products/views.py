from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Products
from django.utils import timezone

def home(request):
    products=Products.objects
    return render(request,'products/home.html',{'products':products})

@login_required(login_url="/accounts/signup")
def upvote(request,product_id):
    if request.method=='POST':
        products=get_object_or_404(Products,pk=product_id)
        products.votes_total+=1
        products.save()
        return redirect('/products/'+str(products.id))


def detail_product(request,product_id):
    products=get_object_or_404(Products,pk=product_id)
    return render(request,'products/detail_product.html',{'products':products})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['url'] and request.POST['body'] and request.FILES['icon'] and request.FILES['image']:
            product=Products()
            product.title=request.POST['title']
            product.body=request.POST['body']
            product.icon=request.FILES['icon']
            product.image=request.FILES['image']
            product.pub_date=timezone.datetime.now()
            product.hunter=request.user

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url=request.POST['url']
            else:
                product.url="http://"+request.POST['url']
            product.save()
            return redirect('/products/'+ str(product.id))
        else:
            return render(request,'products/create.html',{'error':'all fields are required'})
    else:
        return render(request,'products/create.html')
