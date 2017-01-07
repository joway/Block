from django.contrib import admin

from feed.models import Feed, FeedStream


class StreamAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'feed', 'created_at']

    class Meta:
        model = FeedStream


admin.site.register(Feed)
admin.site.register(FeedStream, StreamAdmin)
