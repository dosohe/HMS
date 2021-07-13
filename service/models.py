from django.db import models

class Room(models.Model):
    ROOM_TYPES = (
        ('YAC', 'AC'),
        ('NAC', 'NON-AC'),
        ('DEL', 'DELUX'),
        ('KIN', 'KING'),
        ('QUE', 'QUEEN'),
    )
    type = models.CharField(max_length=3, choices=ROOM_TYPES)
    beds = models.IntegerField()
    number = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.number}: {self.type} with {self.beds} beds for {self.capacity} people'