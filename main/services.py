from django.core.cache import cache

from config.settings import CACHE_ENABLED
from main.models import Doctor


def get_doctor_from_cache():
    """
    Получение списка врачей из кэша или БД
    """
    if not CACHE_ENABLED:
        return Doctor.objects.all()
    else:
        key = 'doctors'
        doctors = cache.get(key)
        if doctors is not None:
            return doctors
        else:
            doctors = Doctor.objects.all()
            cache.set(key, doctors)
            return doctors
