from django import forms
from .models import Product


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 
            'name', 
            'sku',
            'image',
            'price_ghs', 
            'stock_quantity', 
            'description', 
            'specifications',
            'is_active', 
            'is_featured'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'bg-stone-950 border border-stone-700 text-stone-200 rounded-xl px-4 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none'
            }),
            'name': forms.TextInput(attrs={
                'class': 'bg-stone-950 border border-stone-700 text-stone-200 rounded-xl px-4 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none',
                'placeholder': 'e.g. Wall-Mounted Anti-Slip Bath Rails'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'bg-stone-950 border border-stone-700 text-stone-200 rounded-xl px-4 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none',
                'placeholder': 'e.g. WF-SAN-001'
            }),
            'image': forms.FileInput(attrs={
                'class': 'bg-stone-950 border border-stone-700 text-stone-300 rounded-xl px-4 py-2 text-xs w-full focus:ring-1 focus:ring-emerald-500 file:mr-4 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-emerald-600 file:text-white hover:file:bg-emerald-500'
            }),
            'price_ghs': forms.NumberInput(attrs={
                'class': 'bg-stone-950 border border-stone-700 text-stone-200 rounded-xl px-4 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'bg-stone-950 border border-stone-700 text-stone-200 rounded-xl px-4 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-stone-950 border border-stone-700 text-stone-200 rounded-xl px-4 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none',
                'rows': 3,
                'placeholder': 'Product overview, dimensions, materials, and care details...'
            }),
            'specifications': forms.HiddenInput(),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded text-emerald-600 bg-stone-950 border-stone-700 focus:ring-emerald-500'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded text-emerald-600 bg-stone-950 border-stone-700 focus:ring-emerald-500'
            }),
        }

    gallery_images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'multiple': True,
            'class': 'bg-stone-950 border border-stone-700 text-stone-300 rounded-xl px-4 py-2 text-xs w-full focus:ring-1 focus:ring-emerald-500 file:mr-4 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-emerald-600 file:text-white hover:file:bg-emerald-500'
        })
    )


class QuickWhatsAppOrderForm(forms.Form):
    customer_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Full Name (e.g. Kwame Mensah)',
            'class': 'bg-stone-950 border border-stone-800 text-stone-100 rounded-xl px-3.5 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none'
        })
    )
    customer_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number (e.g. 024 412 3456)',
            'class': 'bg-stone-950 border border-stone-800 text-stone-100 rounded-xl px-3.5 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none'
        })
    )
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address (Optional)',
            'class': 'bg-stone-950 border border-stone-800 text-stone-100 rounded-xl px-3.5 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none'
        })
    )
    digital_address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'GhanaPost GPS or Area (e.g. GA-183-9024, Haatso)',
            'class': 'bg-stone-950 border border-stone-800 text-stone-100 rounded-xl px-3.5 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none'
        })
    )
    google_maps_url = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_google_maps_url'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'value': '1',
            'min': '1',
            'class': 'w-16 bg-stone-950 border border-stone-800 text-stone-100 rounded-xl px-2 py-2 text-xs text-center focus:outline-none focus:ring-1 focus:ring-emerald-500 font-bold'
        })
    )
    delivery_notes = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nearby landmark or gate color (Optional)',
            'class': 'bg-stone-950 border border-stone-800 text-stone-100 rounded-xl px-3.5 py-2.5 text-xs w-full focus:ring-1 focus:ring-emerald-500 focus:outline-none'
        })
    )