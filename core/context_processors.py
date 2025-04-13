from .models import SiteConfig, Category

def site_config(request):
    try:
        return {
            'site_config': SiteConfig.objects.first(),
            'categories': Category.objects.all()
        }
    except Exception as e:
        # Fallback em caso de erro
        return {
            'site_config': None,
            'categories': []
        }