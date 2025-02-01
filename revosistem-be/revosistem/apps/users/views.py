from django.shortcuts import render
from django.contrib.auth.models import User
from apps.users.models import CustomUser, UserItems
from django.db.models import Count, Sum
from datetime import timedelta
from django.utils.timezone import now

def users_dashboard(request):
    # Statistik pengguna
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(status=True).count()
    inactive_users = CustomUser.objects.filter(status=False).count()

    # Pengguna online (last login dalam 24 jam terakhir)
    online_users = CustomUser.objects.filter(last_login__gte=now() - timedelta(hours=24)).count()

    # Distribusi membership
    membership_distribution = CustomUser.objects.values('membership').annotate(count=Count('membership'))

    # Pengguna paling aktif menukarkan sampah ke koin
    top_users_by_koin = UserItems.objects.order_by('-total_penukaran_sampah')[:5]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'online_users': online_users,
        'membership_distribution': membership_distribution,
        'top_users_by_koin': top_users_by_koin,
    }
    
    return render(request, 'users/dashboard.html', context)
