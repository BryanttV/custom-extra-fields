"""
Forms for custom extra fields.
"""

from datetime import datetime
import re

from django import forms
from django.forms import ModelForm

from custom_extra_fields.models import CustomExtraFields


def validate_nickname(value: str) -> None:
    """
    Validate the nickname for realistic constraints.
    """
    # Only allow alphanumeric characters, underscores, and hyphens
    if not re.match(r"^[a-zA-Z0-9_-]+$", value):
        raise forms.ValidationError("Nickname can only contain letters, numbers, underscores, and hyphens.")

    # Cannot be only numbers
    if value.isdigit():
        raise forms.ValidationError("Nickname cannot be only numbers.")


def validate_birthdate(value: str) -> None:
    """
    Validate the birthdate for realistic constraints.
    """
    # Must be in the format YYYY/MM/DD
    if not re.match(r"^\d{4}/\d{2}/\d{2}$", value):
        raise forms.ValidationError("Date of birth must be in the format YYYY/MM/DD.")

    # Must be a valid date
    try:
        datetime.strptime(value, "%Y/%m/%d")
    except ValueError as exc:
        raise forms.ValidationError("Date of birth must be a valid date.") from exc


class CustomExtraFieldsForm(ModelForm):
    """
    Form that represents user extra info and is compatible with edX's FormDescription system.

    Adding a field as 'required' will make it mandatory for the user to fill it in, and
    and will show it in the registration form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Text fields
        self.fields["nickname"].help_text = "Enter your nickname."
        self.fields["nickname"].min_length = 3
        self.fields["nickname"].max_length = 50
        self.fields["nickname"].validators = [validate_nickname]
        self.fields["nickname"].restrictions = {
            "min_length": 3,
            "max_length": 50,
        }
        self.fields["nickname"].error_messages = {
            "required": "Please enter a nickname to identify you.",
        }

        self.fields["birthdate"].help_text = "Enter your date of birth."
        self.fields["birthdate"].error_messages = {
            "required": "Please enter your date of birth.",
        }
        self.fields["birthdate"].validators = [validate_birthdate]

        # Text area field
        self.fields["interests"].help_text = "Tell us about your hobbies and interests."
        self.fields["interests"].error_messages = {
            "required": "Please tell us about your interests.",
        }

        # Check box field
        self.fields["wants_newsletter"].help_text = "Subscribe to our newsletter to get the latest news and updates."
        self.fields["wants_newsletter"].label = "Subscribe to newsletter?"

        # Select field
        self.fields["favorite_language"].help_text = "Pick your preferred programming language."

    class Meta:
        model = CustomExtraFields
        fields = [
            "nickname",
            "birthdate",
            "interests",
            "wants_newsletter",
            "favorite_language",
        ]

        serialization_options = {
            "nickname": {
                "default": "Funny Nickname",
            },
        }
