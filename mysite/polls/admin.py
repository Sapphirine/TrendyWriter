from django.contrib import admin
from polls.models import WordDigest

# Register your models here.

class WordDigestAdmin(admin.ModelAdmin):
    # ...
    list_display = ('word_text', 'word_count', 'retrive_date')
    list_filter = ['retrive_date']
    search_fields = ['word_text']

admin.site.register(WordDigest, WordDigestAdmin)