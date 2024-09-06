from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED



def get_products_from_cache():
    """
    Get product_list from cache if available.
    If product_list not found in cache, set data from cache.
    """
    if not CACHE_ENABLED:
        return Product.objects.all()
    cache_key = 'product_list'
    products_from_cache = cache.get(cache_key)
    if products_from_cache is not None:
        return products_from_cache
    products_from_cache = Product.objects.all()
    cache.set(cache_key, products_from_cache)
    return products_from_cache

def get_categories_from_cache():
    """
    Get categories_list from cache if available.
    If categories_list not found in cache, set data from cache.
    """
    if not CACHE_ENABLED:
        return Category.objects.all()
    cache_key = 'categories_list'
    categories_from_cache = cache.get(cache_key)
    if categories_from_cache is not None:
        return categories_from_cache
    categories_from_cache = Category.objects.all()
    cache.set(cache_key, categories_from_cache)
    return categories_from_cache
