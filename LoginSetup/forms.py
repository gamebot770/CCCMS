#forms.py
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):
    """Provides registration form for club heads"""
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    #to be fixed to validate against names from the campion database
    """
    def checkUsername(self):
        #Ensures name entered is a valid campionites name
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])#this should retrieve name from database
        except User.DoesNotExist:
            raise forms.ValidationError(_("This is not a valid Campionite name."))
        return self.cleaned_data['username']
    """
    def checkPassword(self):
        """Ensures the password entered is valid"""
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

        #temporary until passwords can be pulled
        def checkEmail(self):
            """"Verifies that Campion emails are used"""
            a = self.email.split('@')
            '''remember to fix this'''
            if a[0] != "however the import process works":
                raise form.ValidationError(_("You are not on record as a club head"))
            elif a[1] != 'campioncollege.com':
                raise forms.ValidationError(_("Only Campion emails are valid"))
            return self.cleaned_data
    """
    def checkEmail(self):
        #Verifies that Campion emails are used
        a = self.email.split('@')
        '''remember to fix this'''
        if a[0] != "however the import process works":
            raise form.ValidationError(_("You are not on record as a club head"))
        elif a[1] != 'campioncollege.com':
            raise forms.ValidationError(_("Only Campion emails are valid"))
        return self.cleaned_data
        """
        
'''Was an experiment'''
# class loginForm(forms.Form):
#     """Provides login service"""
#
#     email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
#     password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
#
#     def checkEmail(self):
#         """"Verifies that Campion emails are used"""
#         a = self.email.split('@')
#         '''remember to fix this'''
#         if a[0] != "however the import process works":
#             raise form.ValidationError(_("You are not on record as a club head"))
#         elif a[1] != 'campioncollege.com':
#             raise forms.ValidationError(_("Only Campion emails are valid"))
#         return self.cleaned_data
#
#     """This needs to pull password from database"""
#     def checkPassword(self):
#         """Ensures the password entered is valid"""
#         if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
#             if self.cleaned_data['password1'] != self.cleaned_data['password2']:
#                 raise forms.ValidationError(_("The two password fields did not match."))
#         return self.cleaned_data
