# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random, operator

from django.db.models import Q
from django.utils.text import slugify


from FHLBuilder import models as bmod
from FHLBuilder import choices

from FriendlyHomeLibrary import settings


def find_objects(me, target):
    """
    find all members of list marked as liked or loved by me
    """
    likedlist = target.filter(likes__username=me)
    lovedlist = target.filter(loves__username=me)
    
    return likedlist,lovedlist


def kind_from_tag(akind, tagobj):
    """
    given a tag, find all objects matching kind
    """
    kind = akind[0]
    if kind in choices.videos:
        return tagobj.movie_tags.filter(fileKind=kind)
    if kind == choices.SONG:
        return tagobj.song_tags.all()
    if kind == choices.PICTURE:
        return tagobj.picture_tags.all()
    return CommonFile.objects.none()


def kind_from_all(akind):
    """
    given a kind, find all objects in the database matching that kind
    """
    kind = akind[0]
    if kind in choices.videos:
        return bmod.Movie.objects.filter(fileKind=kind)
    if kind == choices.SONG:
        return bmod.Song.objects.all()
    if kind == choices.PICTURE:
        return bmod.Picture.objects.all()
    return bmod.CommonFile.objects.none()


def random_count(mylist,count):
    mysize = mylist.count()
    if mysize <= count:
        return mylist

    rand_entities = random.sample( range(mysize), count)
    flist = []
    for ind in rand_entities:
        flist.append(mylist[ind])
    return flist    


def tag_select(kind,tag):
    mylist = bmod.CommonFile.objects.none()
    if len(tag):
        tSlug = slugify(unicode('%s' % (tag)))
        try:
            target = bmod.Tag.objects.get(slug__iexact=tSlug)
            mylist = kind_from_tag(kind,target)
        except bmod.Tag.DoesNotExist:
            return mylist
    return mylist
    

def random_select(count, kind, tag):
    """
    Find a list of count random objects (or all if there are less than count)
    with matching kind and tag
    """
    mylist = bmod.CommonFile.objects.none()
    if len(tag):
        mylist = tag_select(kind,tag)
    else:
        mylist = kind_from_all(kind)
    return random_count(mylist,count)


def random_select(count, title, tag,kind):
    """
    Find a list of count random cartoons
    """

    mylist = bmod.CommonFile.objects.none()

    # either tag or full list
    if len(tag):
        mylist = tag_select(kind,tag)
    else:
        mylist = kind_from_all(kind)

    # refine for title
    if len(title):
        mylist = mylist.filter(title__icontains=title)

    return random_count(mylist,count)


def videos_by_title(alist):
    """
    Find a list of videos matching any of a list of titles
    """
    query = reduce(operator.or_, (Q(title__icontains = item) for item in alist))
    return bmod.Movie.objects.filter(query)


def saturday_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['animaniacs','hrpufnstuf','looneytunes',
        'magillagorilla','pingo','pinkpanther',
        'scoobydoo','tomandjerry','woodywoodpecker',
        'schoolhouse','thunderbirds','littlerascals',
        'threestooges']

    return random_count(videos_by_title(titles),count)


def silly_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['animaniacs','threestooges'
        'faulty','montypython','allinthefamily',
        'getsmart','seinfeld',
        'carolburnet','evildead','brisco',
        'mrbean','muppetshow','snl','thinblue',
        'dirkgently'
        ]

    return random_count(videos_by_title(titles),count)


def drama_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['boston_legal','allcreatures','drwho',
        'Emergency', 'er-s','rescueme',
        'blackadder','bones','breakingbad',
        'greysanatomy','rescueme','stelsewhere',
        'weeds','treme','vinyl'
        ]

    return random_count(videos_by_title(titles),count)


def scifi_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['drwho','startrek','firefly','lost',
        'xfiles','supergirl','terminator',
        'twilightzone','legendsoftomorrow'
        ]

    return random_count(videos_by_title(titles),count)


def scary_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['drwho','mastersofhorror','americanhorrorstory',
        'xfiles','ghoststories','haunting','twilightzone'
        ]

    return random_count(videos_by_title(titles),count)


def sitcom_select(count):
    """
    Speciality query to select sitcoms
    """
    # add a couple cartoons to sitcom channel    
    q1 = Q(fileKind__exact=choices.TV_SITCOM)
    q2 = Q(title__icontains='flintstones')
    q3 = Q(title__icontains='southpark')
    
    alist = bmod.Movie.objects.filter(q1|q2|q3)
    return random_count(alist,count)


def mix(rest,mine,mixit):
    """mix 2 lists """
    
    result = []
    count = 0
    mycount = len(mine)-1
    for a in rest:
        count = count+1
        if count == mixit:
            if mycount >= 0:
                result.append(mine[mycount])
                count = 0;
                mycount = mycount-1
        result.append(a) 
    if mycount == 0:
        result.append(mine[0])
    return result


def radio_select(count,justme,me):
    if justme:
        g1 = Q(likes__username=me)
        g2 = Q(loves__username=me)
        b1 = Q(dislikes__username=me)
        set1 = bmod.Song.objects.all().exclude(b1)
        set2 = bmod.Song.objects.filter(g1|g2)
        
        if set2.count():
            # take about one tenth of the list from favourites
            # or half if length is less than 10
            mixit = 10 if count > 10 else 2
            portion = count//mixit
            mine = random_count(set2,portion)
            rest = random_count(set1,count-portion)        
            return mix(rest,mine,mixit)
        return random_count(set1,count)            
    final = bmod.Song.objects.filter(dislikes=None)
    return random_count(final,count)

