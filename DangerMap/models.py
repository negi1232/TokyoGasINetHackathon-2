from django.db import models

"""
避難場所のモデル
"""
class EvacuationSite(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


"""
危険な場所のモデル
"""
class DangerLocations(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    dangerType = models.CharField(max_length=30)
