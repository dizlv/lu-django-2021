from django.db import models


class SalaryEntry(models.Model):
    first_name = models.CharField(max_length=250)
    second_name = models.CharField(max_length=250)
    birth_day = models.DateField()

    amount = models.DecimalField(
        max_digits=11,
        decimal_places=4,
    )


class Bonus(models.Model):
    salary_entry = models.ForeignKey(
        to=SalaryEntry,
        on_delete=models.CASCADE,
    )

    amount = models.DecimalField(
        max_digits=11,
        decimal_places=4,
    )
