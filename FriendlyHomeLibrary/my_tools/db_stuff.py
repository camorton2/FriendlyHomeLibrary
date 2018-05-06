# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from FriendlyHomeLibrary import settings
from FHLBuilder import utility
from FHLBuilder import models
from FHLBuilder import choices

def move_songs_to_drive(to_drive):
    print(u'Start work')
    count = 0
    for current in models.Song.objects.all():
        if current.collection.drive is not to_drive:
            count = count+1
            current.collection.drive = to_drive
            current.collection.save()
    print(u'Done, number of collections modified')
    print(count)
    
