from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(
            super().get_readonly_fields(request, obj)
        )

        readonly_fields.extend(
            list(getattr(self, '_readonly_fields', []))
        )

        createonly_fields = list(getattr(self, 'createonly_fields', []))

        if obj:
            readonly_fields.extend(createonly_fields)

        return readonly_fields
