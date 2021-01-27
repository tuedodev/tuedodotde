from django.shortcuts import render, redirect
from django.urls import reverse
from werkstatt.models import BlogPost, Sitecontent
from werkstatt.forms import CommentForm, CaptchaForm, ContactForm, SubscriptionForm
from django.utils import translation
from django.db.models import Q
from tuedo import settings, config
from django.http import JsonResponse, HttpResponse, Http404
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.views import View
from django.views.decorators.http import require_GET
from django.core.paginator import InvalidPage, Paginator
import json
from .utils import (getCaptchaImageString,
                    getNumberOfActiveCommentsFromBlog,
                    getNumberTextOfActiveCommentsFromBlog,
                    checkLanguageSlug,
                    updateCommentList,
                    getDataDictFromForm,
                    getFeaturedBlogs,
                    filterBlogs,
                    getSiteCode,
                    updateMeta,
                    getDict,
                    getErrorHeader,
                    getModalCaptchaHtml,
                    )
from django.template import loader
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.html import escape
from django.utils.http import urlencode
from django.core.exceptions import PermissionDenied
from werkstatt.context_processors import getDefaultMetaTags
from meta.views import Meta

def index(request):
    if request.method == 'GET':
        context = getFeaturedBlogs(request.user.is_staff)
        context['read_on'] = config.TEXT['read_on']
        return render(request, 'werkstatt/index.html', context)

def impressum(request):
    return render(request, 'werkstatt/impressum.html', {})

class ReferencesView(ListView):
    model = Sitecontent
    template_name = 'werkstatt/referenzen.html'
    context_object_name = 'references'

    def get_queryset(self):
        sitecode = getSiteCode('references')
        queryset = Sitecontent.objects.all().filter(draft=False).filter(site=sitecode)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = updateMeta(Meta(), config.METATAGS['references'])
        context['header'] = config.TEMPLATE_HEADERS['references']
        return context

class DatenschutzView(ListView):
    model = Sitecontent
    template_name = 'werkstatt/datenschutz.html'
    context_object_name = 'datenschutz'

    def get_queryset(self):
        sitecode = getSiteCode('datenschutz')
        queryset = Sitecontent.objects.all().filter(draft=False).filter(site=sitecode)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = updateMeta(Meta(), config.METATAGS['privacy'])
        context['header'] = config.TEMPLATE_HEADERS['privacy']
        return context

class AboutView(ListView):
    model = Sitecontent
    template_name = 'werkstatt/about.html'
    context_object_name = 'milestones'

    def get_queryset(self):
        sitecode = getSiteCode('about')
        queryset = Sitecontent.objects.all().filter(draft=False).filter(site=sitecode)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = config.TEMPLATE_HEADERS['about']
        context['meta'] = updateMeta(Meta(), config.METATAGS['about'])
        return context

class ImpressumView(ListView):
    model = Sitecontent
    template_name = 'werkstatt/impressum.html'
    context_object_name = 'milestones'

    def get_queryset(self):
        sitecode = getSiteCode('imprint')
        queryset = Sitecontent.objects.all().filter(draft=False).filter(site=sitecode)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = updateMeta(Meta(), config.METATAGS['imprint'])
        context['header'] = config.TEMPLATE_HEADERS['imprint']
        return context

class KontaktView(View):
    form_class = ContactForm
    template_name = 'werkstatt/kontakt.html'

    def get(self, request, *args, **kwargs):
        contact_form = self.form_class()
        return render(request, self.template_name, {
            'contact_form': contact_form,
            'site_path': request.path,
            'header': config.TEMPLATE_HEADERS['contact'],
            'btn_text': config.BUTTON['send'],
            'meta': updateMeta(Meta(), config.METATAGS['contact']),
        })


class ListViewCustomizedPagination(ListView):

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(
            page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                page_number = 1
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page = paginator.page(paginator.num_pages)
        return (paginator, page, page.object_list, page.has_other_pages())


class WerkstattView(ListViewCustomizedPagination):
    template_name = 'werkstatt/werkstatt.html'
    context_object_name = 'blogs'
    paginate_by = config.BLOGS_PER_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['read_on'] = config.TEXT['read_on']
        context['searchstring'] = ''
        context['meta'] = updateMeta(Meta(), config.METATAGS['werkstatt'])
        return context

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        queryset = filterBlogs(queryset, self.request.user.is_staff)
        return queryset.order_by('date_posted')


class SearchView(ListViewCustomizedPagination):
    template_name = 'werkstatt/search.html'
    context_object_name = 'blogs'
    paginate_by = config.BLOGS_PER_PAGE
    ordering = ['date_posted']

    def get_queryset(self):
        query = self.request.GET.get('s')
        category = self.request.GET.get('category')
        if query:
            queryset = BlogPost.objects.all()
            queryset = filterBlogs(queryset, self.request.user.is_staff)
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(content__icontains=query) |
                Q(categories__title__iexact=query)
            ).distinct()
        elif category:
            queryset = BlogPost.objects.filter(
                categories__title__iexact=category).distinct()
            queryset = filterBlogs(queryset, self.request.user.is_staff)
        else:
            queryset = BlogPost.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('s')
        category = self.request.GET.get('category')
        context['searchstring'] = None
        searching_for = ''
        if query:
            searching_for = f"{config.TEXT['searching_for']} '{query}'"
            context['searchstring'] = f"&{ escape(urlencode({'s': query})) }"
        elif category:
            searching_for = f"{config.TEXT['searching_category']} '{category}'"
            context['searchstring'] = f"&{ escape(urlencode({'category': category})) }"
        context['searching_for'] = searching_for
        context['number_search_result'] = self.get_queryset().count()
        context['searching'] = config.TEXT['searching']
        context['searching_hits'] = config.TEXT['searching_hits']
        context['searching_no_hits'] = config.TEXT['searching_no_hits']
        context['read_on'] = config.TEXT['read_on']
        return context

