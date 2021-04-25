import os
from FriendlyHomeLibrary import settings
from FHLBuilder import utility
from FHLBuilder import models
from FHLBuilder import choices

def play_with_links_old():
    for current in models.Movie.objects.all():
        local_path = utility.object_path_local(current)
        file_exists = os.path.exists(local_path)
        #print('path %s exists: %s ' % (local_path, file_exists))
        
        if file_exists and os.path.islink(local_path):
            print('LINK %s' % local_path)
            
def play_with_links():
    for current in models.Movie.objects.filter(fileName__istartswith='rdm'):
        print('fixing %s' % current.fileName)
        current.fileKind = choices.BF_RANDOM
        current.save()

def verify_list(alist):
    blist = []
    utility.log('--- Starting Diagnostics ---')
    for current in alist:
        if current.collection is None:
            msg = (u'DELETING no collection %s' % current.title)
            utility.log(msg)
            blist.append(msg)
            #current.delete()
        elif os.path.exists(settings.DRIVES[0]):
            lpath = utility.object_path_local(current)
            file_exists = os.path.exists(lpath)
            if not file_exists:
                msg = (u'DELETING file does not exist %s %s' % 
                    (current.collection.filePath, current.title))
                utility.log(msg)
                blist.append(msg)
                #current.delete()
        else:
            msg = (u'ERROR diagnostic abandonded missing path %s' % 
                settings.DRIVES[0])
            blist.append(msg)
            utility.log (msg)
    return blist
