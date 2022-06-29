from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from cart.forms import CartAddProductForm
from main.models import Product, Category
from .forms import UserForm, ProfileForm
from .models import Profile
from concurrent.futures import ThreadPoolExecutor
import logging
logger = logging.getLogger(__name__)

# Create your views here.


def get_main_page(request):
    return render(request, "main/main.html", {})


def get_about_us_page(request):
    return render(request, "main/about_us.html", {})


def get_user_profile_page(request):
    user = request.user

    return render(request, 'main/user_profile.html', {"user": user})


def logout_user(request):
    user = request.user

    if user.is_authenticated:
        logout(request)

    return redirect('main')


def get_products_page(request):
    chosen_category = request.GET.get("category", "")

    if (chosen_category != ""):
        products = Product.objects.all().filter(category__slug=chosen_category)
    else:
        products = Product.objects.all()

    return render(request, "main/products.html", {'products': products, 'category':chosen_category})


def get_specific_product(request, slug):
    product = Product.objects.get(slug=slug)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'main/product.html', context)


def get_categories(request):
    categories = Category.objects.all()
    return render(request, "main/categories.html", {'categories': categories})


# user stuff
def get_login_page(request):
    if (request.method == 'POST'):
        with ThreadPoolExecutor() as executor:
            username_thread = executor.submit(request.POST.get, 'username')
            password_thread = executor.submit(request.POST.get, 'password')

            username = username_thread.result()
            password = password_thread.result()

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('categories')
            else:
                messages.info(request, 'Username or password is not correct')
                return render(request, 'main/login.html', {})
        except Exception as e:
            messages.error(request, 'No such user')
            logger.info('Wrong input')
            return redirect('login')
    else:
        return render(request, 'main/login.html', {})


def get_registration_page(request):
    if request.method == "POST":
        with ThreadPoolExecutor() as executor:
            username_thread = executor.submit(UserForm, request.POST)
            password_thread = executor.submit(ProfileForm, request.POST)

            user_form = username_thread.result()
            profile_form = password_thread.result()

        # Проверяем есть ли уже пользователь с таким адресом почты.
        email = request.POST.get('email')
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, 'This username already registred on site.')
            return redirect('registration')

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            profile_test = Profile.objects.get(user=new_user)
            profile_test.phone_number = profile_form.cleaned_data.get('phone_number', '')
            profile_test.address = profile_form.cleaned_data.get('address', '')
            profile_test.save()
            return redirect('login')
        else:
            messages.error(request, 'Your data is incorrect')
            return redirect('registration')

    elif request.method == "GET":
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'main/registration.html', {'form': user_form, 'profile_form': profile_form})