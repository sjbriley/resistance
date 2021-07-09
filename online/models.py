from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class CustomUser(User):
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']
    
    # def __str__(self):
    #     return 'name:\n\n' + self.name
    
    def create_user(self, email, date_of_birth, password=None):
        user = self.model(username = self.username)
        self.set_unusable_password()
        user.save(using=self._db)
        return user

    def set_password(self):
        return ''
    
    # def authenticate(self, username=None, password=None):
        # login_valid = (settings.ADMIN_LOGIN == username)
        # if login_valid:
        #     try:
        #         user = User.objects.get(username=username)
        #     except User.DoesNotExist:
        #         user = User(username=username)
        #         user.is_staff = True
        #         user.is_superuser = True
        #         user.save()
        #     return User
    # def validate_password(self):
    #     return True
    
    # def save(self, *args,**kwargs):
    #     self.validate_unique()
    #     super(CustomUser,self).save(*args, **kwargs)
    
