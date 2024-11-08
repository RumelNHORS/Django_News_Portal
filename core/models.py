from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode
from taggit.managers import TaggableManager

# Create your models here.

STATUS_CHOICES = (
    ('D', 'Draft'),
    ('P', 'Published')
)

HOME_NEWS_CHOICES = (
    ('S', 'Slider'),
    ('6', 'Top 6'),
    ('N', 'None'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True,)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True) # user avatar upload
    slug = AutoSlugField(populate_from='username', editable=True, null=True, blank=True)

    def __str__(self):
        return self.user.email


class SiteSettings(models.Model):
    site_title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=300, blank=True, null=True,
                                     help_text='Comma Separated Keyword for search engines')
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    copyright_text = models.CharField(max_length=120, blank=True, null=True)
    google_analytics_code = models.CharField(max_length=50, blank=True, null=True, help_text='Paste google analytics tracing code: ex. UA-69123876-4')
    alexa_code = models.CharField(max_length=50, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True, help_text='Input your Facebook page url')
    twitter = models.URLField(blank=True, null=True, help_text='Input your Twitter page url')
    youtube = models.URLField(blank=True, null=True, help_text='Input your YouTube page url')
    linkedin = models.URLField(blank=True, null=True, help_text='Input your LinkedIN page url')
    instagram = models.URLField(blank=True, null=True, help_text='Input your Instagram page url')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_title

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


class MainCategory(models.Model):
    title = models.CharField(max_length=200, blank=True, unique=True)
    # slug = AutoSlugField(populate_from=title, editable=True, unique=True, unique_with=['created__month', 'status'])
    slug = AutoSlugField(
        populate_from='title',
        editable=True,
        unique=True,
        unique_with=['created_at__month', 'status']
    )
    description = HTMLField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    featured = models.BooleanField(help_text='Select this content for main menu', default=False)
    sequence = models.PositiveIntegerField(blank=True, null=True, default=0)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Main Category'
        verbose_name_plural = 'Main Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:main-category-detail', args=[str(self.slug)])


class NewsRoom(models.Model):
    title = models.CharField(max_length=200, blank=True, unique=True)
    description = HTMLField(blank=True, null=True)
    sequence = models.CharField(max_length=3, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=200)
    # slug = AutoSlugField(populate_from='title', unique=True, editable=True, allow_unicode=True)
    slug = models.CharField(unique=True, null=False, blank=True, max_length=200)
    news_room = models.ForeignKey(
        'NewsRoom',
        on_delete=models.CASCADE, blank=True, help_text='Select news room', null=True,
    )
    main_category = models.ForeignKey(
        'MainCategory',
        on_delete=models.CASCADE, blank=False, help_text='Select main category'
    )
    is_home = models.BooleanField(help_text='Select this content for home page')
    description = HTMLField()
    content_image = models.ImageField(upload_to='content_images/', blank=False)
    quote_text = models.TextField(blank=True, null=True)
    image_caption = models.CharField(max_length=200, blank=True, null=True)
    video_link = models.CharField(max_length=100, blank=True, null=True, help_text='Input YouTube Video Embed Code')
    tags = TaggableManager()
    meta_title = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=300, blank=True, null=True, help_text='Comma Separated Keyword for search engines')
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='P')
    top_news = models.CharField(choices=HOME_NEWS_CHOICES, max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:news-detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)


class Page(models.Model):
    title = models.CharField(max_length=200)
    # slug = AutoSlugField(populate_from='title', unique=True, editable=True, allow_unicode=True)
    slug = models.CharField(unique=True, null=False, blank=True, max_length=200)
    description = HTMLField()
    content_image = models.ImageField(upload_to='content_images/', blank=True)
    image_caption = models.CharField(max_length=200, blank=True, null=True)
    meta_title = models.CharField(max_length=250, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=300, blank=True, null=True, help_text='Comma Separated Keyword for search engines')
    sequence = models.PositiveIntegerField(blank=True, null=True, default=0)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:page-detail', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)