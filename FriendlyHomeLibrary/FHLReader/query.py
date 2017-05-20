# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

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


def kind_from_tag(kind, tagobj):
    """
    given a tag, find all objects matching kind
    """
    if kind in choices.videos:
        return tagobj.movie_tags.filter(fileKind=kind)
    if kind == choices.SONG:
        return tagobj.song_tags.all()
    if kind == choices.PICTURE:
        return tagobj.picture_tags.all()
    return CommonFile.objects.none()


def recent_bykind(kind, count):
    """
    given a kind, find all objects in the database matching that kind
    """
    print('query recent by kind %s' % kind)
    ob = '-date_added'
    if kind in choices.videos:
        return bmod.Movie.objects.filter(fileKind=kind).distinct().order_by(ob)[0:count]
    if kind == choices.SONG:
        return bmod.Song.objects.all().distinct().order_by(ob)[0:count]
    if kind == choices.PICTURE:
        return bmod.Picture.slide_objects.all().distinct().order_by(ob)[0:count]
    return bmod.CommonFile.objects.none()


def kind_from_all(kind):
    """
    given a kind, find all objects in the database matching that kind
    """
    if kind in choices.videos:
        return bmod.Movie.objects.filter(fileKind=kind)
    if kind == choices.SONG:
        return bmod.Song.objects.all()
    if kind == choices.PICTURE:
        return bmod.Picture.slide_objects.all()
    return bmod.CommonFile.objects.none()


def random_count(mylist,count):
    """
    given QuerySet mylist, randomly select count
    objects and return them as a list
    """
    mysize = len(mylist)
    
    if mysize <= count:
        return mylist

    rand_entities = random.sample( range(mysize), count)
    flist = []
    for ind in rand_entities:
        flist.append(mylist[ind])
    return flist    


