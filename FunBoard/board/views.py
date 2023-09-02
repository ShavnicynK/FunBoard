from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Advertisement, Category, Reaction, News
from .forms import CategoryForm, AdvertisementForm, ReactionForm, NewsForm
from .filters import ReactionFilter


class AdvertisementList(PermissionRequiredMixin, ListView):
    permission_required = 'board.view_advertisement'
    model = Advertisement
    ordering = '-date'
    template_name = 'advertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 10


class MyAdvertisementList(PermissionRequiredMixin, ListView):
    permission_required = 'board.view_advertisement'
    model = Advertisement
    ordering = '-date'
    template_name = 'myadvertisements.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(author=self.request.user)
        return queryset


class AdvertisementUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'board.change_advertisement'
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'advertisement_edit.html'
    success_url = reverse_lazy('myadvertisement_list')


class AdvertisementCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'board.add_advertisement'
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'advertisement_edit.html'
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryList(PermissionRequiredMixin, ListView):
    permission_required = 'board.view_category'
    model = Category
    ordering = 'name'
    template_name = 'categorys.html'
    context_object_name = 'categorys'
    paginate_by = 20


class CategoryBlog(PermissionRequiredMixin, DetailView):
    permission_required = 'board.view_category'
    model = Category
    template_name = 'category_blog.html'
    context_object_name = 'category'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisements'] = Advertisement.objects.filter(category=kwargs['object'])

        return context


class CategoryCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'board.add_category'
    model = Category
    form_class = CategoryForm
    template_name = 'category_edit.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'board.change_category'
    model = Category
    form_class = CategoryForm
    template_name = 'category_edit.html'
    success_url = reverse_lazy('category_list')


class ReactionCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'board.add_reaction'
    model = Reaction
    form_class = ReactionForm
    template_name = 'reaction_edit.html'
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form, **kwargs):
        form.instance.author = self.request.user
        form.instance.advertisement_id = self.kwargs.get('pk')
        messages.success(self.request, ("Ваша рекция успешно добавлена"))
        return super().form_valid(form)


class ReactionList(PermissionRequiredMixin, ListView):
    permission_required = 'board.view_reaction'
    model = Reaction
    template_name = 'reaction_blog.html'
    context_object_name = 'reactions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(advertisement__author=self.request.user)
        self.filterset = ReactionFilter(self.request.GET, queryset, request=self.request.user.pk)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['filter_on'] = True if len(self.filterset.data) else False
        return context


def set_reaction_accept(request, pk):
    reaction = Reaction.objects.get(id=pk)
    reaction.status = 'A'
    reaction.save()

    return redirect('/reactions/')


def set_reaction_refused(request, pk):
    reaction = Reaction.objects.get(id=pk)
    reaction.status = 'R'
    reaction.save()

    return redirect('/reactions/')


def set_reaction_delete(request, pk):
    Reaction.objects.get(id=pk).delete()

    return redirect('/reactions/')


class NewsList(PermissionRequiredMixin, ListView):
    permission_required = 'board.view_news'
    model = News
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 20


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'board.add_news'
    model = News
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')
