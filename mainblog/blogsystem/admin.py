from django.contrib import admin
from blogsystem.models import MessageText, Message,Link

# Register your models here.

class MessageTextAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('title', 'from_user', 'message_type','create_time')
    list_filter = ('create_time',)
    fields = ('title', 'text',
             'from_user', 'message_type')

class MessageAdmin(admin.ModelAdmin):
    search_fields = ('to_user',)
    list_display = ('message_text', 'to_user', 'is_read')
    list_filter = ('message_text',)
    fields = ('message_text', 'to_user', 'is_read')

class LinkAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'url')
    list_filter = ('create_time',)
    fields = ('title', 'url', 'type')


admin.site.register(MessageText, MessageTextAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Link, LinkAdmin)
