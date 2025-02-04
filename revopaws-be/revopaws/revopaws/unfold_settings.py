from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

def is_group_member(request, group_name):
    """ Helper untuk mengecek apakah user adalah anggota dari group tertentu """
    return request.user.groups.filter(name=group_name).exists()

 # "permission": lambda request: request.user.is_superuser or is_group_member(request, 'doctor'),  # Hanya superuser(admin) / doctor yang biisa akses
 # "permission": lambda request: request.user.is_superuser or is_group_member(request, 'user') or is_group_member(request, 'doctor'),
UNFOLD = {
    "SITE_TITLE": "Revopaws",
    "SITE_HEADER": "Revopaws Admin",
    "SITE_URL": "/",
    "SITE_ICON": None,
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Navigasi Utama"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Manage Blog"),
                "separator": True,
                "collapsible": True,
                "permission": lambda request: request.user.is_superuser or is_group_member(request, 'Admin') or is_group_member(request, 'Doctor'),  # Otoritas admin sama dokter
                "items": [
                    {
                        "title": _("Kategori Blog"),
                        "icon": "category",
                        "link": reverse_lazy("admin:blog_blogcategory_changelist"),
                        "permission": lambda request: request.user.is_superuser or is_group_member(request, 'Admin') or is_group_member(request, 'Doctor'),
                    },
                    {
                        "title": _("Blog"),
                        "icon": "article",
                        "link": reverse_lazy("admin:blog_blogpost_changelist"),
                        "permission": lambda request: request.user.is_superuser or is_group_member(request, 'Admin') or is_group_member(request, 'Doctor'),
                    },
                    {
                        "title": _("Komentar Blog"),
                        "icon": "comment",
                        "link": reverse_lazy("admin:blog_blogcomment_changelist"),
                        "permission": lambda request: request.user.is_superuser or is_group_member(request, 'Admin'),  # otoritas khusus admin/ganti aja ini otoritas sesuain
                    },
                ],
            },
            {
                "title": _("Manage Chatbot"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("ChatAi"),
                        "icon": "chat",
                        "link": reverse_lazy("admin:chatbot_chatai_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Chat Realtime"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Chat Realtime"),
                        "icon": "chat_bubble",
                        "link": reverse_lazy("admin:chatrealtime_chatrealtime_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Konsultasi"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Konsultasi"),
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:consultation_consultation_changelist"),
                    },
                    {
                        "title": _("Review Dokter"),
                        "icon": "rate_review",
                        "link": reverse_lazy("admin:consultation_doctorreview_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Ecommerce"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Produk"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:ecommerce_product_changelist"),
                    },
                    {
                        "title": _("Produk Review"),
                        "icon": "star",
                        "link": reverse_lazy("admin:ecommerce_productreview_changelist"),
                    },
                    {
                        "title": _("Order"),
                        "icon": "receipt",
                        "link": reverse_lazy("admin:ecommerce_order_changelist"),
                    },
                    {
                        "title": _("Item Order"),
                        "icon": "list_alt",
                        "link": reverse_lazy("admin:ecommerce_orderitem_changelist"),
                    },
                    {
                        "title": _("Shipping"),
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:ecommerce_shipping_changelist"),
                    },
                    {
                        "title": _("Invoice"),
                        "icon": "description",
                        "link": reverse_lazy("admin:ecommerce_invoice_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Edukasi"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Edukasi"),
                        "icon": "school",
                        "link": reverse_lazy("admin:education_educationalcontent_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Forum"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Kategori Forum"),
                        "icon": "category",
                        "link": reverse_lazy("admin:forum_forumcategory_changelist"),
                    },
                    {
                        "title": _("Topik Forum"),
                        "icon": "forum",
                        "link": reverse_lazy("admin:forum_forumtopic_changelist"),
                    },
                    {
                        "title": _("Post Forum"),
                        "icon": "edit",
                        "link": reverse_lazy("admin:forum_forumpost_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Payment"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Payment"),
                        "icon": "payment",
                        "link": reverse_lazy("admin:payment_paymentlog_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Hewan"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Hewan"),
                        "icon": "pets",
                        "link": reverse_lazy("admin:pet_pet_changelist"),
                    },
                    {
                        "title": _("Riwayat Hewan"),
                        "icon": "history",
                        "link": reverse_lazy("admin:pet_petmedicalrecord_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage Report"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Report"),
                        "icon": "assessment",
                        "link": reverse_lazy("admin:report_reportquestion_changelist"),
                    },
                ],
            },
            {
                "title": _("Manage User"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("User"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },

                    {
                        "title": _("User Profile"),
                        "icon": "account_circle",
                        "link": reverse_lazy("admin:users_userprofile_changelist"),
                    },
                    {
                        "title": _("Doctor"),
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:users_doctor_changelist"),
                    },
                    {
                        "title": _("Role"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    }

}

