from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from apps.marketplace.models import Order, Product, ProductCategory
from apps.payments.models import PaymentOption, SwapRecord
from apps.trash.models import Trash, TrashRecord
from apps.users.models import CustomUser


class CustomAdminSite(admin.AdminSite):
    site_header = "Greenloop Admin Panel"
    site_title = "Greenloop"
    index_title = "Selamat Datang di Greenloop Admin"

    # filter model di sidebar
    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # get group user
        user_groups = set(group.name for group in request.user.groups.all())

        # Filter model sesuai role (berdasarkan group)
        filtered_apps = []
        for app in app_list:
            new_models = []
            for model in app['models']:
                model_name = model['object_name'].lower()

                # Logic filtering model sesuai group
                if 'seller' in user_groups:
                    if model_name in ['product', 'productcategory', 'order']:
                        new_models.append(model)
                elif 'admin' in user_groups or 'petugas' in user_groups:
                    if model_name in ['trash', 'trashrecord', 'paymentoption', 'swaprecord', 'customuser']:
                        new_models.append(model)

            # Tambahin aja app kalo punya model yang cocok
            if new_models:
                filtered_apps.append({
                    'name': app['name'],
                    'app_label': app['app_label'],
                    'app_url': app['app_url'],
                    'has_module_perms': app['has_module_perms'],
                    'models': new_models
                })
        return filtered_apps


admin_site = CustomAdminSite(name='greenloop_admin')

# register all model 
admin_site.register(CustomUser, UserAdmin)
admin_site.register(Product)
admin_site.register(ProductCategory)
admin_site.register(Order)
admin_site.register(PaymentOption)
admin_site.register(SwapRecord)
admin_site.register(Trash)
admin_site.register(TrashRecord)
