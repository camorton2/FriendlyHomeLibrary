
from FHLBuilder import choices


# used to select person
people = ['actor','director','musician']
st = '|'.join(x for x in people)
artist = unicode(r'^artist/(%s)$' % st)

# used to select list order
ot = '|'.join(x for x in choices.ordering)
#sorder = unicode(r'^files/(%s)$' % ot)

# select all files view
lv = '|'.join(x1 for x1 in choices.live)
sorder = unicode(r'^files/(%s)/(%s)$' % (lv,ot))


liked = 'liked'
loved = 'loved'
both = 'both'
random = 'random'

# used to select by video kind
v = '|'.join(x for x in choices.videos)
vchannel = unicode(r'^channel/(%s)$' % v)

# used to select channel
special = ['sitcom','saturday-morning','silly','scifi','drama','scary']
st = '|'.join(x for x in special)
schannel = unicode(r'^channel/(%s)$' % st)


