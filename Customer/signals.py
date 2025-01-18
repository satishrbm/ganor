# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Customers, Supply
# from datetime import date, timedelta

# @receiver(post_save, sender=Customers)
# def create_supply_entries(sender, instance, created, **kwargs):
#     if created:
#         start_date = instance.Started_at
#         end_date = instance.End_date
#         current_date = start_date
#         while current_date <= end_date:
#             Supply.objects.create(
#                 Customer=instance,
#                 Supply_date=current_date,
#                 Today_cost=0.0,
#                 Total_bottle=instance.Morning_bottle,
#                 Total_cost=0.0,
#                 updated_at=date.today()
#             )
#             if instance.Milk_delivery_frequency == '1':  # Daily delivery
#                 current_date += timedelta(days=1)
#             elif instance.Milk_delivery_frequency == '2':  # Every Other Day delivery
#                 current_date += timedelta(days=2)
#             elif instance.Milk_delivery_frequency == '3':  # Weekly delivery
#                 current_date += timedelta(weeks=1)