def blogpost(request, *args, **kwargs):

    language_slug = kwargs.get('language_slug')
    blog_slug = kwargs.get('blog_slug')
    language_code = checkLanguageSlug(language_slug)

    queryset = BlogPost.objects.filter(
        language=language_code).filter(slug=blog_slug)

    if queryset.exists():
        blog = queryset.first()
        blog_id = 'blog-' + str(blog.id)
        if blog.draft is True and request.user.is_staff is False:
            raise PermissionDenied
        context = {}
        context['blog_path'] = request.path
        context['blog_previous_hint'] = config.HINT['previous-blog']
        context['blog_next_hint'] = config.HINT['next-blog']
        context['blog'] = blog
        context['btn_text'] = config.BUTTON['send']
        try:
            context['blog_previous'] = blog.get_previous_by_date_posted(draft=False)
        except:
            context['blog_previous'] = None
        try:
            context['blog_next'] = blog.get_next_by_date_posted(draft=False)
        except:
            context['blog_next'] = None

        # Overwrite Meta
        # Order: 1. Default Meta 2. meta() from model 3. Database
        meta = getDefaultMetaTags(request)['meta']
        meta_as_meta = getDict(blog.as_meta())
        try:
            meta_database = json.loads(blog.meta)
        except:
            meta_database = {}
        meta_merged = {**meta_as_meta, **meta_database} 
        context['meta'] =  updateMeta(meta, meta_merged)
        
        all_comments = blog.comments.all()
        new_comment = None
        new_comment_html = None
        if request.method == 'GET':
            new_comment_id = request.session.get(blog_id)
            if new_comment_id:
                pending_comment = all_comments.filter(
                    id=new_comment_id).first()
                if pending_comment:
                    if pending_comment.active == True:
                        del request.session[blog_id]
                    else:
                        new_comment = all_comments.filter(
                            id=new_comment_id).first()
                        comment_header = render_to_string('werkstatt/comment_header.html', {
                            'date_posted': new_comment.date_posted,
                            'comment_header':  new_comment.comment_header,                          
                            'name': new_comment.name,
                            })
                        new_comment_html = render_to_string('werkstatt/new_comment.html', {
                            'name': new_comment.name,
                            'comment_header': comment_header,
                            'comment_body': new_comment.comment_body,
                            'comment_notification': config.TEXT['comment_notification'],
                        })
                else:
                    del request.session[blog_id]

        comment_form = CommentForm()
        comments = updateCommentList(blog)
        context['comments'] = comments
        context['new_comment_html'] = new_comment_html
        context['comment_form'] = comment_form
        comments_number = getNumberOfActiveCommentsFromBlog(blog.id)
        context['comments_number'] = comments_number
        context['comments_number_text'] = getNumberTextOfActiveCommentsFromBlog(
            comments_number)
        context['comments_empty_message'] = config.HINT['comments_empty_message']
        context['comments_add_comment'] = config.HINT['comments_add_comment']
        return render(request, 'werkstatt/blogpost.html', context)
    else:
        raise Http404


# new app API?
def get_captcha_image(request):
    if request.method == 'POST':
        s = getCaptchaImageString()
        captcha_code = s.get('code')
        request.session['captcha_code'] = captcha_code
        bin_decoded = json.dumps(s.get('img_str').decode("utf-8"))
        res = {'img': bin_decoded, 'code': captcha_code, }
        return JsonResponse(res, safe=True)


def check_captcha(request):
    if request.method == 'POST':
        try:
            captchacode_input = request.POST['captchacode_input']
            if captchacode_input == request.session.get('captcha_code'):
                msg = 'Your captcha input was successful.'
            else:
                msg = 'Your captcha input was wrong.'
        except KeyError:
            msg = 'Error Message: An Error occured.'

        request.session['msg'] = msg
    return redirect('index')


def validate_form(request):
    if request.method == 'POST':
        context = {}
        form = None
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        data_from_form = getDataDictFromForm(body_data)
        if data_from_form.get('action') == 'validate':
            formclass = data_from_form.get('form')
            if formclass == 'comment':
                form = CommentForm(data_from_form)
                context['html'] = getModalCaptchaHtml()
            elif formclass == 'captcha':
                form = CaptchaForm(data_from_form)
                form.captcha_code = request.session.get('captcha_code')
                context['html'] = ''
            elif formclass == 'contact':
                form = ContactForm(data_from_form)
                context['html'] = getModalCaptchaHtml()
            elif formclass == 'subscribe':
                form = SubscriptionForm(data_from_form)
                context['html'] = getModalCaptchaHtml()
            if form and form.is_valid():
                context['errors'] = ''
            else:
                context['errors'] = {f: e.get_json_data()
                                     for f, e in form.errors.items()}
        return JsonResponse(context, safe=True)


