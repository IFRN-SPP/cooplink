from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string


class PaginateMixin:
    """
    Provides pagination capabilities to a list of objects for class-based views.
    """
    paginate_by = None
    partial_list = None
    partial_pagination = 'partials/pagination.html'

    def paginate(self, request, paginate_by, object_list):
        """
        Paginates the given object list based on the request's page number.
        """
        paginator = Paginator(object_list, paginate_by)
        page_num = request.GET.get('page')
        
        try:
            object_list = paginator.get_page(page_num)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        return object_list


class ContextMixin:
    """
    Provides a basic context mixin that can be extended to include additional context for templates.
    """
    context = None
    def get_context(self):
        """
        Returns the context dictionary to be used in rendering templates.
        """
        context = {}
        return context


class AjaxResponseMixin(ContextMixin, PaginateMixin):
    """
    Mixin to handle AJAX responses, providing methods for returning JSON responses.
    """
    object_list = 'object_list'
    model = None
    template_name = None
    message = None
    message_class = None

    def ajax_response(self, form=None, object_list=None, context=None, template_name=None, paginate_by=None, success_url=None):
        """
        Constructs a JSON response for an AJAX request with optional form validation, object listing, and pagination.
        """
        data = {}
        if form:
            data['html_form'] = render_to_string(template_name, {'form': form}, request=self.request)
            data['form_is_valid'] = form.is_valid()
            if success_url:
                data['success_url'] = success_url
            if self.message:
                data['message'] = self.message
                data['message_class'] =  self.message_class

        if object_list:
            if paginate_by:
                object_list = self.paginate(self.request, paginate_by, object_list)
                context['page'] = context[f'{self.object_list}'] = object_list
                data['html_pagination'] = render_to_string(self.partial_pagination, context)
            
            context[f'{self.object_list}'] = object_list
            data['html_list'] = render_to_string(self.partial_list, context)
        return JsonResponse(data)
    
    def get_queryset(self):
        """
        Returns the queryset of the model's objects to be listed.
        """
        queryset = self.model.objects.all()
        return queryset
    

class FormResponseMixin(AjaxResponseMixin):
    """
    Mixin to handle form responses via AJAX, including validation and rendering.
    """
    form = None
    success_url = None

    def form_valid(self, form):
        """
        Processes a valid form, returns an AJAX response.
        """
        return self.ajax_response(form=form, template_name=self.template_name, success_url=self.success_url)
    
    def render_form(self, form):
        """
        Renders the specified form as part of the AJAX response.
        """
        return self.ajax_response(form=form, template_name=self.template_name)


class DeleteReponseMixin(AjaxResponseMixin):
    """
    Mixin to handle AJAX responses for delete operations.
    """
    success_url = None

    def render_form(self, instance):
        """
        Renders a form for confirming a delete operation on an instance.
        """
        data = {'form_is_valid': False}
        data['html_form'] = render_to_string(self.template_name, {'object': instance}, request=self.request)
        return JsonResponse(data)
    
    def form_valid(self):
        """
        Processes a successful delete operation, returning an AJAX response.
        """
        data = {'form_is_valid': True}
        data['success_url'] = self.success_url
        if self.message:
            data['message'] = self.message
            data['message_class'] =  self.message_class

        return JsonResponse(data)
