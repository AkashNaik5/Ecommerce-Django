from django.db import models


class Blogpost(models.Model):
    post_id = models.AutoField(primary_key= True)
    blog_title = models.CharField(max_length=50, default='')
    blog_desc = models.CharField(max_length=300, default='')
    heading0 = models.CharField(max_length=50, default="")
    content0 = models.CharField(max_length=5000, default='')
    heading1 = models.CharField(max_length=50, default="")
    content1 = models.CharField(max_length=5000, default='')
    heading2 = models.CharField(max_length=50, default="")
    content2 = models.CharField(max_length=5000, default='')
    timestamp = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="blog/images", default='')

    def __str__(self):
        return self.blog_title

