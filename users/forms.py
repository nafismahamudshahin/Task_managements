from django import forms
import re
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , PasswordChangeForm , PasswordResetForm , SetPasswordForm
from django.contrib.auth.models import User , Group ,Permission
from tasks.forms import StyledFormMixin
from users.models import CustomUser

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

# password change view:
class CustomPasswordChangeForm(PasswordChangeForm , StyledFormMixin):
    def __init__(self, *arg, **kwarg):
        super(PasswordChangeForm , self).__init__(*arg, **kwarg)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
# Password Reset form:
class CustomPasswordResetForm(StyledFormMixin,PasswordResetForm):
    pass

# set Password form after reset:
class CustomPasswordConfirmForm(StyledFormMixin ,SetPasswordForm ):
    pass
# Login form:
class LoginForm(StyledFormMixin , AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

# custom use creation form using User
class CustomRegisterForm(StyledFormMixin,forms.ModelForm ):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields =['username','first_name','last_name','email','password','confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        e = CustomUser.objects.filter(email = email).exists()
        if e != False:
            raise forms.ValidationError(f"This Email alredy Exit {email}")
        return email

    def clean_username(self): # define field error
        username = self.cleaned_data.get('username')
        if " " in username:
            raise forms.ValidationError("space are not allow in username.")
        return username
    
    def clean_password(self): # Field Error
        password =self.cleaned_data.get('password')
        errors = []
        if len(password)<8:
            errors.append("Your password is very short, please give at least 8 charters")

        if 'abc' not in password:
            errors.append("abc not included in your password ")
        
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        
        if re.fullmatch(pattern,password):
            errors.append(f"Please include spacial char.{pattern}")

        if errors:
            raise forms.ValidationError(errors)

        return password
    
    def clean(self): # non field error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("password and confirm password are not same please try agin.")
        return cleaned_data

class RoleAssignedForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label= "Select a Group"
    )

class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset= Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = "assigned role",
    )

    class Meta:
        model = Group
        fields = ['name','permissions']

class EditProfileForm( StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','bio','image']


"""
# Edit User Profile:
class EditProfileForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email']
    
    bio = forms.CharField(required=False , widget=forms.Textarea , label="bio")
    image = forms.ImageField(required=False , label="Image")

    def __init__(self,*args,**kwargs):
        self.userprofile = kwargs.pop('userprofile' , None)
        super().__init__(*args,**kwargs)

        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['image'].initial = self.userprofile.image

    def save(self, commit = True):
        user = super().save(commit=False)
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.image = self.cleaned_data.get('image')
            if commit:
                self.userprofile.save()
        if commit:
            user.save()

        return user
"""