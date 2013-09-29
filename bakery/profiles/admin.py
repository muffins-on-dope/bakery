from django.contrib import admin

from bakery.profiles.models import Profile


class ProfileAdmin(VersionAdmin):

    search_fields = ("user__username", "github_account", "user__email", "email")
    list_display = ("github_account", "email", 'username_display', 'username_display')

    def username_display(self, obj):
        return (obj.user.username)
    username.short_description = "User username"


    def user_email_display(self, obj):
        return (obj.user.email)
    username.short_description = "User email"


admin.site.register(Profile, ProfileAdmin)
