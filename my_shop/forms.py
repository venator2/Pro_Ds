from django import forms
from django.contrib.auth.models import User
from .models import Order, UserProfile

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Ім'я користувача (Логін)")
    first_name = forms.CharField(max_length=30, label="Ім'я")
    last_name = forms.CharField(max_length=30, label="Прізвище")
    email = forms.EmailField(required=False, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Підтвердження паролю')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ця електронна адреса вже використовується.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Паролі не збігаються.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Створюємо профіль тільки якщо він ще не існує
            UserProfile.objects.get_or_create(user=user)
        return user



class OrderForm(forms.ModelForm):
    shipping_address = forms.CharField(label='Адреса доставки', widget=forms.Textarea)
    additional_phone_number = forms.CharField(label='Номер телефону', max_length=15, required=False)

    class Meta:
        model = Order
        fields = ['shipping_address', 'additional_phone_number']

    def save(self, user=None, cart=None, commit=True):
        if user is None or cart is None:
            raise ValueError("Користувач і кошик повинні бути надані.")

        order = super().save(commit=False)
        order.user = user
        order.first_name = user.first_name
        order.last_name = user.last_name
        if commit:
            order.save()
            for item in cart.items.all():
                order.products.add(item.product)
            cart.delete()
        return order
