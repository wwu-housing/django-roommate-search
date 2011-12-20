from django.contrib.auth.models import User
from django.db import models


class Cluster(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"<Cluster: %s>" % self.name
    __str__ = __repr__ = __unicode__


class Profile(models.Model):
    STATUS_CHOICES = (("looking", "I am looking for a roommate; allow others to search for me."),
                      ("found", "I have found a roommate; do not allow others to search for me."),
                      ("withdrawn", "I am not looking for a roommate at this time."))

    screen_name = models.CharField(max_length=128, unique=True)
    bio = models.TextField()
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default="looking")
    user = models.ForeignKey(User,
                             related_name="myroommate_profiles",
                             editable=False)
    clusters = models.ManyToManyField(Cluster,
                                      related_name="profiles",
                                      editable=False)
    stars = models.ManyToManyField("self",
                                   symmetrical=False,
                                   editable=False)
    created_datetime = models.DateTimeField(auto_now_add=True,
                                            editable=False)
    last_activity = models.DateTimeField(auto_now=True,
                                         editable=False)

    def __unicode__(self):
        return u"<Profile: %s for %s>" % (self.user, self.term)
    __str__ = __repr__ = __unicode__

