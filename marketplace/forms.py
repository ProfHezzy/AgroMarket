from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, ProductReview, Category


class ProductForm(forms.ModelForm):
    """Form for creating and editing products."""
    
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'description', 'price', 'unit', 'condition',
            'quantity_available', 'minimum_order', 'location', 'shipping_available',
            'shipping_cost', 'meta_title', 'meta_description'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'rows': 5,
                'placeholder': 'Describe your product in detail'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'step': '0.01',
                'min': '0'
            }),
            'unit': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'
            }),
            'condition': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'
            }),
            'quantity_available': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'min': '0'
            }),
            'minimum_order': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'min': '1'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Enter your location'
            }),
            'shipping_available': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-green-600 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50'
            }),
            'shipping_cost': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'step': '0.01',
                'min': '0'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'SEO title (optional)'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'rows': 3,
                'placeholder': 'SEO description (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)


class ProductImageForm(forms.ModelForm):
    """Form for product images."""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_main', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Image description'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-green-600 shadow-sm focus:border-green-300 focus:ring focus:ring-green-200 focus:ring-opacity-50'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'min': '0'
            }),
        }


# Create formset for multiple product images
ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,
    can_delete=True,
    max_num=10
)


class ProductReviewForm(forms.ModelForm):
    """Form for product reviews."""
    
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Review title'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
        }


class ProductSearchForm(forms.Form):
    """Form for product search and filtering."""
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Search products...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Min price'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Max price'
        })
    )
    condition = forms.ChoiceField(
        choices=[('', 'Any Condition')] + Product.CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'
        })
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('price', 'Price: Low to High'),
            ('-price', 'Price: High to Low'),
            ('name', 'Name: A to Z'),
            ('-name', 'Name: Z to A'),
            ('-view_count', 'Most Popular'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500'
        })
    )