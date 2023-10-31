from django.contrib import admin
from .models import Category, ShoeType, Shoe, \
    Order, \
    Cart  # , NewArrival, Favorite, CartItem, Order, OrderItem, ContactMessage, AboutPage, TermsAndConditionsPage, PrivacyPolicyPage, FAQPage, UserProfile

class ShoeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category)
admin.site.register(ShoeType)
admin.site.register(Shoe, ShoeAdmin)
admin.site.register(Order)
admin.site.register(Cart)


"""
class NewArrivalAdmin(admin.ModelAdmin):
    list_display = ('shoe',)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'shoe')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'shoe', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_price', 'is_completed')
    filter_horizontal = ('items',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'shoe', 'quantity', 'total_price')

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number', 'country', 'region')
"""

"""
admin.site.register(NewArrival, NewArrivalAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(AboutPage)
admin.site.register(TermsAndConditionsPage)
admin.site.register(PrivacyPolicyPage)
admin.site.register(FAQPage)
admin.site.register(UserProfile)
"""