from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#extends User with a profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trips = models.ManyToManyField('Trip')

    def __str__(self):
        return self.user.first_name + ', ' + self.user.last_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Trip(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return 'Trip to ' + self.destination

