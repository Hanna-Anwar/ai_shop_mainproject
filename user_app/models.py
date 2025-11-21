from django.db import models

from django.contrib.auth.models import AbstractUser


#user registration

class CustomUserModel(AbstractUser):

    full_name = models.CharField(max_length=100)

    mobile_no = models.CharField(max_length=15,unique=True)


#profile model

class UserProfileModel(models.Model):

    user = models.OneToOneField(CustomUserModel,on_delete=models.CASCADE)

    # Delivery info

    address = models.TextField(blank=True,null=True)

    city = models.CharField(max_length=100,blank=True,null=True)

    state = models.CharField(max_length=100,blank=True,null=True)

    pincode = models.CharField(max_length=100,blank=True,null=True)
    
    # Size + body details (for ML model)

    height = models.FloatField(blank=True,null=True) #in cm

    weight = models.FloatField(blank=True,null=True)  #in kg

    body_shape = models.CharField(max_length=100,blank=True,null=True,
                                  
                                   choices=[('hourglass','Hourglass'),
                                           ('pear','Pear Shape'),
                                            ('apple','Apple Shape'),
                                            ('rectangle','Rectangle'),
                                            ('inverter_triangle',"Inverted Triangle"),
                                            ('diamond','Diamond Shape'),
                                            ('oval','Oval/Round')
                                            ])
    
    preferred_size = models.CharField(max_length=15,blank=True,null=True,
                                      
                                      choices=[
                                         ("XS","XS"), ("S","S"), ("M","M"),
                                         ("L","L"), ("XL","XL"), ("XXL","XXL"),
                                         ('3XL','3XL'),('4XL','4XL'),
                                         ])
    
    # Shopping preference for chatbot recommendation

    style_preference = models.CharField(max_length=100,blank=True,null=True,
                                        
                                        choices=[
                                         ("casual", "Casual"),
                                         ("office", "Office Wear"),
                                         ("party", "Party Wear"),
                                         ("ethnic", "Ethnic Wear"),
                                         ("sports", "Sportswear"),   
                                        ])
    
    
    favorite_color = models.CharField(max_length=50, blank=True, null=True)








