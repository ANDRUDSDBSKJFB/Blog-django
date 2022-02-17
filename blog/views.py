from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions
from . import serializers
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AuthUserForm, RegUserForm, PostForm, CommentForm
from .models import Post, Comment, Category
from .serializers import PostSerializer, UserSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from rest_framework.views import APIView
from django.views.generic.edit import FormMixin
from .permissions import IsOwnerOrReadOnly


class PostinList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/index.html'

    def get(self, request):
        queryset = Post.objects.all()
        return Response({'profile': queryset})


class PostDetailView(DetailView):
    model = Post
    template_name = 'main/changer.html'
    context_object_name = 'get_article'


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class PostCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = Post
    template_name = 'main/changer.html'
    form_class = PostForm
    success_url = reverse_lazy('change')
    success_msg = 'Запись создана'
    raise_exception = True

    def get_context_data(self, **kwargs):
        kwargs['profile'] = Post.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostinDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Post
    template_name = 'main/post_detail.html'
    context_object_name = 'profile'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'

    def get_context_data(self, **kwargs):
        kwargs['comments'] = Comment.objects.all().filter(post=self.object.id)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.get_object().id})

    def post(self, request, pk, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Post
    template_name = 'main/post_update.html'
    form_class = PostForm
    success_url = reverse_lazy('change')
    success_msg = 'Запись успешно обновлена'
    raise_exception = True

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].owner:
            return self.handle_no_permission()
        return kwargs


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'main/post_delete.html'
    success_url = reverse_lazy('change')
    success_msg = 'Запись удалена'
    raise_exception = True

    def get_context_data(self, **kwargs):
        kwargs['comments'] = Comment.objects.all()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != self.object.owner:
            return self.handle_no_permission()
        return kwargs


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'main/post_delete.html'
    success_url = '/'
    success_msg = 'Запись удалена'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user == self.object.owner:
            self.object.delete()
            return self.handle_no_permission()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != self.object.owner:
            return self.handle_no_permission()
        return kwargs


class ProjectUserLoginView(LoginView):
    template_name = 'main/login.html'
    form_class = AuthUserForm
    success_url = '/login'


class ProjectUserRegistrationView(CreateView):
    template_name = 'main/register.html'
    form_class = RegUserForm
    success_url = '/'
    success_msg = "Record created"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class ProjectUserLogOutView(LogoutView):
    next_page = '/'


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
