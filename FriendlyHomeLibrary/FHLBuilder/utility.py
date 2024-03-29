import os
import datetime

from FriendlyHomeLibrary import settings
from FHLBuilder import choices

#Utility functions


def log(msg):
    try:
        my_log = ('%s/log%s' % (settings.LOG_PATH,datetime.date.today()))
        with open(my_log,'a+') as f:
            f.write(msg)
            f.write('\n')
            f.close()
    except UnicodeDecodeError:
        print("RATS UnicodeDecodeError logging message %s" % msg)
        f.close()
    except UnicodeEncodeError:
        print("RATS UnicodeEncodeError logging Message %s" % msg)
        f.close()


        

def slugCompare(s1,s2):
    remove = str.maketrans('-','_')
    c1 = str(s1).translate(remove)
    c2 = str(s2).translate(remove)
    return c1==c2

def get_drive(driveNo):
    return str(settings.DRIVES[driveNo-1])

def get_drive_samba(driveNo):
    return str(settings.SDRIVES[driveNo-1])

def get_drive_slink(driveNo):
    return str(settings.LDRIVES[driveNo-1])


def object_path(obj):
    """ return the path from links in django's static path """
    if obj is None:
        message = str('error - request path object None')
        raise Exception(message)        
    if obj.collection is None:
        message = str('error - request path object collection none %s type %s' % (obj.title,type(obj)))
        raise Exception(message)
    drive = get_drive_slink(obj.collection.drive)
    thePath = str(os.path.join(u'links/', drive))
    thePath = str(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return str(thePath)


def object_path_with_static(obj):
    """ return the path from static/links django's static path """
    drive=str(u'drive') + str(obj.collection.drive)
    thePath = os.path.join(u'static/links/', drive)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName)
    return str(thePath)


def object_path_no_static(obj):
    """ return the path from static/links django's static path """
    drive=str(u'drive') + str(obj.collection.drive)
    thePath = os.path.join(u'links/', drive)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName)
    return str(thePath)


def object_path_web(obj):
    """ return the path from static/links django's static path """
    #drive=using path+str(u'drive') + str(obj.collection.drive)
    drive = get_drive_slink(obj.collection.drive)
    thePath = os.path.join(u'links/', drive)
    thePath = os.path.join(settings.HTTP_PREFIX,thePath)
    thePath = os.path.join(thePath, obj.collection.filePath,obj.fileName)
    return str(thePath)



def object_path_local(obj):
    """ real path to object using local samba link """
    thePath = get_drive(obj.collection.drive)
    thePath = str(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return str(thePath)


def object_path_samba(obj):
    """ real samba path to object for use on all machines """
    thePath = get_drive_samba(obj.collection.drive)
    thePath = str(os.path.join(thePath, obj.collection.filePath,obj.fileName))
    return str(thePath)


def collection_sets(collections):
    """ break a list of collections according to category  """
    songc = []
    moviec = []
    picturec = []
    variousc = []
    if collections is not None:
        for current in collections:
            sc = current.songs.count()
            mc = current.movies.count()
            pc = current.pictures.count()
            if sc and not mc and not pc:
                # only songs
                songc.append(current)
            elif mc and not sc and not pc:
                # only movies
                moviec.append(current)
            elif pc and not sc and not mc:
                # only pictures
                picturec.append(current)
            else:
                # various
                if sc > pc:
                    # some albums have a few pictures/movies
                    songc.append(current)
                elif pc > mc:
                    # picture directories may contain mini-movies
                    picturec.append(current)
                else:
                    variousc.append(current)
    return songc,moviec,picturec,variousc


def rescan(myreq,a):
    '''
    Cheats to make local rescans easier
    Ideally this should not be hard-coded with magic drive numbers
    but it's working for now
    '''
    if 'rescan-songs' in myreq:
        print('rescan scons')
        _,_ = a.add_members('mp3s',3,choices.CONCERT,'')            
    elif 'rescan-pictures' in myreq:
        print('rescan pictures')
        _,_ = a.add_members('picturesbackup',2,choices.MINI_MOVIE,'')            
    elif 'rescan-movies' in myreq:
        print('rescan-movies')
        _,_ = a.add_members('Videos',1,choices.MOVIE,'')
    elif 'rescan-video' in myreq:
        print('rescan bava')
        _,_ = a.add_members('Videos/bava',2,choices.MOVIE,'scary')
        print('rescan 3d')
        _,_ = a.add_members('Videos/3d',2,choices.MOVIE,'')
        print('rescan TV')
        _,_ = a.add_members('Videos/TV',2,choices.UNKNOWN,'')
        print('rescan comedy')
        _,_ = a.add_members('Videos/comedy',2,choices.STANDUP,'')
        print('rescan concert')
        _,_ = a.add_members('Videos/concert',2,choices.CONCERT,'')
        print('rescan documentaries')
        _,_ = a.add_members('Videos/documentaries',2,choices.DOCUMENTARY,'')
        print('rescan instructional')
        _,_ = a.add_members('Videos/Instructional',2,choices.MINI_MOVIE,'')
        print('rescan neal')
        _,_ = a.add_members('Videos/nealYoundArchives',2,choices.CONCERT,'')
        print('rescan workout')
        _,_ = a.add_members('Videos/Workout',2,choices.MINI_MOVIE,'')
        print('rescan snowboarding')
        _,_ = a.add_members('Videos/zz-snowboarding',2,choices.MINI_MOVIE,'')
        print('rescan twisted')
        _,_ = a.add_members('Videos/ZZtwistedMonk',2,choices.MINI_MOVIE,'')

