from django.forms import ModelForm
from .models import Load, DetailUser

class LoadForm(ModelForm):
    class Meta:
        model = Load
        fields = '__all__'
        exclude = ['created', 'updated', 'participants', 'user', 'pickX', 'pickY', 'dropX', 'dropY']


class EditProfileForm(ModelForm):
    class Meta:
        model = DetailUser
        fields = '__all__'
        exclude = ['emailConfirmed', 'documentsConfirmed', 'user']