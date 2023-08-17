import decimal

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .models import TouristPlace, PaymentItem
from account.forms import CarForm


class AboutView(TemplateView):
    template_name = 'about.html'


class BlogView(TemplateView):
    template_name = 'blog.html'


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        # Логика для GET-запроса
        # ...

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Логика для POST-запроса
        if 'car_id' in kwargs:
            car_id = kwargs['car_id']
            print(f"Car ID: {car_id}")
            car = get_object_or_404(TouristPlace, pk=car_id)

            # Добавляем карточку в корзину (сессию)
            cart = request.session.get('cart', [])
            cart.append(car_id)
            request.session['cart'] = cart

            # Перенаправляем на страницу корзины или куда вам нужно
            return redirect('contact')  # Замените 'cart_page' на ваш URL-шаблон корзины

        return render(request, self.template_name)


class DestinationView(TemplateView):
    template_name = 'destination.html'


class GuideView(TemplateView):
    template_name = 'guide.html'


class IndexView(TemplateView):
    template_name = 'index.html'


class PackageView(TemplateView):
    template_name = 'package.html'


class ServiceView(TemplateView):
    template_name = 'service.html'


class TestimonialView(TemplateView):
    template_name = 'testimonial.html'


# @login_required
# def add_car(request):
#     if request.method == 'POST':
#         form = CarForm(request.POST, request.FILES)
#         if form.is_valid():
#             car = form.save(commit=False)
#             car.user = request.user
#
#             if 'image' in request.FILES:
#                 car.image = request.FILES['image']
#
#             car.save()
#
#             return redirect('my_cars')
#         else:
#             print("Форма недействительна:", form.errors)
#     else:
#         form = CarForm()
#     return render(request, 'add_car.html', {'form': form})
@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user

            if 'image' in request.FILES:
                car.image = request.FILES['image']

            if request.user.is_superuser:  # Если суперпользователь, делаем машину видимой для всех
                car.visibility = 'all'

            car.save()

            return redirect('my_cars')
        else:
            print("Форма недействительна:", form.errors)
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


@login_required()
def my_cars(request):

    cars = TouristPlace.objects.filter(user=request.user)

    return render(request, 'my_cars.html', {'cars': cars})


# def cars(request):
#
#     cars = TouristPlace.objects.filter(user=request.user)
#
#     return render(request, 'car.html', {'cars': cars})


def cars(request):
    # Получить все машины, которые либо принадлежат текущему пользователю,
    # либо видны для всех (is_shared=True)
    cars = TouristPlace.objects.filter(Q(user=request.user) | Q(visibility='all'))

    return render(request, 'car.html', {'cars': cars})


def search_results_view(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = TouristPlace.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'search_results.html', context)


@login_required(login_url='login/')
def profile_view(request):

    cars_in_cart = request.session.get('cars_in_cart', [])

    myitems = TouristPlace.objects.filter(pk__in=cars_in_cart)

    total_price = sum(car.price for car in myitems)

    template = loader.get_template('payment.html')
    context = {
        'myitems': myitems,
        'total_price': total_price,
    }
    return HttpResponse(template.render(context, request))


@login_required
def payment_views(request):
    user = request.user

    payment_items = TouristPlace.objects.filter(user=user)

    context = {'payment_items': payment_items}
    return render(request, 'payment.html', context)


def calculate_subtotal(cars_in_cart):
    subtotal = 0
    for car_id in cars_in_cart:
        car = TouristPlace.objects.get(pk=car_id)
        subtotal += car.price
    return subtotal


def calculate_total_with_taxes(subtotal):
    tax_rate = decimal.Decimal('0.1')
    total_with_taxes = subtotal * (1 + tax_rate)
    return total_with_taxes


def summ_views(request):
    cars_in_cart = request.session.get('cars_in_cart', [])

    subtotal = calculate_subtotal(cars_in_cart)
    total = calculate_total_with_taxes(subtotal)

    context = {
        'cars_in_cart': cars_in_cart,
        'subtotal': subtotal,
        'total': total,
    }

    return render(request, 'contact.html', context)


@login_required
def delete_car(request, car_id):
    if request.method == 'POST':
        try:
            car = TouristPlace.objects.get(id=car_id, user=request.user)
            car.delete()
            return redirect('my_cars')
        except TouristPlace.DoesNotExist:
            pass

    return redirect('my_cars')


@login_required
def add_to_payment(request, car_id):
    car_id = int(car_id)
    cars_in_cart = request.session.get('cars_in_cart', [])
    cars_in_cart.append(car_id)
    request.session['cars_in_cart'] = cars_in_cart

    cars_in_cart_details = TouristPlace.objects.filter(pk__in=cars_in_cart)
    subtotal = calculate_subtotal(cars_in_cart)
    total = calculate_total_with_taxes(subtotal)
    context = {
        'cars_in_cart': cars_in_cart_details,
        'subtotal': subtotal,
        'total': total,
    }

    return render(request, 'contact.html', context)


@login_required
def remove_from_contact(request, car_id):
    car_id = int(car_id)
    user = request.user

    cars_in_cart = request.session.get('cars_in_cart', [])

    try:
        cars_in_cart.remove(car_id)
    except ValueError:
        pass

    request.session['cars_in_cart'] = cars_in_cart

    cars_in_cart_details = TouristPlace.objects.filter(pk__in=cars_in_cart)

    subtotal = calculate_subtotal(cars_in_cart)
    total = calculate_total_with_taxes(subtotal)

    context = {
        'cars_in_cart': cars_in_cart_details,
        'subtotal': subtotal,
        'total': total,
    }

    return render(request, 'contact.html', context)

