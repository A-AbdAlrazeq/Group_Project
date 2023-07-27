from math import log
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Car ,User,Cart
from django.contrib import messages
import datetime

def index(request): 
    return render(request, 'home.html')


def regLog(request): 
    return render(request, 'index.html')

def register(request):
    errors = User.objects.regValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/regLog')
    else:
        User.objects.create(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        return redirect ('/regLog')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/regLog')
    else:
       
        this_user = User.objects.get(email=request.POST['email2'])
        request.session['user_id'] = this_user.id
        request.session['username']=this_user.username
        if this_user.isAdmin==1 : 
            return redirect ('/admin') 
        else :
            return redirect('/user')
    
def admin(request): 
    context = {
        'username' : request.session['username'],
        'cars': Car.objects.all(),
    }
    return render(request, 'admin.html', context)
 
def user(request): 
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
            'cars': Car.objects.all(),
        }
    return render(request, 'user.html', context)
def add(request):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    if user.isAdmin == True:
        return render(request, 'add.html')
    else :
        return render(request, 'home.html')

        

def addCar(request):
    
        errors = Car.objects.addValidator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add')
        else:
        
            Car.objects.create(
                            name = request.POST['name'], 
                            model = request.POST['model'], 
                            color = request.POST['color'],
                            fuelType = request.POST['fuelType'],
                            price = request.POST['price'],
                            user = User.objects.get(id=request.session['user_id']), 
                        )
            return redirect('/admin')

def edit(request, car_id):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    if user.isAdmin == True:
        context = {
            'cars' : Car.objects.get(id=car_id) 
        }
        return render(request,'edit.html',context)
    else :
        return render(request, 'home.html')

def editCar(request, car_id):
    errors = Car.objects.editValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{car_id}')
    else:
   

        selected = Car.objects.get(id=car_id)
        selected.name = request.POST['name']
        selected.model = request.POST['model']
        selected.color = request.POST['color']
        selected.fuelType = request.POST['fuelType']
        selected.price = request.POST['price']
        selected.save()
        return redirect('/admin')

def delete(request, car_id):
    dell = Car.objects.get(id = car_id)
    dell.delete() 
    return redirect('/admin')

def add_to_favorites(request, car_id):
    this_car = Car.objects.get(id=car_id)
    this_car.bookmarked.add(
        User.objects.get(id=request.session['user_id']))
    return redirect('/user')


def remove_from_favorites(request, car_id):
    this_car = Car.objects.get(id=car_id)
    this_car.bookmarked.remove(
        User.objects.get(id=request.session['user_id']))
    return redirect('/user')


def show_favorites(request):
    user_id = request.session.get('user_id')
    user=User.objects.get(id=user_id)
    if user_id:
        context = {
            "user":user.bookmakred.all()
        }
        return render(request, "bookmark.html", context)

def logout(request): 
    request.session.flush()
    return redirect('/')


def view_cart(request,car_id):
    user_id = request.session.get('user_id')
    this_car=Car.objects.get(id=car_id)
    if user_id:
            context = {
                "car":this_car
            }
    return render (request, "add_to_cart.html",context)

def add_to_cart(request,car_id):
    user_id = request.session.get('user_id')
    this_car=Car.objects.get(id=car_id)
    from_date=request.POST['date1']
    to_date=request.POST['date2']
    user=User.objects.get(id=user_id)
    user_cart=Cart.objects.get(user=user)
    if from_date and to_date:
        start_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
        diff = abs((end_date-start_date).days)
    if user_id:
        
        total_price=int(this_car.price*diff)
    else :
            total_price=this_car.price
    if user_cart:
        user_cart.cars.add(
        Car.objects.get(id=car_id))
        user_cart.total+=total_price
        this_car.rent_days=diff
        this_car.save()
        user_cart.save()

    else:
        this_cart= Cart.objects.create(
                            user = user, 
                            total = total_price,
                        )
        this_cart.cars.add(
            Car.objects.get(id=car_id))
        this_car.rent_days=diff
        this_car.save()

    return redirect('/cart')

def cart(request):
    user_id = request.session.get('user_id')
    user=User.objects.get(id=user_id)
    user_cart=Cart.objects.get(user=user)
    if user_id:
            context = {
                "cart":user_cart
            }

    return render (request, "cart.html",context)

def remove_car_from_cart(request, car_id):
    user_id = request.session.get('user_id')
    user=User.objects.get(id=user_id)
    user_cart=Cart.objects.get(user=user)
    this_car = Car.objects.get(id=car_id)
    user_cart.total-=this_car.rent_days*this_car.price
    user_cart.cars.remove(this_car)
    user_cart.save()
    return redirect('/cart')

def checkout(request):
    return render (request, "checkout.html")


def bookmark(request):
    return render (request, "bookmark.html")
