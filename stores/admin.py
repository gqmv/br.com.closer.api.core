from django.contrib import admin

from .models import Store, RegularCampaign, CampaignUser, WelcomeCampaign


class WelcomeCampaignAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "id",
        "name",
        "reward_id",
        "reward_name",
        "reward_qty",
    )
    search_fields = (
        "name",
        "reward_id",
        "reward_name",
    )


class WelcomeCampaignInline(admin.StackedInline):
    model = WelcomeCampaign


class StoreAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    inlines = [WelcomeCampaignInline]


class CampaignAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "name",
        "item_id",
        "item_name",
        "item_qty",
        "reward_id",
        "reward_name",
        "reward_qty",
        "store",
    )
    search_fields = (
        "name",
        "item_id",
        "item_name",
        "reward_id",
        "reward_name",
        "store",
    )


class CampaignUserAdmin(admin.ModelAdmin):
    ordering = ("campaign", "user")
    list_display = ("campaign", "user", "progress")
    search_fields = ("campaign", "user")


admin.site.register(Store, StoreAdmin)
admin.site.register(RegularCampaign, CampaignAdmin)
admin.site.register(CampaignUser, CampaignUserAdmin)