def process_form(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        data_from_form = getDataDictFromForm(body_data)
        action = data_from_form.get('action')
        form_captcha = CaptchaForm(data_from_form)        
        form_captcha.captcha_code = request.session.get('captcha_code')
        context = {}

        if action == 'process_comment':
            form = CommentForm(data_from_form)
            site_path = body_data.get('site_path')
            if site_path:
                li = site_path.strip('/').split('/')
                blog_slug = li.pop()
                if len(li):
                    language_slug = li.pop()
                else:
                    language_slug = None
                language_code = checkLanguageSlug(language_slug)
                queryset = BlogPost.objects.filter(
                    language=language_code).filter(slug=blog_slug)
                if queryset.exists():
                    blog = queryset.first()
                    blog_id = 'blog-' + str(blog.id)
                    context['redirect_url'] = blog.absolute_url
                    if form.is_valid and form_captcha.is_valid:
                        new_comment = form.save(commit=False)
                        new_comment.blogpost = blog
                        new_comment.save()
                        request.session[blog_id] = new_comment.id
                        context['html'] = render_to_string('werkstatt/new_comment.html', {
                            'name': new_comment.name,
                            'date_posted': new_comment.date_posted,
                            'comment_body': new_comment.comment_body,
                        })
                        context['message_html'] = render_to_string('werkstatt/modal_message.html', {
                                                                   'messages': config.MESSAGE['comment_success'], 'button': config.BUTTON['okay']})
                    else:
                        context['error_html'] = render_to_string('werkstatt/modal_message.html', {
                                                                 'messages': config.MESSAGE['error_transfer_data'], 'button': config.BUTTON['okay']})
            else:
                context['redirect_url'] = reverse('index')
                context['error_html'] = render_to_string('werkstatt/modal_message.html', {
                                                         'messages': config.MESSAGE['error_unknown_homepage'], 'button': config.BUTTON['home']})

        elif action == 'process_contact':
            form = ContactForm(data_from_form)
            context['redirect_url'] = reverse('index')
            if form.is_valid and form_captcha.is_valid:
                form.save()
                context['message_html'] = render_to_string('werkstatt/modal_message.html', {
                                                           'messages': config.MESSAGE['contact_success'], 'button': config.BUTTON['home'], 
                                                           'modal_message_header': config.MESSAGE['modal_message_header']})
            else:
                context['error_html'] = render_to_string('werkstatt/modal_message.html', {
                                                         'messages': config.MESSAGE['error_unknown_homepage'], 'button': config.BUTTON['home'],
                                                         'modal_message_header': config.MESSAGE['modal_message_header']})
        elif action == 'process_subscribe':
            form = SubscriptionForm(data_from_form)
            site_path = body_data.get('site_path')
            if site_path is None:
                site_path = reverse('index')
            context['redirect_url'] = site_path
            if form.is_valid and form_captcha.is_valid:
                form.save()
                context['message_html'] = render_to_string('werkstatt/modal_message.html', {
                                                           'messages': config.MESSAGE['subscription_success'], 'button': config.BUTTON['okay'],
                                                           'modal_message_header': config.MESSAGE['modal_message_header']})
            else:
                context['error_html'] = render_to_string('werkstatt/modal_message.html', {
                                                         'messages': config.MESSAGE['error_unknown_homepage'], 'button': config.BUTTON['home'],
                                                         'modal_message_header': config.MESSAGE['modal_message_header']})
    return JsonResponse(context, safe=True)

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def custom_page_not_found_view(request, exception):
    status = 404
    return render(request, 'werkstatt/error.html', {'error_message': config.ERROR_PAGES_MSG[str(status)], 'index_url': reverse('index'), 'button_text': config.BUTTON['going_home'], 'error_page_header': getErrorHeader(404)}, status=404)


def custom_error_view(request):
    status = 500
    return render(request, 'werkstatt/error.html', {'error_message': config.ERROR_PAGES_MSG[str(status)], 'index_url': reverse('index'), 'button_text': config.BUTTON['going_home'], 'error_page_header': getErrorHeader(500)}, status=500)


def custom_permission_denied_view(request, exception):
    status = 403
    return render(request, 'werkstatt/error.html', {'error_message': config.ERROR_PAGES_MSG[str(status)], 'index_url': reverse('index'), 'button_text': config.BUTTON['going_home'], 'error_page_header': getErrorHeader(403)}, status=403)


def custom_bad_request_view(request, exception):
    status = 400
    return render(request, 'werkstatt/error.html', {'error_message': config.ERROR_PAGES_MSG[str(status)], 'index_url': reverse('index'),  'button_text': config.BUTTON['going_home'], 'error_page_header': getErrorHeader(400)}, status=400)
