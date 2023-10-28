from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Shoe(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='media/shoes/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    additional_images = models.ManyToManyField('Image', blank=True, related_name='shoes')  # Définissez un nom de requête inversée

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def get_additional_images(self):
        # Récupérez les images supplémentaires associées à ce Shoe
        return self.additional_images.all()

    def get_main_image_url(self):
        # Récupérez l'URL de l'image principale
        if self.image:
            return self.image.url
        else:
            # Remplacez ceci par l'URL par défaut de l'image principale si nécessaire
            return 'media/shoes/sneakers/Nike Air Max 95 x Future Movement/air-max-95-future-movement-shoes-7Wqr2R.png'

class Image(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='images')  # Définissez un nom de requête inversée
    image = models.ImageField(upload_to='media/shoes/', blank=True, null=True)



