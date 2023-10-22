from django import forms

import phonenumbers

from store.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone"]
        labels = {
            "name": "Ім'я",
            "email": "Електронна пошта",
            "phone": "Номер телефону",
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) > 50:
            raise forms.ValidationError(
                "Name is too long, max length is 50/Ім'я занадто вилеке, максимальна довжина 50"
            )

        if any(char.isdigit() for char in name):
            raise forms.ValidationError(
                "The name must not contain any numbers/Ім'я не повинно мати цифр"
            )

        return name

    def clean_email(self):
        email = self.cleaned_data["email"]
        if len(email) > 254:
            raise forms.ValidationError(
                "The e-mail address is too long/Адреса електронної пошти занадто довга"
            )

        # if "@" in email:
        #     raise forms.ValidationError(
        #         "The email address cannot be without an @ sign/Адреса електронної пошти не може бути без знаку @"
        #     )
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone:
            raise forms.ValidationError(
                "Phone cannot be empty/Поле телефон не може бути пустим"
            )

        if len(phone) < 9:
            raise forms.ValidationError(
                "The number provided is too short/Наданий номер занадто короткий"
            )

        try:
            parsed = phonenumbers.parse(phone, None)
        except phonenumbers.NumberParseException as error:
            raise forms.ValidationError(
                f"{error.args[0]}/Наданий рядок, схоже, не був номером телефону "
            )

        formatted_phone = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        return formatted_phone
