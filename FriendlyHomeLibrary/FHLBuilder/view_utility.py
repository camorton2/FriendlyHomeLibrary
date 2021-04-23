from django.urls import reverse
from django.shortcuts import render,redirect
from django.utils.text import slugify

from FHLBuilder import models
from FHLBuilder import collection
from FHLBuilder import choices
from FHLBuilder import utility

from FHLReader import kodi,chromecast
from FHLReader import utility as rutils

#def run_slideshow(pictures):
    #length = len(pictures)
    #count = 0
    #for p in pictures:
    #    count = count+1
    #    print('redirect %s' % (p.slug))
    #    gohere = reverse('builder_picture_detail', 
    #        kwargs = { 'slug':p.slug })
    #    print('gohere %s' % gohere)
    #    redirect(gohere)
    #    time.sleep(30)
#    pass


def generic_collection_view(request, **kwargs):
    """
    Keep view details and playback requests in a single place
    so all collections view look the same and have the same options
    """

    if 'stopshow' in request.GET:
        slideshow = False
        return redirect(reverse('user_page'))
        
    template_name = 'FHLBuilder/collection_detail.html'
    slideshow = False
    
    # respond to playlist
    if 'playlist' in request.GET:
        asPlayList = True
    else:
        asPlayList = False

    # arguments and defaults        
    songs=kwargs.get('songs',[])
    movies=kwargs.get('movies',[])
    pictures=kwargs.get('pictures',[])
    artists=kwargs.get('artists',[])
    title=kwargs.get('title','Collection View')
    allowChoice = kwargs.get('allowChoice',False)
    kind=kwargs.get('kind',choices.UNKNOWN)
    update=kwargs.get('update',None)    
    sorder=kwargs.get('myorder',choices.NAME)

    allow_tag = True
    
    if kind == choices.SONG and not len(songs):
        # no tagging everything please
        allow_tag = False        
        if sorder == choices.NEWEST:
            songs = models.Song.newest_objects.all()
        elif sorder == choices.OLDEST:
            songs = models.Song.oldest_objects.all()
        else:
            songs = models.Song.objects.all()
            
        title = ('All Songs %d' % songs.count())

    if sorder == choices.NEWEST:
        ob = '-date_added'
    elif sorder == choices.OLDEST:
        ob = 'date_added'
    else:
        ob = 'title'

    if kind in choices.videos and not len(movies):
        allow_tag = False
        # all movies view, can there be a faster option?
        olist,title =  movies_bykind(kind)
        movies = olist.order_by(ob)
    
    # respond to slide show
    current_picture = 1
    picture = None
    filename = None

    picture_count = len(pictures)

    use_all = False
    if not picture_count and kind == choices.PICTURE:
        # all pictures view
        picture_count = models.Picture.slide_objects.all().count()
        use_all = True

    try:
        me = models.User.objects.get(username=request.user)
    except models.User.DoesNotExist:
        # anonymous user
        me = None
    except Exception as ex:
        utility.log("ERROR unhandled exception %s" % (type(ex).__name__))
        
    message = ''

    ccasts = []

    #print(request.GET)
    if 'options' in request.GET and not slideshow:
        #print('A hey go get cc ss %s' % slideshow)
        ccasts = chromecast.find_chrome_casts()
        val = request.GET.get('options')
        if val == 'slideshow':
            slideshow = True
        elif val[:4] == 't___':
            dev = val[4:]
            chromecast.cast_slides(dev,pictures,me,True)
        elif val[:4] == 'cst_':
            dev = val[4:]
            chromecast.cast_slides(dev,pictures,me,False)
        elif val == 'CastAll-title':
            chromecast.cast_slides_all(pictures,me,True)
        elif val == 'CastAll':
            chromecast.cast_slides_all(pictures,me,False)
        else:
            # kodi playlist options
            try:
                res = kodi.playlist_requests_new(pictures,val,me,request)
                if res:
                    message = u'success - pictures sent'
            except rutils.MyException as ex:
                message = ex.message
                #print('Caught %s' % ex.message)
            
        
    if 'sNext' in request.GET and request.GET.get('sNext'):
        current_picture = int(request.GET.get('sNext'))
        slideshow = True
        current_picture = current_picture+1
        if current_picture > picture_count:
            current_picture = 1
    if 'cNext' in request.GET and request.GET.get('cNext'):
        current_picture = int(request.GET.get('cNext'))
        current_picture = current_picture+1
        if current_picture > picture_count:
            current_picture = 1
    elif 'cPrev' in request.GET and request.GET.get('cPrev'):
        current_picture = int(request.GET.get('cPrev'))
        if current_picture == 1:
            current_picture = picture_count
        else:
            current_picture=current_picture-1

    if picture_count and not slideshow:
        # slow
        print('B hey go get cc ss %s' % slideshow) 
        ccasts = chromecast.find_chrome_casts()


    if use_all:
        # all pictures view
        allow_tag = False
        picture = models.Picture.slide_objects.all().order_by(ob)[current_picture]
        title = ('All Pictures %d' % picture_count)
        filename = utility.object_path(picture)
    elif picture_count:
        allow_tag = False
        picture = pictures[current_picture-1]
        filename = utility.object_path(picture)
    
    # tags all objects
    if 'tq' in request.GET and request.GET['tq']:
        tq = request.GET['tq']
        tqSlug = slugify(str(tq))
        new_tag = collection.add_tag(tq,tqSlug)

        for obj in songs:
            obj.tags.add(new_tag)
        for obj in pictures:
            obj.tags.add(new_tag)
        for obj in movies:
            obj.tags.add(new_tag)

    # kodi playlist options
    try:
        if movies and kodi.playlist_requests(movies,request):
            message = u'success - movies sent'
        elif songs and kodi.playlist_requests(songs,request):
            message = u'success - songs sent'
        elif pictures and kodi.playlist_requests(pictures,request):
            message = u'success - pictures sent'

    except rutils.MyException as ex:
        message = ex.message
        print('Caught %s' % ex.message)

    context = {
        'title':title,
        'songlist':songs,
        'picture':picture,
        'pictureCount':picture_count,
        'filename': filename,
        'index': current_picture,
        'asPlayList': asPlayList,
        'movielist':movies,
        'update':update,
        'choices': choices.LIVE_CHOICES,
        'listkind':kind,
        'allowChoice': allowChoice,
        'artists': artists,
        'message': message,
        'allow_tag': allow_tag,
        'slideshow': slideshow,
        'ccasts':ccasts,
        'use_all':use_all
        }
    return render(request, template_name, context)


def movies_bykind(kind):
    """
    Given a kind, select only matching movie objects
    """
    movies = models.Movie.objects.filter(fileKind=kind)
    count = movies.count()
    for x,y in choices.LIVE_CHOICES:
        if x == kind:
            desc = y
            break
    title = ('%s: %d' % (desc, count))
    return movies, title


def view_list(request,alist,title,kind):
    template_name='FHLBuilder/collection_list.html'
    context = {
        'title':title,
        'clist': alist,
        'listkind':kind,
        'choices': choices.LIVE_CHOICES
        }
    return render(request,template_name,context)


def select_kind(request):
    """
    Given a GET request, select kind or default to movie
    """
    if 'kind' in request.GET and request.GET.get('kind'):
        kind = request.GET.get('kind')
    else:
        kind = choices.MOVIE
    return kind

