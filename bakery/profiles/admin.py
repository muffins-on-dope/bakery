from django.contrib import admin

from bakery.profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):

    search_fields = ("user__username", "user__email")
    list_display = ('username_display', 'user_email_display')

    def username_display(self, obj):
        return (obj.user.username)
    username_display.short_description = "User username"


    def user_email_display(self, obj):
        return (obj.user.email)
    username_display.short_description = "User email"


admin.site.register(Profile, ProfileAdmin)
