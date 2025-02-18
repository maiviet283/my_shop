from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Danh Mục"
        verbose_name_plural = "Danh Mục Sản Phẩm"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    image = models.ImageField(upload_to='products/image/%Y/%m/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0) # Lưu số lượng sản phẩm có trong kho.
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    color = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products') # loại
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sản Phẩm"
        verbose_name_plural = "Danh Sách Sản Phẩm"
    
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/%Y/%m/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Hình Ảnh Sản Phẩm"
        verbose_name_plural = "Hình Ảnh Sản Phẩm"

    def save(self, *args, **kwargs):
        if not self.alt_text and self.product:
            self.alt_text = self.product.name  # Gán tên sản phẩm làm mô tả ảnh mặc định
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name if self.product else 'Deleted Product'}"

