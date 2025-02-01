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

    # Konfigurasi model yang ditampilkan per role (group)
    ROLE_MODEL_ACCESS = {
        'seller': ['product', 'productcategory', 'order'],
        'admin': ['trash', 'trashrecord', 'paymentoption', 'swaprecord', 'customuser'],
        'petugas': ['trash', 'trashrecord', 'paymentoption', 'swaprecord', 'customuser'],
    }

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # Dapatkan role (group) user
        user_groups = set(group.name.lower() for group in request.user.groups.all())

        # Tentukan model yang boleh ditampilkan berdasarkan group
        allowed_models = set()
        for group in user_groups:
            allowed_models.update(self.ROLE_MODEL_ACCESS.get(group, []))

        # Filter app_list berdasarkan model yang diizinkan
        filtered_apps = []
        for app in app_list:
            new_models = [model for model in app['models'] if model['object_name'].lower() in allowed_models]

            # Tambahkan app jika memiliki model yang sesuai
            if new_models:
                filtered_apps.append({
                    'name': app['name'],
                    'app_label': app['app_label'],
                    'app_url': app['app_url'],
                    'has_module_perms': app['has_module_perms'],
                    'models': new_models
                })
        return filtered_apps


# Custom Admin Site Registration
admin_site = CustomAdminSite(name='revosistem_admin')

# Register semua model yang dibutuhkan
admin_site.register(CustomUser, UserAdmin)
admin_site.register(Product)
admin_site.register(ProductCategory)
admin_site.register(Order)
admin_site.register(PaymentOption)
admin_site.register(SwapRecord)
admin_site.register(Trash)
admin_site.register(TrashRecord)
