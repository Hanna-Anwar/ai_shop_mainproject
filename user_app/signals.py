from django.db.models.signals import post_save

from django.dispatch import receiver

from user_app.models import CustomUserModel

from django.core.mail import send_mail

@receiver(post_save,sender=CustomUserModel)
def sent_register_mail(sender,instance,created,**kwargs):

    if created:

        subject = "Welcome Aboard! Your Account Is Ready"

        message = """Welcome to our Fashion Store!

        Your account has been created successfully. 
        You can now explore new arrivals, track your orders, and enjoy a personalized shopping experience.

        Thank you for joining our community!"""
        
        from_email = "hannaanwar469@gmail.com"

        recipient_list = [instance.email]

        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=True)

        print("mail sended")    
    