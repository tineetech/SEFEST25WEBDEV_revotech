from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.marketplace.models import Order, Product, ProductCategory
from apps.payments.models import PaymentOption, SwapRecord
from apps.trash.models import Trash, TrashRecord
from apps.users.models import CustomUser

class CustomAdminSite(admin.AdminSite):
    site_header = "Revosistem Admin Panel"
    site_title = "Revosistem"
    index_title = "Selamat Datang di Revosistem Admin"

    ROLE_MODEL_ACCESS = {
        'seller': ['product', 'productcategory', 'order'],
        'admin': ['trash', 'trashrecord', 'paymentoption', 'swaprecord', 'customuser'],
        'petugas': ['trash', 'trashrecord', 'paymentoption', 'swaprecord', 'customuser'],
    }

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        user_groups = set(group.name.lower() for group in request.user.groups.all())

        allowed_models = set()
        for group in user_groups:
            allowed_models.update(self.ROLE_MODEL_ACCESS.get(group, []))

        filtered_apps = []
        for app in app_list:
            new_models = [model for model in app['models'] if model['object_name'].lower() in allowed_models]

            if new_models:
                filtered_apps.append({
                    'name': app['name'],
                    'app_label': app['app_label'],
                    'app_url': app['app_url'],
                    'has_module_perms': app['has_module_perms'],
                    'models': new_models
                })
        return filtered_apps


admin_site = CustomAdminSite(name='revosistem_admin')

admin_site.register(CustomUser, UserAdmin)
admin_site.register(Product)
admin_site.register(ProductCategory)
admin_site.register(Order)
admin_site.register(PaymentOption)
admin_site.register(SwapRecord)
admin_site.register(Trash)
admin_site.register(TrashRecord)
