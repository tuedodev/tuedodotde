from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from .utils import getHashString
from tuedo import settings, config
from .mixins import CaseInsensitiveFieldMixin
from django.utils.http import urlencode
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from meta.models import ModelMeta

User = get_user_model()

class CaseInsensitiveCharField(CaseInsensitiveFieldMixin, models.CharField):
    pass

class Author (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Category (models.Model):
    title = CaseInsensitiveCharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title
    
    @property
    def getStringLowercase(self):
        return f"{config.CATEGORY_PREFIX}{self.title.lower()}"
    
    @property
    def getURLEncode(self):
        return f"{urlencode({'category': self.title})}"

class BlogPost(ModelMeta, models.Model):

    language = models.PositiveSmallIntegerField(choices=config.LANGUAGES, default=1)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    tuedo_number = models.CharField(max_length=10, null=True, blank=True)
    meta = models.TextField(null=True, blank=True, default='{}') #models.JSONField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    keywords = models.CharField(max_length=255)
    summary = models.TextField()
    content = RichTextUploadingField() #models.TextField() #HTMLField()  / content = models.TextField()
    references = models.TextField(blank=True, null=True)
    image = models.ImageField()
    image_alt = models.CharField(max_length=100, null=True)
    featured = models.BooleanField(default=False)
    featured_position = models.PositiveSmallIntegerField(blank=True, null=True)
    draft = models.BooleanField(default=True)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    # Metadata
    _metadata = {
        'title': 'title',
        'description': 'summary',
        'image': 'get_meta_image',
    }

    def get_meta_image(self):
        if self.image:
            return self.image.url
    
    def get_absolute_url(self):
        language_slug = config.getLanguageShort(self.language)
        if language_slug == settings.LANGUAGE_CODE and config.LANGUAGE_DEFAULT_PREFIX is False:
            return reverse('blogpost', kwargs={'blog_slug': self.slug})
        else:
            return reverse('blogpost', kwargs={'language_slug': language_slug, 'blog_slug': self.slug})
    
    @property
    def absolute_url(self):
        return self.get_absolute_url()

    @property
    def get_tuedo_no(self):
        if self.tuedo_number:
            return self.tuedo_number
        return '#{:03d}'.format(self.id)
    

class Comment(models.Model):

    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment_body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    confirm_hash = models.CharField(max_length=20, default=getHashString)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        body = str(self.comment_body)
        return 'Kommentar {} von {}'.format(body[0:30], self.name)

    @property
    def blogpost_short(self):
        return self.blogpost.title[:30]
    
    @property
    def comment_body_short(self):
        return self.comment_body[:50]
    
    @property
    def comment_header(self):
        return (
            config.TEXT['comment_reply'] if self.reply else config.TEXT['comment'],
            config.TEXT['comment_by'],
            config.TEXT['comment_on'],
            config.TEXT['comment_at'],
        )

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=320)
    content = models.TextField()
    confirmed = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        content = str(self.content)
        return 'Nachricht von {}: {}'.format(self.name, content[0:30])

class Subscription(models.Model):
    subscription_email = models.EmailField(unique=True)
    subscribe_hash = models.CharField(max_length=20, default=getHashString)
    unsubscribe_hash = models.CharField(max_length=20, default=getHashString)
    date_joined = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.subscription_email

class Sitecontent(models.Model):
    site = models.PositiveSmallIntegerField(choices=config.SITES, null=True, blank=True)
    header = models.CharField(max_length=100, null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    position = models.PositiveSmallIntegerField(blank=True, null=True)
    draft = models.BooleanField(default=True)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-position', 'header', )
        verbose_name_plural = "sitecontent"

    def __str__(self):
        return f"{self.header[0:10]} {self.content[0:50]}"