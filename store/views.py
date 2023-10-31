from django.shortcuts import render, get_object_or_404, redirect  # , redirect,
from django.urls import reverse

from .models import Shoe, \
    Cart, \
    Order  # , NewArrival, Favorite, CartItem, Order, UserProfile, ContactMessage, AboutPage, TermsAndConditionsPage, PrivacyPolicyPage, FAQPage

def index(request):
    all_shoes = Shoe.objects.all()
    return render(request, 'store/index.html', {'shoes': all_shoes})

def product_detail(request, slug):
    shoe = get_object_or_404(Shoe, slug=slug)
    return render(request, 'store/product_detail.html', {'shoe': shoe})


def add_to_cart(request, slug):
    user = request.user
    shoe = get_object_or_404(Shoe, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,
                                                 is_completed=False,
                                                 shoe=shoe)
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("shoe",  kwargs={"slug": slug}))

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    return render(request, 'store/cart.html', {"orders": cart.orders.all()})

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()

    return redirect('index')


"""
def category_view(request, category_name):
    shoes = Shoe.objects.filter(category__name=category_name)
    context = {
        'category_name': category_name,
        'shoes': shoes,
    }
    return render(request, 'store/category.html', context)


def new_arrivals(request):
    new_arrivals = NewArrival.objects.select_related('shoe').all()
    return render(request, 'store/new_arrivals.html', {'new_arrivals': new_arrivals})

def shoes_by_gender(request, gender):
    gender_shoes = Shoe.objects.filter(gender=gender)
    return render(request, 'store/shoes_by_gender.html', {'gender_shoes': gender_shoes})

def search_results(request):
    query = request.GET.get('q')
    results = Shoe.objects.filter(name__icontains=query)
    return render(request, 'store/search_results.html', {'query': query, 'results': results})

def favorites(request):
    user = request.user
    user_favorites = Favorite.objects.filter(user=user)
    return render(request, 'store/favorites.html', {'user_favorites': user_favorites})

def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    return render(request, 'store/cart.html', {'cart_items': cart_items})


def checkout(request):
    # Ajoutez ici la logique pour gérer le paiement
    return render(request, 'store/checkout.html')

def order_confirmation(request):
    # Ajoutez ici la logique pour afficher la confirmation de commande
    return render(request, 'store/order_confirmation.html')

def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_orders = Order.objects.filter(user=user)
    return render(request, 'store/profile.html', {'user_profile': user_profile, 'user_orders': user_orders})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('contact')  # Redirige vers la page de contact
    return render(request, 'store/contact.html')

def about(request):
    about_page = AboutPage.objects.first()
    return render(request, 'store/about.html', {'about_page': about_page})

def terms_and_conditions(request):
    terms_page = TermsAndConditionsPage.objects.first()
    return render(request, 'store/terms_and_conditions.html', {'terms_page': terms_page})

def privacy_policy(request):
    privacy_page = PrivacyPolicyPage.objects.first()
    return render(request, 'store/privacy_policy.html', {'privacy_page': privacy_page})

def faq(request):
    faq_page = FAQPage.objects.first()
    return render(request, 'store/faq.html', {'faq_page': faq_page})
"""