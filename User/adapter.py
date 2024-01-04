from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from User.models import CustomUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        u = super().save_user(request, sociallogin, form=form)

        # Save data from the social account to the CustomUser model
        if sociallogin.account.provider == 'google':
            u.save_social_account_data(sociallogin.account)

        return u