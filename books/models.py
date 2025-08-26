from enum import Enum
from django.db import models

# Title: str
# Author: str
# Cover: Enum: HARD | SOFT
# Inventory*: positive int
# Daily fee: decimal (in $USD)

#  * Inventory – the number of this specific book available now in the library

class Cover(str, Enum):
    SOFT = "SOFT"
    HARD = "HARD"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
      max_length=4,
      choices=[(cover, cover.value) for cover in Cover]
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)
