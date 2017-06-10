# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import random, operator

from django.db.models import Q
from django.utils.text import slugify

from FHLBuilder import models as bmod
from FHLBuilder import choices

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
    return bmod.CommonFile.objects.none()


def recent_bykind(kind, count):
    """
    given a kind, find all objects in the database matching that kind
    """
    ob = '-date_added'
    if kind in choices.videos:
        return bmod.Movie.objects.filter(fileKind=kind).distinct().order_by(ob)[0:count]
    if kind == choices.SONG:
        return bmod.Song.newest_objects.all().distinct()[0:count]
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
    given a list (not a queryset) mylist, randomly select count
    objects and return them as a list
    """
    mysize = len(mylist)
    
    if mysize <= count:
        count = mysize

    rand_entities = random.sample( xrange(mysize), count)
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
    

def random_select_unused(count, kind, tag,o_random=True):
    """
    return QuerySet of count random objects
    correspondong to any of the parameters passed in
    tag is optional, count and kind are not    
    """
    if len(tag):
        mylist = tag_select(kind,tag)
    else:
        mylist = kind_from_all(kind)
    if o_random:
        return mylist.order_by('?')[:count]
    return mylist[:count]


def random_select(count, title, tag, kind,o_random=True):
    """
    return QuerySet of count random objects
    correspondong to any of the parameters passed in
    title and tag are optional, count and kind are not
    """

    # either tag or full list
    if len(tag):
        mylist = tag_select(kind,tag)
    else:
        # no tag was chosen, start with all matching kind
        mylist = kind_from_all(kind)

    # refine for title
    if len(title):
        mylist = mylist.filter(title__icontains=title)

    if o_random:
        return mylist.order_by('?')[:count]
    return mylist[:count]


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
    return tv_by_title(titles).order_by('?')[:count]


def silly_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['threestooges','faulty','montypython',
        'carolburnet','bennyhill','mrbean','muppetshow','snl',
        'dirkgently','hitchhiker','policesquad'
        ]
    return tv_by_title(titles).order_by('?')[:count]


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
    return tv_by_title(titles).order_by('?')[:count]


def scifi_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['drwho','startrek','firefly','lost',
        'xfiles','supergirl','terminator',
        'twilightzone','legend','stng'
        ]
    return tv_by_title(titles).order_by('?')[:count]


def scary_select(count):
    """
    Speciality query to select Saturday Morning Cartoons
    """
    titles = ['drwho','mastersofhorror','americanhorrorstory',
        'xfiles','ghoststories','haunting','twilightzone'
        ]

    return tv_by_title(titles).order_by('?')[:count]


def sitcom_select(count):
    """
    Speciality query to select sitcoms
    """
    # add a couple cartoons to sitcom channel    
    q1 = Q(fileKind__exact=choices.TV_SITCOM)
    q2 = Q(title__icontains='flintstones')
    q3 = Q(title__icontains='southpark')
    
    return bmod.Movie.tv_objects.filter(q1|q2|q3).order_by('?')[:count]


def mix(rest,mine,mixit):
    """
    mix 2 lists
    mixit indicates how many from mine list, for example
    if mixit is 10 every 10th song should come from 2nd list
    """
    
    result = []
    count = 0
    mycount = 0
    mel = len(mine)  
    
    for a in rest:
        count+=1
        mres = count % mixit
        if not mres:
            if mycount < mel:
                result.append(mine[mycount])
                mycount+=1
        result.append(a)
            
    return result


def radio_list(start,justme,me,cl):
    """
    Get the list of random songs added prefered songs if requested
    add classical songs if requested
    """
    if justme:
        g1 = Q(likes__username=me)
        g2 = Q(loves__username=me)
        set2 = exclude_ick_xmas(bmod.Song.random_objects.filter(g1|g2))
        if set2.count():
            start = mix(start,set2,10)
    if cl:
        cq = Q(tags__name__icontains='classical')
        clst = exclude_ick_xmas(bmod.Song.random_objects.filter(cq))
        if clst.count():
            start = mix(start,clst,25)
    return start


def exclude_ick(big):    
    ick1 = Q(tags__name__icontains='bagpipe')
    ick2 = Q(tags__name__icontains='fiddle')
    ick3 = Q(tags__name__icontains='yuck')
    # by default exclude classical music
    cq = Q(tags__name__icontains='classical')
    return big.exclude(ick1|ick2|ick3|cq)


def exclude_ick_xmas(big):
    b1 = Q(tags__name__icontains='christmas')
    b2 = Q(title__icontains='christmas')
    b3 = Q(tags__name__icontains='seasonal')
    
    return exclude_ick(big.exclude(b1|b2|b3))


def only_xmas(big):
    b1 = Q(tags__name__icontains='christmas')
    b2 = Q(title__icontains='christmas')
    b3 = Q(tags__name__icontains='seasonal')
    
    return exclude_ick(big.filter(b1|b2|b3))


def radio_select(justme,me,target,cl):
    """
    Select a list of non-Christmas songs
    if justme is true include favourites of me
    target is the start list to select from
    if cl is true include some classical music
    """
    big = exclude_ick_xmas(target)
    if justme:
        yuck = Q(dislikes__username=me)
        start = big.exclude(yuck)
    else:
        start = big.filter(dislikes=None)
    
    return radio_list(start,justme,me,cl)


def radio_select_christmas(justme,me,target,cl):
    """
    select an appropriate mix of Christmas songs
    if justme is true include favourites of me
    target is the start list to select from
    if cl is true include some classical music    
    """
    # no Christmas part
    big = exclude_ick_xmas(target)
    if justme:
        yuck = Q(dislikes__username=me)
        start = big.exclude(yuck)
    else:
        start = big.filter(dislikes=None)
        
    therest = radio_list(start,False,me,False)

    # Christmas
    big = only_xmas(target)
    
    if justme:
        yuck = Q(dislikes__username=me)
        start = big.exclude(yuck)
    else:
        start = big.filter(dislikes=None)
        
    xmas = radio_list(start,False,me,False)
    
    radio = christmas(therest, xmas)
    if justme or cl:
        return radio_list(radio,justme,me,cl)
    return radio


def christmas(rest, xmas):
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


def artist_radio_select(artists,xmas):
    """
    passed a queryset containing artists and boolean for xmas
    returns a list of all songs by artists in that queryset
    without ick
    """
    query = reduce(operator.or_, (Q(song_musicians=item) for item in artists))                           
    
    big = bmod.Song.objects.filter(query).order_by('?')
        
    if xmas:
        return exclude_ick(big)
    else:
        return exclude_ick_xmas(big)
    

def collection_radio_select(colls,xmas):
    """
    passed a queryset containing collections and boolean for xmas
    returns a list of all songs by artists in that queryset
    without ick
    """
    query = reduce(operator.or_, (Q(collection=item) for item in colls))                           
    
    big = bmod.Song.objects.filter(query).order_by('?')
        
    if xmas:
        return exclude_ick(big)
    else:
        return exclude_ick_xmas(big)
    
