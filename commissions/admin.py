from django.contrib import admin
from .models import Commission, Comment

class CommissionAdmin(admin.ModelAdmin):
    model = Commission

    search_fields = ('title', )

class CommentAdmin(admin.ModelAdmin):
    model = Comment

    search_fields = ('commission', )

admin.site.register(Commission, CommissionAdmin)
admin.site.register(Comment, CommentAdmin)
