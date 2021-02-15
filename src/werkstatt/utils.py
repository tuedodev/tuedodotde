from PIL import Image, ImageFont, ImageDraw
from tuedo import settings, config
import base64
from io import BytesIO
import os, random, hashlib 
from django.db.models import Count, Q
from django.apps import apps
from django.template import Template, Context
from django.template.loader import render_to_string
from functools import wraps

def getCaptchaImageString():

    str = 'ABCDEFGHIJKMNPQRSTUVWQYZabcdefghijklmnpqrstuvwxyz012345789'
    code = ''
    try:
        for i in range(7):
            code += random.choice(str)
        img = Image.new('RGBA', (170, 38), color='#ffffff20')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(os.path.join(settings.STATICFILES_FONTS, 'BPdots.otf'), 40)
        draw.text((0, 0), code, font=font, fill=(0, 0, 0, 255) )
        buf = BytesIO()
        img.save(buf, format="PNG")
        img_str = base64.b64encode(buf.getvalue())
    except:
        img_str = 'Cannot build Captcha'
    return {'img_str': img_str, 'code': code, 'cwd': os.getcwd()}

def getNumberOfActiveCommentsFromBlog(id):
    BlogPost = apps.get_model(app_label='werkstatt', model_name='BlogPost')
    blog_comments = BlogPost.objects.annotate(num_comments=Count('comments', filter=Q(comments__active=True))).filter(id=id)
    if blog_comments.exists():
        comments_number = blog_comments.first().num_comments
        return comments_number

def getNumberTextOfActiveCommentsFromBlog(comments_number):
    index = 2 if comments_number < 0 or comments_number > 1 else comments_number
    return config.TEXT['comments_number_string'][index].format(comments_number)

def checkLanguageSlug(language_slug):
    language_code = config.getLanguageCode(settings.LANGUAGE_CODE)
    if language_slug:
        if language_slug == settings.LANGUAGE_CODE:
             if config.LANGUAGE_DEFAULT_PREFIX is False:
                language_code = None
        else:
            language_code = config.getLanguageCode(language_slug)
    return language_code

def getCurrentLanguage(kwargs):
    language_slug = kwargs.get('language_slug')
    language_code = checkLanguageSlug(language_slug)
    language_short = config.getLanguageShort(language_code)
    return settings.LANGUAGE_CODE if language_short is None else language_short

def updateCommentList(blog):
    comments_not_replies = blog.comments.filter(active=True).filter(reply__isnull=True)
    li = []
    for comment in comments_not_replies:
        li.append(comment)
        if comment.replies:
            replies = comment.replies.filter(active=True).order_by('date_posted')
            for reply in replies:
                li.append(reply)
    return li

def getDataDictFromForm(body_data):
    data = {}
    for k, v in body_data.items():
        data[k] = v
    return data

def getHashString():
        r_string = str(random.getrandbits(256)).encode('utf-8')
        return hashlib.sha256(r_string).hexdigest()[:20]

def filterBlogs(queryset, is_staff = False):
    if is_staff is not True:
        queryset = queryset.exclude(draft=True)
    return queryset

def getFeaturedBlogs(is_staff=False):
    dic = {}
    BlogPost = apps.get_model(app_label='werkstatt', model_name='BlogPost')
    queryset = BlogPost.objects.all()
    queryset = filterBlogs(queryset, is_staff)
    last_blog = queryset.order_by('-date_posted').first()
    dic['last_blog'] = last_blog
    featured_blogs = queryset.filter(featured=True).order_by('featured_position')
    dic['featured_blogs'] = featured_blogs
    return dic

def getSiteCode(str):
    for s in config.SITES:
        if s[1] == str:
            return s[0]

def updateMeta(defaultObject, updateObject):
    items = getDict(updateObject).items()
    for attr, value in items:
        if (value):
            setattr(defaultObject, attr, value)
    return defaultObject

def getDict(updateObject):
    if type(updateObject) is not dict:
        return updateObject.__dict__
    else:
        return updateObject

def getErrorHeader(status):
    template = Template(config.TEXT['error_page_header'])
    context = Context({'status': status})
    return template.render(context)

def getModalCaptchaHtml():
    return render_to_string('werkstatt/modal_captcha.html', { 
        'dataset_error_msg': config.DATASET_ERROR_MSG,
        'captcha_code': config.TEXT['captcha_code'],
        'btn_msg': config.BUTTON['send'],
        'captcha_modal_header': config.MESSAGE['captcha_modal_header'],
        'captcha_modal_message': config.MESSAGE['captcha_modal_message'],
        })