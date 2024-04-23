from django.shortcuts import get_object_or_404, render
from django.views import View
from .mixins import AjaxResponseMixin, FormResponseMixin, DeleteReponseMixin

class AjaxListView(View, AjaxResponseMixin):
    """
    Base view for returning JSON response for object listing.
    """
    def get(self, request, *args, **kwargs):
        """
        GET method to handle object listing request.
        """
        object_list = self.get_queryset()
        context = self.get_context()
        context[f'{self.object_list}'] = object_list

        if request.headers.get('header') == 'ajax':
            return self.ajax_response(object_list=object_list, context=context, paginate_by=self.paginate_by)

        else:
            if self.paginate_by:
                object_list = self.paginate(self.request, self.paginate_by, object_list)
                context['page'] = context[f'{self.object_list}'] = object_list

            return render(request, self.template_name, context)
        
class AjaxFormView(View, FormResponseMixin):
    """
    Base view for form processing and returning JSON responses.
    """
    form_class = None

    def get(self, request, *args, **kwargs):
        """
        GET method to handle form rendering request.
        """
        form = self.form_class()
        return self.render_form(form)

    def post(self, request, *args, **kwargs):
        """
        POST method to handle form submission.
        """
        form = self.form_class(request.POST)
        return self.form_valid(form)
    
    def form_valid(self, form):
        """
        Save form parameters and return the form validation.
        """
        form.save()
        return super().form_valid(form)

class AjaxCreateView(AjaxFormView):
    """
    View to create a new object using AJAX.
    """
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AjaxUpdateView(AjaxFormView):
    """
    View to update an existing object using AJAX.
    """
    def get(self, request, pk, *args, **kwargs):
        model = self.form_class._meta.model
        instance = get_object_or_404(model, pk=pk)
        form = self.form_class(instance=instance)
        return self.render_form(form)

    def post(self, request, pk, *args, **kwargs):
        model = self.form_class._meta.model
        instance = get_object_or_404(model, pk=pk)
        form = self.form_class(request.POST, instance=instance)
        return self.form_valid(form)

class AjaxDeleteView(View, DeleteReponseMixin):
    """
    View to delete an existing object using AJAX.
    """
    def get(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=pk)
        return self.render_form(instance)

    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=pk)
        instance.delete()
        return self.form_valid()
