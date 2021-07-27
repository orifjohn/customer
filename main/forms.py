from django.core.exceptions import ValidationError
from django.forms import Form, fields, widgets, forms


class CustomerForm(Form):
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    phone_number = fields.CharField(max_length=13)
    address = fields.CharField(widget=widgets.Textarea())

    def clean(self):
        cd = self.cleaned_data
        # if '$' not in cd.get('address'):
        #     self.add_error('address', 'Dollar bolish kerak')
        phone_number = cd.get('phone_number', None)
        if phone_number:
            if phone_number[:4] != '+998':
                self.add_error('phone_number', 'Please enter uzb numbers (998)')
            if phone_number[4:6] not in ['33', '99', '98']:
                self.add_error('phone_number', 'Enter an available numbers')
            if phone_number[1:].isdigit():
                self.add_error('phone_number', 'Please, enter the numbers')
        return cd


class LoginForm(Form):
    username = fields.CharField(max_length=100)
    password = fields.CharField(max_length=100)

