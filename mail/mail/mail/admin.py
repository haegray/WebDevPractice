from django.contrib import admin

# Register your models here.

from .models import Email, User
# Register your models here.

class EmailAdmin(admin.ModelAdmin):
    list_display = ("user","sender","show_recipients","subject","body","timestamp","read","archived")

    def show_recipients(self, obj):
            return "\n".join([a.username for a in obj.recipients.all()])
    
admin.site.register(Email, EmailAdmin)
