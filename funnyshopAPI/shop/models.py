from django.db import models
from django.urls import reverse


COLOR_CHOICES = (
    (1, 'primary'),
    (2, 'secondary'),
    (3, 'success'),
    (4, 'danger'),
    (5, 'warning'),
    (6, 'info'),
    (7, 'light'),
    (8, 'dark'),
)



class Category(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    color = models.PositiveIntegerField(choices= COLOR_CHOICES,
                                blank=True,
                                null=True)

    image = models.ImageField(upload_to='categories/%Y/%m/%d',
                                blank=True)

    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name


    def get_color_name(self):
        return COLOR_CHOICES[self.color - 1][1]
    
    def get_image_url(self):
        return self.image.url
        # return self.image.path


    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                        args=[self.slug])



class Product(models.Model):

    category = models.ForeignKey(Category,
                                    related_name='products',
                                    on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200)

    slug = models.SlugField(max_length=200)

    hb = models.PositiveIntegerField(blank=False,
                                        default=0,
                                        null=False)

    attack = models.PositiveIntegerField(blank=False,
                                        default=0,
                                        null=False)

    defense  = models.PositiveIntegerField(blank=False,
                                        default=0,
                                        null=False)

    speed  = models.PositiveIntegerField(blank=False,
                                        default=0,
                                        null=False)

    image = models.ImageField(upload_to='products/%Y/%m/%d',
                                blank=True)
    
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                        args=[self.id, self.slug])
    
    def get_category_name(self):
        return self.category.name

    def get_category_image(self):
        return self.category.get_image_url()
