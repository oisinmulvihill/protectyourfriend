from django import forms


POLICY_TYPE = (
    ("annual", "Annual Cover"),
    ("lifetime", "Lifetime Cover"),
    ("preexisting", "Pre-existing Condition Cover"),
)


ANIMALS = (
    ("dog", "Dog"),
    ("cat", "Cat"),
)


BREEDS = (
    ("american_curl", "American Curl"),
    ("american_short_hair", "American Short Hair"),
    ("bombay", "Bombay"),
    ("border_collie", "Border Collie"),
    ("british_short_hair", "British Short Hair"),
    ("dalmation", "Dalmation"),
    ("miniature_schnauzer", "Miniature Schnauzer"),
    ("shiba_Inu", "Shiba Inu"),
    ("west_highland_white", "West Highland White Terrier"),
)


class QuoteForm(forms.Form):

    policy_type = forms.ChoiceField(
        label='Policy Type',
        required=True,
        disabled=False,
        choices=POLICY_TYPE,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is required."}
    )

    species = forms.ChoiceField(
        label='Animal',
        required=True,
        disabled=False,
        choices=ANIMALS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is required."}
    )

    breed = forms.ChoiceField(
        label='Breed',
        required=True,
        disabled=False,
        choices=BREEDS,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': "This field is required."}
    )

    age = forms.IntegerField(
        label="Your Pet's Age",
        min_value=0
    )

    excess = forms.IntegerField(
        label="Voluntary Excess",
        required=False,
        min_value=0,
        max_value=100000
    )
