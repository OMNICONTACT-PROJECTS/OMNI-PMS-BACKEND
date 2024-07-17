from import_export import fields, resources,widgets

from accounts.models import User
from .models import Subscriber


# class SubscriberResource(resources.ModelResource):
#     class Meta:
#         model = User
#         import_id_fields = [ 
#             "organisation",
#             "first_name",
#             "last_name",
#             "gender",
#             "email",
#             "phone_number",
#             "national_id",
#             "nationality",
#             "province",
#             "home_address",
#             "job_title",
#             "dob",
#             "current_location",
#             "user_status",
#             "account_status",
#             "contract_type",
#             "contract_tenure"
            
#         ]
#         fields = (
#             # "id",
#            "organisation",
#             "first_name",
#             "last_name",
#             "gender",
#             "email",
#             "phone_number",
#             "national_id",
#             "nationality",
#             "province",
#             "home_address",
#             "job_title",
#             "dob",
#             "current_location",
#             "user_status",
#             "account_status",
#             "contract_type",
#             "contract_tenure"
#         )
#         skip_unchanged = True
#         use_bulk = True
#         report_skipped = False


class UserWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        else:
            obj, _ = User.objects.update_or_create(
                pk=value,
                defaults={
                
                    'organisation': row.get('organisation'),
                    'first_name': row.get('first_name'),
                    'last_name': row.get('last_name'),
                    'gender': row.get('gender'),
                    'email': row.get('email'),
                    'phone_number': row.get('phone_number'),
                    'national_id': row.get('national_id'),
                    'nationality': row.get('nationality'),
                    'province': row.get('province'),
                    'home_address': row.get('home_address'),
                    'job_title': row.get('job_title'),
                    'dob': row.get('dob'),
                    'current_location': row.get('current_location'),
                    'user_status': row.get('user_status'),
                    'account_status': row.get('account_status'),
                    'contract_type': row.get('contract_type'),
                    'contract_tenure': row.get('contract_tenure'),
                }
            )
        return obj

class SubscriberResource(resources.ModelResource):
    user = fields.Field(
        column_name='user_id',
        attribute='user',
        widget=UserWidget(User, 'pk')
    )
    class Meta:
        model= Subscriber
        fields=('id','user')


    # def before_save_instance(self, instance, *args, **kwargs):
    #     # Ensure user instance is saved first
    #     instance.user.save()

    # def after_save_instance(self, instance, *args, **kwargs):
    #     # Ensure that instance.user_id is updated
    #     instance.user_id = instance.user.id
    #     instance.save()

    def before_save_instance(self, instance, *args, **kwargs):
        # Ensure user instance is saved first
        # instance = User
        if instance:
            instance.save()
        else:
            # Handle the case where instance.user is None
            raise ValueError("User instance is None, cannot save.")

    def after_save_instance(self, instance, *args, **kwargs):
        # Ensure that instance.user_id is updated
        # instance = Subscriber
        if instance:
            instance.user_id = instance.user.id
            instance.save()
        else:
            # Handle the case where instance.user is None
            raise ValueError("User instance is None, cannot update user_id.")



