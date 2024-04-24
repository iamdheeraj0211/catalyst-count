from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UploadDataModel(models.Model):
    document                        = models.FileField(blank=True,null=True,help_text="media Document")

    created_at                      = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by                      = models.ForeignKey(User, blank = True, null = True, on_delete=models.CASCADE,related_name="created_file")
    is_deleted                      = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self) -> str:
        return str(self.id)