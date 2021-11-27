from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView
from restaurant.forms import MenuForm, CategoryForm
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from restaurant.models import MenuModel, Restaurant, CategoryModel


class MenuListView(ListView):
    template_name = 'user/index.html'
    model = MenuModel

    def get_queryset(self, **kwargs):
        link = self.kwargs.get('name')
        qs = Restaurant.objects.filter(link=link)
        menu = MenuModel.objects.order_by('-pk')
        if qs:
            menu = menu.filter(restaurant__link=link)
        else:
            raise Http404
        return menu


class MTemplateView(TemplateView):
    template_name = 'index.html'


class MenuCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/menu.html'
    form_class = MenuForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('menu:create'))

    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
        context['category'] = self.request.user.category.order_by('-pk')
        context['restaurant'] = self.request.user.restaurant.order_by('-pk')
        return context


class AdminMenuListView(ListView):
    template_name = 'admin/menulist.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = MenuModel.objects.all()
        if q:
            return qs.filter(category_id=q).order_by('-pk')
        else:
            return qs.filter(user=self.request.user).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.user.category.order_by('-pk')
        context['restaurant'] = self.request.user.restaurant.order_by('-pk')
        return context


def ProductDelete(request):
    cat = request.POST.getlist('option')
    for i in cat:
        MenuModel.objects.get(id=i).delete()
    return HttpResponseRedirect(reverse('menu:list'))


class ProductUpdateView(UpdateView):
    template_name = 'admin/menulist.html'
    form_class = MenuForm
    model = MenuModel

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(self.request.GET.get('next'))


class CategoryListView(ListView):
    template_name = 'admin/category.html'
    paginate_by = 10

    def get_queryset(self):
        return CategoryModel.objects.order_by('-pk')


def CategoryDelete(request):
    cat = request.POST.getlist('option')
    for i in cat:
        CategoryModel.objects.get(id=i).delete()
    return HttpResponseRedirect(reverse('menu:category'))


class CategoryCreateView(CreateView):
    template_name = 'admin/category.html'
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('menu:category'))


class CategoryUpdateView(UpdateView):
    template_name = 'admin/category.html'
    form_class = CategoryForm
    model = CategoryModel

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('menu:category'))