def tag_select(kind,tag):
    """
    given objects of kind from the given tag
    if the tag is not passed, returns empty list
    """
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
    return QuerySet of count random objects
    correspondong to any of the parameters passed in
    tag is optional, count and kind are not    
    """
    mylist = bmod.CommonFile.objects.none()
    if len(tag):
        mylist = tag_select(kind,tag)
    else:
        mylist = kind_from_all(kind)
    return random_count(mylist,count)


def random_select(count, title, tag, kind):
    """
    return QuerySet of count random objects
    correspondong to any of the parameters passed in
    title and tag are optional, count and kind are not
    """
    mylist = bmod.CommonFile.objects.none()

    # either tag or full list
    if len(tag):
        mylist = tag_select(kind,tag)
    else:
        # no tag was chosen, start with all matching kind
        mylist = kind_from_all(kind)

    # refine for title
    if len(title):
        mylist = mylist.filter(title__icontains=title)

    return random_count(mylist,count)


def tv_by_title(alist):
    """
    Find a list of videos matching any of a list of titles
    """
    query = reduce(operator.or_, (Q(title__icontains = item) for item in alist))
    return bmod.Movie.tv_objects.filter(query)


def saturday_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['animaniacs','hrpufnstuf','looneytunes',
        'magillagorilla','pingo','pinkpanther',
        'scoobydoo','tomandjerry','woodywoodpecker',
        'schoolhouse','thunderbirds','littlerascals',
        'threestooges']

    return random_count(tv_by_title(titles),count)


def silly_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['animaniacs','threestooges'
        'faulty','montypython','allinthefamily',
        'getsmart','seinfeld',
        'carolburnet','evildead','bennyhill',
        'mrbean','muppetshow','snl','thinblue',
        'dirkgently','hitchhiker','policesquad'
        ]

    return random_count(tv_by_title(titles),count)


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

    return random_count(tv_by_title(titles),count)


def scifi_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['drwho','startrek','firefly','lost',
        'xfiles','supergirl','terminator',
        'twilightzone','legend','stng'
        ]

    return random_count(tv_by_title(titles),count)


def scary_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['drwho','mastersofhorror','americanhorrorstory',
        'xfiles','ghoststories','haunting','twilightzone'
        ]

    return random_count(tv_by_title(titles),count)


def sitcom_select(count):
    """
    Speciality query to select sitcoms
    """
    # add a couple cartoons to sitcom channel    
    q1 = Q(fileKind__exact=choices.TV_SITCOM)
    q2 = Q(title__icontains='flintstones')
    q3 = Q(title__icontains='southpark')
    
    alist = bmod.Movie.tv_objects.filter(q1|q2|q3)
    return random_count(alist,count)


def mix(rest,mine,mixit):
    """
    mix 2 lists
    mixit indicates how many from mine list, for example
    if mixit is 10 every 10th song should come from 2nd list
    """
    
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


def radio_list(start,count,justme,me):
    """
    Get the list of random songs added prefered songs if requested
    """
    if justme:
        g1 = Q(likes__username=me)
        g2 = Q(loves__username=me)
        
        set2 = bmod.Song.objects.filter(g1|g2)
        
        if set2.count():
            # take about one tenth of the list from favourites
            # or half if length is less than 10
            mixit = 10 if count > 10 else 2
            portion = count//mixit
            mine = random_count(set2,portion)
            rest = random_count(start,count-portion)        
            return mix(rest,mine,mixit)
    return random_count(start,count)    


def radio_select(count,justme,me,recent):
    """
    Select a list of non-Christmas songs
    """
    b1 = Q(tags__name__icontains='christmas')
    b2 = Q(title__icontains='christmas')
    b3 = Q(tags__name__icontains='seasonal')
    
    ick1 = Q(tags__name__icontains='bagpipe')
    ick2 = Q(tags__name__icontains='fiddle')
    ick3 = Q(tags__name__icontains='yuck')
    
    big = bmod.Song.objects.exclude(b1|b2|b3|ick1|ick2|ick3)
    if justme:
        yuck = Q(dislikes__username=me)
        start = big.exclude(yuck)
    else:
        start = big.filter(dislikes=None)

    if recent:
        start = start.order_by('-date_added')[:count]
    
    return radio_list(start,count,justme,me)


def radio_select_christmas(count,justme,me,recent):
    """
    select an appropriate mix of Christmas songs
    """
    b1 = Q(tags__name__icontains='christmas')
    b2 = Q(title__icontains='christmas')
    b3 = Q(tags__name__icontains='seasonal')

    ick1 = Q(tags__name__icontains='bagpipe')
    ick2 = Q(tags__name__icontains='fiddle')
    ick3 = Q(tags__name__icontains='yuck')

    # no Christmas part
    big = bmod.Song.objects.exclude(b1|b2|b3|ick1|ick2|ick3)
    if justme:
        yuck = Q(dislikes__username=me)
        start = big.exclude(yuck)
    else:
        start = big.filter(dislikes=None)
    
    if recent:
        start = start.order_by('-date_added')[:count]
    
    therest = radio_list(start,count,justme,me)

    # Christmas
    big = bmod.Song.objects.filter(b1|b2|b3).exclude(ick1|ick2|ick3)
    if justme:
        yuck = Q(dislikes__username=me)
        start = big.exclude(yuck)
    else:
        start = big.filter(dislikes=None)
    
    if recent:
        start = start.order_by('-date_added')[:count]
    
    xmas = radio_list(start,count,justme,me)
    
    return christmas(count, therest, xmas)


def christmas(count, rest, xmas):
    """
    Use today's date to mix Christmas songs
    with the rest of the songs
    """
    month = datetime.date.today().month
    day = datetime.date.today().day
    
    if month == 12:
        if day in [23,24,25,26]:
            return mix(xmas,rest,15)
        if day < 15:
            return mix(xmas,rest,4)
        return mix(xmas,rest,8)
    if month == 1:
        if day < 4:
            return mix(xmas,rest,4)
    if month == 11:
        if day < 25:
            return mix(rest,xmas,8)
        else:
            return mix(rest,xmas,5)
            
    return mix(rest,xmas,15)
