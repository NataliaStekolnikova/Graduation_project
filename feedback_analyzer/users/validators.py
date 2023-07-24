import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UniqueEmailValidator:
    def validate(self, email, user=None):
        if User.objects.filter(email=email).exclude(pk=user.pk if user else None).exists():
            raise ValidationError(_("This email address is already registered."), code="email_already_exists")

    def get_help_text(self):
        return _("This email address must be unique.")

class EmailFormatValidator:
    def validate(self, email, user=None):
        # Email Format Check
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError(_("Enter a valid email address."), code="invalid_email_format")

        # Domain Blacklist Check
        blacklisted_domains = ["example.com", "example.net", "example.org"]
        domain = email.split("@")[-1]
        if domain in blacklisted_domains:
            raise ValidationError(_("This email domain is not allowed."), code="email_domain_blacklisted")

        # Disposable Email Address Check
        disposable_domains = ["examplemail.com", "tempmail.com", "throwawaymail.com"]
        if domain in disposable_domains:
            raise ValidationError(_("Disposable email addresses are not allowed."), code="disposable_email")

        # Email Typo Suggestions Check (for demonstration purposes)
        common_typos = {"gmial.com": "gmail.com", "hotmal.com": "hotmail.com", "yahooo.com": "yahoo.com"}
        corrected_email = common_typos.get(email.lower())
        if corrected_email:
            raise ValidationError(_("Did you mean %(corrected_email)s?"), code="email_typo", params={"corrected_email": corrected_email})

    def get_help_text(self):
        return _("Your email address must be in a valid format.")
