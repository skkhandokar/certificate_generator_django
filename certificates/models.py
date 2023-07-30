


from django.db import models

class Certificate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='certificate/',blank=True,null=True)



