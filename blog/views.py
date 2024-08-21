import re
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from allauth.account.views import LoginView

from blog.forms import CustomPostForm, ProfileForm
from .models import Post, Comment, Category, Tag, Profile
from django.db.models import Count
import markdown2


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse("post_list")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("profile_view")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        # Print or log form errors if needed
        if not form.is_valid():
            print(form.errors)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # 마크다운을 HTML로 변환
        content_html = markdown2.markdown(
            post.content, extras=["fenced-code-blocks", "tables"]
        )

        # HTML에서 태그 링크 생성
        content_with_links = re.sub(
            r"#(\w+)",
            lambda m: f'<a href="{reverse("tag_posts", kwargs={"slug": m.group(1)})}" class="tag-link">#{m.group(1)}</a>',
            content_html,
        )

        context["content"] = content_with_links
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomPostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CustomPostForm
    template_name = "blog/post_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["tags_input"] = ", ".join(tag.name for tag in self.object.tags.all())
        return initial

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")


class PostSearchView(ListView):
    model = Post
    template_name = "blog/post_search.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "blog/comment_form.html"
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "blog/comment_form.html"
    fields = ["content"]

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.annotate(post_count=Count("post"))
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/category_posts.html"
    context_object_name = "posts"
    paginate_by = 6  # 페이지당 포스트 수, PostListView와 일치시킴

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.objects.filter(category=self.category).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class TagListView(ListView):
    model = Tag
    template_name = "blog/tag_list.html"
    context_object_name = "tags"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.annotate(post_count=Count("post"))
        return context


class TagPostListView(ListView):
    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        tag_slug = self.kwargs.get("slug")
        if not tag_slug:
            return Post.objects.none()  # 빈 쿼리셋 반환
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags=self.tag).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = getattr(self, "tag", None)
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = "blog/tag_detail.html"
    context_object_name = "tag"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(tags=self.object)
        return context


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class PostLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse({"likes_count": post.likes.count(), "liked": liked})


class CommentLikeToggleView(LoginRequiredMixin, DetailView):
    model = Comment

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect("post_detail", pk=comment.post.pk)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "blog/reply_form.html"
    fields = ["content"]

    def form_valid(self, form):
        parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        form.instance.author = self.request.user
        form.instance.post = parent_comment.post
        form.instance.parent_comment = parent_comment
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        context["parent_comment"] = parent_comment
        return context

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.post.pk})


import logging
from django.views import View
from django.shortcuts import render
from django.core.cache import cache
from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
from concurrent.futures import ThreadPoolExecutor
import numpy as np

logger = logging.getLogger(__name__)


class CommentSentimentView(View):
    model = None
    tokenizer = None

    @classmethod
    def load_model(cls):
        if cls.model is None or cls.tokenizer is None:
            try:
                model_name = "bert-base-multilingual-cased"
                cls.model = TFBertForSequenceClassification.from_pretrained(model_name)
                cls.tokenizer = BertTokenizer.from_pretrained(model_name)
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                raise

    def get(self, request, *args, **kwargs):
        context = {}
        try:
            self.load_model()
            comments = self.get_queryset()
            context = self.get_context_data(comments)
        except Exception as e:
            logger.error(f"Error in get method: {str(e)}")
            context["error"] = str(e)

        return render(request, "blog/comment_sentiment.html", context)

    def get_queryset(self):
        post_pk = self.kwargs["pk"]
        return Comment.objects.filter(post__pk=post_pk)

    def get_context_data(self, comments):
        context = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            sentiment_futures = {
                executor.submit(self.get_cached_sentiment, comment.content): comment
                for comment in comments
            }
            sentiments = []
            for future in sentiment_futures:
                comment = sentiment_futures[future]
                try:
                    sentiment, confidence = future.result()
                    sentiments.append((comment, sentiment, confidence))
                except Exception as e:
                    logger.error(
                        f"Error predicting sentiment for comment {comment.id}: {str(e)}"
                    )
                    sentiments.append((comment, "Error in prediction", 0.0))
        context["comments"] = sentiments
        return context

    def get_cached_sentiment(self, text):
        cache_key = f"sentiment_{hash(text)}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result
        sentiment, confidence = self.predict_sentiment(text)
        cache.set(cache_key, (sentiment, confidence), timeout=3600)  # Cache for 1 hour
        return sentiment, confidence

    def predict_sentiment(self, text):
        try:
            inputs = self.tokenizer(
                text, padding=True, truncation=True, return_tensors="tf"
            )
            outputs = self.model(inputs)
            logits = outputs.logits
            probabilities = tf.nn.softmax(logits, axis=1).numpy()[0]
            predicted_class = np.argmax(probabilities)
            confidence = probabilities[predicted_class]

            sentiment_labels = {
                0: "Very Negative",
                1: "Negative",
                2: "Neutral",
                3: "Positive",
                4: "Very Positive",
            }

            # 신뢰도 기반 감정 분류 세분화
            if confidence < 0.4:
                sentiment = "불확실하다"
            elif confidence < 0.6:
                sentiment = "중립"
            else:
                sentiment = sentiment_labels[predicted_class]

            # 결과 해석 개선
            interpretation = self.interpret_sentiment(sentiment, confidence, text)

            return f"{sentiment} - {interpretation}", confidence
        except Exception as e:
            logger.error(f"Error in sentiment prediction: {str(e)}")
            return "Error in prediction", 0.0

    def interpret_sentiment(self, sentiment, confidence, text):
        if sentiment == "Uncertain":
            return "The sentiment is unclear. The model is not confident in its prediction."
        elif sentiment == "Neutral":
            return "The text appears to be neutral or balanced in sentiment."
        else:
            intensity = "strongly" if confidence > 0.8 else "moderately"
            return f"The text appears to be {intensity} {sentiment.lower()}."

    @staticmethod
    def detect_language(text):
        # 간단한 언어 감지 (한국어 또는 영어)
        if any("\uac00" <= char <= "\ud7a3" for char in text):
            return "ko"
        return "en"
