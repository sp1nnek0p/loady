from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User
import uuid
import geocoder
# Create your models here.

class Vehicle(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        ordering = ['type']

    def __str__(self) -> str:
        return self.type


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.tag


class Load(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tagname = models.ManyToManyField(Tag, related_name='tagname', blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    vehicleType = models.ForeignKey(Vehicle ,on_delete=models.SET_NULL, null=True, blank=True, default=1)
    pickup = models.CharField(max_length=100)
    pickX = models.FloatField(default=0)
    pickY = models.FloatField(default=0)
    dropoff = models.CharField(max_length=200)
    dropX = models.FloatField(default=0)
    dropY = models.FloatField(default=0)
    product = models.CharField(max_length=100, default="General Goods")
    git = models.BooleanField(default=False)
    price = models.FloatField(default=0.0)
    pricePerTon = models.BooleanField(default=False)
    totalTons = models.IntegerField(default=1)
    totalVehiclesRequired = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)
    ordernumber = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self) -> str:
        return self.title

    
    def save(self, *args, **kwargs):
        try: 
            g = geocoder.osm(self.pickup)
        except:
            g = NULL
        
        if g != NULL:
            self.pickX = g.osm['x']
            self.pickY = g.osm['y'] 
        else:
            self.pickX = self.pickY = 0

        try: 
            g = geocoder.osm(self.dropoff)
        except:
            g = NULL
        
        if g != NULL:
            self.dropX = g.osm['x']
            self.dropY = g.osm['y'] 
        else:
            self.dropX = self.dropY = 0

        return super(Load, self).save(*args, **kwargs)


class DirectMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='toUser')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True, default="")
    read = models.BooleanField(default=False)
    replyto = models.CharField(max_length=100, blank=True, null=True, default="")
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self) -> str:
        return self.title


class LoadMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    load = models.ForeignKey(Load, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self) -> str:
        return self.body[:25]


class DetailUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    email = models.EmailField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    isTranporter = models.BooleanField(default=False)
    emailConfirmed = models.BooleanField(default=False)
    documentsVerified = models.BooleanField(default=False)
    fleetsize = models.IntegerField(default=0)
    companyName = models.CharField(max_length=100, blank=True, null=True)
    companyDescription = models.TextField(blank=True, null=True)
    registrationNumber = models.CharField(max_length=150, blank=True, null=True)
    contactNumber = models.CharField(max_length=50, blank=True, null=True)
    addressLine1 = models.CharField(max_length=100, blank=True, null=True)
    addressLine2 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.companyName

    