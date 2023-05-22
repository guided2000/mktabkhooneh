from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import post


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = [
                "image", "author", "title", "content", "tags", "category", "status", "published_date"
            ]
        elif request.user.is_author:
            self.fields = [
                "image", "title", "content", "tags", "category", "published_date"
            ]
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FormValidsMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = False
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(post, pk=pk)
        if request.user.is_authenticated:
            if article.author == request.user and article.status == True or\
                    request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("login")


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
