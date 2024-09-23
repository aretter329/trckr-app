from django.contrib import admin
from coach.models import Program, Tag, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_joined')
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    model = Program

    list_display = (
        "id",
        "title",
        "slug",
        "date_created",
        "published",
    )
    list_filter = (
        "published",
        "date_created",
    )
    list_editable = (
        "title",
        "slug",
        "published",
    )
    search_fields = (
        "title",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug": (
            "title",
        )
    }
    date_hierarchy = "date_created"
    save_on_top = True