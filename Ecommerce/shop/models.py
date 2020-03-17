from django.db import models


class Product(models.Model):
    product_id = models.AutoField(primary_key = True)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=400)
    product_name = models.CharField(max_length=100)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default='')

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000, default=' ')
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50, default="some_example@gmail.com")
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=30)
    amount = models.IntegerField(default='')
    state = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.name+" order_id = ("+str(self.order_id)+")"


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
























