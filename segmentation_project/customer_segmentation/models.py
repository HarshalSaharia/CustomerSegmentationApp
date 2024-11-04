from django.db import models

class CustomerData(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    annual_income = models.FloatField()  # in thousands
    spending_score = models.IntegerField()

    def __str__(self):
        return f"{self.customer_id}: {self.gender}, Age: {self.age}"

class ClusterResult(models.Model):
    cluster_id = models.IntegerField()
    description = models.TextField()
    customer = models.ForeignKey(CustomerData, on_delete=models.CASCADE)

    # New fields for average metrics
    avg_spending_score = models.FloatField(default=0.0)
    avg_annual_income = models.FloatField(default=0.0)

    def __str__(self):
        return f"Cluster {self.cluster_id}: {self.description}"
