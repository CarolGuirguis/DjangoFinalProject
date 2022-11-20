from django.db import models
from pickle import TRUE
from django.shortcuts import  reverse, get_object_or_404
from django.contrib.auth import get_user_model

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=100,null=TRUE)
    

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=100)
    users=models.ManyToManyField(get_user_model())

    @classmethod
    def get_all_objects(cls):
        return cls.objects.all()

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)

    def __str__(self):
        return self.name

    @classmethod
    def delete_category(cls, id):
        c= cls.get_object(id)
        c.delete()
        return True


class Tag(models.Model):
    tagword = models.CharField(max_length=50)

    def __str__(self):
        return self.tagword

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)
    
    @classmethod
    def get_all_objects(cls):
        return cls.objects.all()

class Posts(models.Model):
    title = models.CharField(max_length=100)
    image=models.ImageField(upload_to="main/images/", null=True, blank=True)
    content=models.CharField(max_length=1000,null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    publish_date=models.DateField(null=True)
    likes=models.PositiveIntegerField(null=True,default=0)
    dislikes=models.PositiveIntegerField(null=True,default=0)
    tags=models.ManyToManyField(Tag)

    class Meta:
        ordering = ["-publish_date"]

    
    @classmethod
    def delete_post(cls, id):
        p= cls.get_object(id)
        p.delete()
        return True
        
    @classmethod
    def get_all_objects(cls):
        return cls.objects.all()

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)
    
    def getimageurl(self):
        return f"/media/{self.image}"

    @classmethod
    def filterCategory(cls,cid):
        return cls.objects.filter(category=cid)

    @classmethod
    def filterTitle(cls,title):
        return cls.objects.filter(title=title)
    
    @classmethod
    def filterTag(cls,tag):
         all_tags = Tag.objects.filter(tagword=tag)
         return cls.objects.filter(tags__in = all_tags)

    def __str__(self):
        return self.title


class ForbiddenWords(models.Model):
    word = models.CharField(max_length=100)
    
    @classmethod
    def delete_word(cls, id):
        w= cls.get_object(id)
        w.delete()
        return True
        
    @classmethod
    def get_all_objects(cls):
        return cls.objects.all()

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)
    @classmethod
    def delete_forbiddenword(cls, id):
        fw= cls.get_object(id)
        fw.delete()
        return True
        
    def __str__(self):
       return self.word


class Comment(models.Model):
    content = models.CharField(max_length=500)
    date=models.DateTimeField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

    @classmethod
    def filterPost(cls,pid):
        return cls.objects.filter(post=pid)

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)

class Reply(models.Model):
    content = models.CharField(max_length=500)
    date=models.DateTimeField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)

    @classmethod
    def filterComment(cls,cid):
        return cls.objects.filter(comment=cid)
    @classmethod
    def filterPost(cls,pid):
        return cls.objects.filter(post=pid)

    @classmethod
    def get_object(cls, id):
        return get_object_or_404(cls, pk=id)
