from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequireMixin(object):

    @method_decorator(login_required)
    def dispatch(self,request,*args, **kwargs):
        return super(LoginRequireMixin, self).dispatch(request, *args,**kwargs)


class StaffRequireMixin(object):

    @method_decorator(staff_member_required)
    def dispatch(self,request,*args, **kwargs):
        return super(StaffRequireMixin, self).dispatch(request,*args,**kwargs)


class MultiSlugMixin(object):
    model = None

    def get_object(self,*args, **kwargs):
        slug = self.kwargs.get("slug")
        modelClass = self.model
        if slug is not None:
            try:
                obj = get_object_or_404(modelClass, slug=slug)
            except modelClass.MultipleObjectsReturned:
                obj = modelClass.objects.filter(slug=slug)
        else:
            obj = super(MultiSlugMixin, self).get_context_data(*args,**kwargs)
        # print(obj)
        return obj