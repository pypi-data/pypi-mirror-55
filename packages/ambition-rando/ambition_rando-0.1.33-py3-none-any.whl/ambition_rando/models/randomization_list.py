from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager

from ..constants import CONTROL, CONTROL_NAME, SINGLE_DOSE, SINGLE_DOSE_NAME
from ..randomizer import RandomizationError


class RandomizationListModelError(Exception):
    pass


class RandomizationListManager(models.Manager):
    def get_by_natural_key(self, sid):
        return self.get(sid=sid)


class RandomizationList(BaseUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier", max_length=50, null=True, unique=True
    )

    sid = models.IntegerField(unique=True)

    assignment = EncryptedTextField(
        choices=((SINGLE_DOSE, SINGLE_DOSE_NAME), (CONTROL, CONTROL_NAME))
    )

    site_name = models.CharField(max_length=100)

    allocation = EncryptedTextField(
        verbose_name="Original integer allocation", null=True
    )

    allocated = models.BooleanField(default=False)

    allocated_datetime = models.DateTimeField(null=True)

    allocated_user = models.CharField(max_length=50, null=True)

    allocated_site = models.ForeignKey(
        Site, null=True, on_delete=models.CASCADE, related_name="+"
    )

    verified = models.BooleanField(default=False)

    verified_datetime = models.DateTimeField(null=True)

    verified_user = models.CharField(max_length=50, null=True)

    objects = RandomizationListManager()

    history = HistoricalRecords()

    on_site = CurrentSiteManager("allocated_site")

    def __str__(self):
        return f"{self.site_name}.{self.sid} subject={self.subject_identifier}"

    def save(self, *args, **kwargs):
        try:
            self.treatment_description
        except RandomizationError as e:
            raise RandomizationListModelError(e)
        try:
            Site.objects.get(name=self.site_name)
        except ObjectDoesNotExist:
            site_names = [obj.name for obj in Site.objects.all()]
            raise RandomizationListModelError(
                f"Invalid site name. Got {self.site_name}. "
                f"Expected one of {site_names}."
            )
        super().save(*args, **kwargs)

    @property
    def short_label(self):
        return f"{self.assignment} SID:{self.site_name}.{self.sid}"

    @property
    def treatment_description(self):
        if self.assignment == CONTROL:
            return CONTROL_NAME
        elif self.assignment == SINGLE_DOSE:
            return SINGLE_DOSE_NAME
        raise RandomizationError(f"Invalid assignment. Got {self.assignment}")

    def natural_key(self):
        return (self.sid,)

    class Meta:
        ordering = ("site_name", "sid")
        unique_together = ("site_name", "sid")
        permissions = (("display_assignment", "Can display assignment"),)
