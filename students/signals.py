from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):

    if created:
        UserProfile.objects.create(user=instance)

# NEXT STEP GO IN apps.py there StudentConfigClass is already created, in this built a  ready function and import students.signals

# NEXT STEP= Go to setting,py there in INSTALLED APPS add students.apps.StudentConfig



# post_save means:Run something after a model is saved.
# When you do:
# user = User.objects.create(username="parth")

# Django saves the user first, then triggers:

# post_save
#    ↓
# my_function()



# UserProfile.objects.create(user=instance)means:Create a UserProfile and connect it to the User stored in instance.



# sender tells you:  Which model sent the signal?

# The instance is the actual User object that was saved.

# Created: This tells you whether this is a new object.If a new User was created:
# created = True :If an existing User was updated:
# created = False


# **kwargs means:Accept additional keyword arguments that Django sends with the signal.