from lemon import extradmin as admin
from articles.models import Article, Note, Image


class NoteInline(admin.StackedInline):

    model = Note
    fieldsets = (
        (None, {
            'fields': ('content',),
        }),
        ('Activity', {
            'fields': ('is_active',),
        }),
    )


class ImageInline(admin.TabularInline):

    model = Image


class ArticleAdmin(admin.ModelAdmin):

    inlines = [NoteInline, ImageInline]
    tabs = True


admin.site.register(Article, ArticleAdmin)
