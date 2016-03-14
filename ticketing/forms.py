from django import forms
from .models import Client, Product, FeatureRequest


class FeatureRequestForm(forms.ModelForm):
    """
            Form for Creating Feature Request
    """

    class Meta:
        model = FeatureRequest
        fields = [
            'title',
            'desc',
            'targetdate',
            'url',
            'client',
            'productarea']

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-md-7 col-xs-12',
                'placeholder': 'New Feature Request',
                'required': 'required',
            }
        ),
        label='Feature Title',
        max_length=300,
        help_text="A short descriptive name",
        required=True,
    )

    desc = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 0,
                'cols': 0,
                'required': 'required',
            }
        ),
        label='Description',
        help_text="A long description of the feature request.",
        required=True,
        error_messages={
            'required': 'Please enter a description of the feature request.',
        }
    )

    # priority	= forms.IntegerField(
    # widget			= forms.NumberInput(
    # attrs = {
    # 'class': 'form-control col-md-7 col-xs-12',
    # 'placeholder': 'Enter Priority Number',
    # 'required': 'required',
    # 'value': 0,
    # }
    # ),
    # min_value 		= 0,
    # required		= False,
    # label			= 'Feature Priority',
    # help_text		= 'Priority number should be unique for specific client. If you leave this to 0 then application will automatically give the latest priority number while saving.'
    # )

    targetdate = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control has-feedback-left',
                'placeholder': '03/05/2016',
                'required': 'required',
                'aria-describedby': 'inputSuccess2Status',
            },
        ),
        label='Target Date',
        input_formats=['%m/%d/%Y'],
    )

    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control col-md-7 col-xs-12',
                'placeholder': 'Enter URL',
            }
        ),
        label='Feature URL',
        required=False,
    )

    client = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control required',
            },
        ),
        queryset=Client.objects.all(),
        empty_label=("Choose An Option"),
        label='Client',
        required=True,
    )

    productarea = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control required',
            },
        ),
        queryset=Product.objects.all(),
        empty_label=("Choose An Option"),
        label='Product Area',
        required=True,
    )


class SortRequestForm(forms.ModelForm):
    """
            Form for Sorting Feature Request
    """

    class Meta:
        model = FeatureRequest
        fields = ['client']

    client = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-control required',
            },
        ),
        queryset=Client.objects.all(),
        empty_label=("Choose An Option"),
        label='Client',
        required=True,
    )
