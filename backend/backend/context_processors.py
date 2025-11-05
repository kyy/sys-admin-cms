from home.models import ServiceSection, BlogPage

def global_data(request):
    """Глобальные данные доступные на всех страницах"""
    return {
        'global_service_sections': ServiceSection.objects.live().public(),
        'recent_blog_posts': BlogPage.objects.live().public().order_by('-first_published_at')[:3],
    }