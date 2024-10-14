
from django import forms
from .models import CartItem,Checkout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe




class CartItemForm(forms.ModelForm):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    size = forms.ChoiceField(choices=SIZE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}))

    class Meta:
        model = CartItem
        fields = ['product', 'size', 'quantity']
        widgets = {
            'product': forms.HiddenInput(),
        }
        

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['name', 'address', 'contact_number', 'payment_method']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'starts with country code! eg(+00)'
            }),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
        

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Username'
    }))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password',
            'id': 'password',  # Unique ID for targeting by JavaScript
            'style': 'padding-right: 30px;'  # Space for icon inside input
        })
    )

    def as_p(self):
        # Overriding the as_p method to render custom HTML, including the icon and JavaScript
        return mark_safe(f"""
            <p>{self['username'].label_tag()}{self['username']}</p>
            <p style="position: relative;">
                {self['password'].label_tag()}
                {self['password']}
                <span id="toggle-password" onclick="togglePasswordVisibility()" 
                      style="position: absolute; right: 10px; top: 35px; cursor: pointer;">
                    👁️
                </span>
            </p>
            <script>
                function togglePasswordVisibility() {{
                    var passwordInput = document.getElementById('password');
                    var toggleIcon = document.getElementById('toggle-password');
                    if (passwordInput.type === 'password') {{
                        passwordInput.type = 'text';
                        toggleIcon.textContent = '🙈'; // Change to hide icon
                    }} else {{
                        passwordInput.type = 'password';
                        toggleIcon.textContent = '👁️'; // Change to show icon
                    }}
                }}
            </script>
        """)
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
  



    




    

