from django.contrib.auth.models import User
from django.contrib import admin
from crimsononline.subscriptions.models import EmailSubscription, PaperSubscription, PaperPromoCode

class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_on', 'is_active',)
    actions = ['action_deactivate', 'action_activate']
    
    def action_deactivate(self, request, queryset):
        """Deactivate the subscriptions"""
        rows_updated = queryset.update(is_active=False)
        message_bit = "1 subscription was" if rows_updated == 1 \
                 else "%s subscriptionss were" % rows_updated
        self.message_user(request, "%s successfully deactivated." % message_bit)
    
    action_deactivate.short_description = 'Deactivate selected subscriptions'
    
    def action_activate(self, request, queryset):
        """Activate the subscriptions"""
        rows_updated = queryset.update(is_active=True)
        message_bit = "1 subscription was" if rows_updated == 1 \
                 else "%s subscriptionss were" % rows_updated
        self.message_user(request, "%s successfully activated." % message_bit)
    
    action_activate.short_description = 'Activate selected subscriptions'

admin.site.register(EmailSubscription, EmailSubscriptionAdmin)

class PaperPromoCodeInline(admin.TabularInline):
    model = PaperPromoCode

class PaperSubscriptionAdmin(admin.ModelAdmin):
    inlines = [
        PaperPromoCodeInline,
    ]
    
admin.site.register(PaperSubscription, PaperSubscriptionAdmin)