from random import choices
from users.models import Constituency, Country, Region
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


country = Country.objects.all()
cnt = []
for i in country:
    cnt.append((i.id,i.name))


region = Region.objects.all()
rgn = []
for i in region:
    rgn.append((i.id,i.name))


consti = Constituency.objects.all()
cst = []
for i in consti:
    cst.append((i.id,i.name))




class SignUpContForm(forms.Form):
    voters_id       = forms.CharField(max_length=15)
    town            = forms.CharField(max_length=50)
    country         = forms.ChoiceField(choices=cnt)
    region          = forms.ChoiceField(choices=rgn)
    constituency    = forms.ChoiceField(choices=cst)
    class Meta:
        model= User
        fields = ['email', 'full_name', 'date_of_birth', 'voters_id', 'town', 'contact', 'country','region', 'town', 'constituency', 'password']
