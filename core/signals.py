from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()


@receiver(post_save, sender=get_user_model())
def send_email_handler(sender, instance, created, **kwargs):

    if created and instance.email:
        rendered = render_to_string('welcome_email.html', {'user': instance.get_full_name()})
        print("I WAS CALLED")
        print(sender, instance)
        try:
            send_mail(
                'Welcome To Fast Parcel',
                rendered,
                None,
                [instance.email],
                fail_silently=False,
            )
            print("EMAIL SENT TO: " + instance.email)
        except:
            print("EMAIL SENDING FAILED")
    else:
        print(created, sender, instance)
        print("EMAIL NOT SENT")