from django.db import models


class Event(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)


    def __str__(self):
        return self.title


class Bouquet(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)
    price = models.FloatField(verbose_name='Цена')
    events = models.ManyToManyField(Event, verbose_name='События',
                                    related_name='events')
    photo = models.ImageField(verbose_name="Фото", upload_to='Downloads')
    description = models.TextField(verbose_name="Описание")


    def __str__(self):
        return self.title


class Order(models.Model):
    client_name = models.CharField(verbose_name="Имя клиента", max_length=200, blank=True)
    address = models.CharField(verbose_name='адрес', max_length=200, blank=True)
    date = models.CharField(verbose_name="Дата доставки", max_length=200, blank=True, null=True)
    time = models.CharField(verbose_name="Время доставки", max_length=200, blank=True, null=True)
    bouquet = models.ForeignKey(Bouquet, blank=True,null=True, on_delete=models.CASCADE)


class Memory(models.Model):
    click_event = models.CharField(max_length=200, null=True)
    click_price = models.CharField(max_length=200, null=True)




