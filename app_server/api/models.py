from django.db import models
from django.utils import timezone
import os.path

DOWNLOADS_PATH = './downloads/'

# Create your models here.
class Instance(models.Model):
    name = models.CharField(max_length=100)
    problem_type = models.CharField(max_length=100)
    path = models.CharField(max_length=200, blank=True)


class InstanceFeature(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, blank=True)


class InstanceValue(models.Model):
    value = models.CharField(max_length=400)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    feature = models.ForeignKey(InstanceFeature, on_delete=models.CASCADE)


def define_path(instance, filename):
    path_exist = True
    while path_exist:
        now = timezone.now()
        path_format = DOWNLOADS_PATH + '%Y/%m/%d/' + filename + '_%H%M%S%f'
        path_name = now.strftime(path_format)
        path_exist = os.path.isfile(path_name)
    return path_name

class Solver(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)
    source_path = models.FileField(upload_to=define_path, blank=True)
    executable_path = models.FileField(upload_to=define_path, blank=True)

    # from stackoverflow
    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Solver, self).save(*args, **kwargs)


# TODO add User
class Experimentation(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    solver_parameters = models.CharField(max_length=200)
    solver = models.ForeignKey(Solver, on_delete=models.CASCADE)
    device = models.CharField(max_length=200, blank=True)


class Result(models.Model):
    status = models.CharField(max_length=100)
    result = models.ForeignKey(Experimentation, on_delete=models.CASCADE)


class ResultMeasurement(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, blank=True)


class ResultValue(models.Model):
    value = models.CharField(max_length=400)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    measurement = models.ForeignKey(ResultMeasurement, on_delete=models.CASCADE)
