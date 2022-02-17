from django.db import models


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, verbose_name='Title')
    body = models.TextField(verbose_name='Text')
    owner = models.ForeignKey('auth.User', related_name='posts',  on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return f'/{self.id}'

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created', 'owner']
        verbose_name = 'Post'
        verbose_name_plural = "Posts"


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Owner')
    body = models.TextField(blank=False, verbose_name='Text')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.owner, self.post)

    class Meta:
        ordering = ['created']
        verbose_name = 'Comment'
        verbose_name_plural = "Comments"


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE)
    posts = models.ManyToManyField('Post',  related_name='categories', blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'

