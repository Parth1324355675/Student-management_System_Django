from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'

    def ready(self):
        import students.signals

# Django calls ready() when the application has been loaded.
# "When the students app is ready, load my signals."