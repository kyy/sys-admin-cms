from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class ServiceSection(Page):
    template = 'home/service_section.html'

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('description'),
    ]

    subpage_types = ['ServiceCategory']  # В секции могут быть только категории
    parent_page_types = ['HomePage']  # Секции создаются на главной

    def get_context(self, request):
        context = super().get_context(request)
        # Получаем все категории в этой секции
        context['service_categories'] = ServiceCategory.objects.child_of(self).live()
        return context


class ServiceCategory(Page):
    template = 'home/service_category.html'

    category_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('category_image'),
        FieldPanel('description'),
    ]

    subpage_types = ['Service']  # В категории могут быть только услуги
    parent_page_types = ['ServiceSection']  # Категории создаются в секциях

    def get_context(self, request):
        context = super().get_context(request)
        # Получаем все услуги в этой категории
        context['services'] = Service.objects.child_of(self).live()
        # Получаем родительскую секцию
        context['service_section'] = self.get_parent().specific
        return context


class Service(Page):
    template = 'home/service_page.html'

    service_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    short_description = RichTextField(
        max_length=300,
        features=['bold', 'italic', 'link'],
        blank=True
    )
    full_description = RichTextField(blank=True)


    featured = models.BooleanField(
        default=False,
        verbose_name="Рекомендуемая услуга"
    )

    content_panels = Page.content_panels + [
        FieldPanel('service_image'),
        FieldPanel('short_description'),
        FieldPanel('full_description'),
        FieldPanel('featured'),
    ]

    parent_page_types = ['ServiceCategory']  # Услуги создаются в категориях

    def get_service_section(self):
        """Получить секцию услуг через категорию"""
        category = self.get_parent().specific
        return category.get_parent().specific


class BlogTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogIndex(Page):
    template = 'home/blog_index.html'

    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    subpage_types = ['BlogPage']

    def get_context(self, request):
        context = super().get_context(request)
        context['posts'] = BlogPage.objects.child_of(self).live().order_by('-first_published_at')
        return context


class BlogPage(Page):
    template = 'home/blog_page.html'

    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = ClusterTaggableManager(through=BlogTag, blank=True)
    excerpt = RichTextField(
        max_length=400,
        features=['bold', 'italic'],
        blank=True
    )
    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('blog_image'),
        FieldPanel('tags'),
        FieldPanel('excerpt'),
        FieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('excerpt'),
        index.SearchField('content'),
        index.SearchField('tags'),
    ]

    parent_page_types = ['BlogIndex']


class HomePage(Page):
    template = 'home/home_page.html'

    featured_services_description = RichTextField(
        blank=True,
        verbose_name="Описание рекомендуемых услуг"
    )

    # Добавляем дополнительные поля для главной страницы
    hero_title = RichTextField(
        blank=True,
        features=['bold', 'italic'],
        verbose_name="Заголовок героя"
    )
    hero_description = RichTextField(
        blank=True,
        features=['bold', 'italic'],
        verbose_name="Описание героя"
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Изображение героя"
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_description'),
        FieldPanel('hero_image'),
        FieldPanel('featured_services_description'),
    ]

    subpage_types = ['ServiceSection', 'BlogIndex']

    def get_context(self, request):
        context = super().get_context(request)
        context['service_sections'] = ServiceSection.objects.child_of(self).live()
        context['featured_services'] = Service.objects.live().filter(featured=True)[:6]
        context['blog_posts'] = BlogPage.objects.live().order_by('-first_published_at')[:3]
        return context