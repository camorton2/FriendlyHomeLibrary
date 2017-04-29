# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import string
from FriendlyHomeLibrary import settings
from FHLBuilder import utility
from FHLBuilder import models

def play_with_links():
    for current in models.Movie.objects.all():
        local_path = utility.object_path_local(current)
        file_exists = os.path.exists(local_path)
        #print('path %s exists: %s ' % (local_path, file_exists))
        
        if file_exists and os.path.islink(local_path):
            print('LINK %s' % local_path)
            


