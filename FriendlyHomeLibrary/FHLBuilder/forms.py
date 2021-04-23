import os

from django import forms
from django.core.exceptions import ValidationError

from FHLBuilder import models, choices, utility
from FriendlyHomeLibrary import settings
#from FHLReader import chromecast

class CommonFileForm(forms.ModelForm):


    class Meta:
        model=models.CommonFile
        fields='__all__'
# seems like a good idea, but finding the list is painfully show
#    cast = forms.ChoiceField(choices = chromecast.find_chrome_casts(),
#        widget=forms.RadioSelect, label = 'Send to ChromeCast',
#        required=False)                
    pref = forms.ChoiceField(choices = choices.PREF_CHOICES,
        widget=forms.RadioSelect,
        initial=choices.INDIFFERENT)
    tag = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add tag')



class SongForm(CommonFileForm):
    class Meta:
        model=models.Song
        fields=['title','year']
    musician = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add musician')

class PictureForm(CommonFileForm):
    class Meta:
        model=models.Picture
        fields=['title','year']


class MovieForm(CommonFileForm):
    class Meta:
        model=models.Movie
        fields=['title','year','fileKind']
    actor = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add actor')
    director = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add director')        
    musician = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='add musician')

class TagForm(forms.ModelForm):
    class Meta:
        model=models.Tag
        fields=['name']
        
    def clean_name(self):
        return self.cleaned_data['name'].lower()
        
    def clean_slug(self):
        new_slug=(self.cleaned_data['slug'].lower())
        if(new_slug=='create'):
            raise ValidationError('Slug may not be "create".')
        return new_slug


class AllFilesForm(forms.ModelForm):
    class Meta:
        model=models.CommonFile
        fields=[]
    
    kind = forms.ChoiceField(choices = choices.LIVE_CHOICES,
        widget=forms.RadioSelect, label = 'Pick a kind',
        initial=choices.SONG)    

    order = forms.ChoiceField(choices = choices.ORDER_CHOICES,
        widget=forms.RadioSelect, label = 'Pick an Order',
        initial=choices.NAME)    

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')
    


class BasicCollectionForm(forms.ModelForm):
    class Meta:
        model=models.Collection
        fields=[]
    
    kind = forms.ChoiceField(choices = choices.VIDEO_CHOICES_FORM,
        widget=forms.RadioSelect, label = 'kind for videos',
        initial=choices.MOVIE)    
    
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)


class CollectionForm(forms.ModelForm):
    class Meta:
        model=models.Collection
        fields=['filePath']

    kind = forms.ChoiceField(choices = choices.VIDEO_CHOICES_FORM,
        widget=forms.RadioSelect, label = 'kind for videos',
        initial=choices.MOVIE)    
    
    # Used to add a tag to everything in the collection
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)
    drive = -1
    
    def clean_filePath(self):
        self.drive = -1
        new_path=self.cleaned_data['filePath']
        for i,drive in enumerate(settings.DRIVES,1):
            toCheck = os.path.join(settings.MY_MEDIA_FILES_ROOT,drive,new_path)
            utility.log("checking drive %d name %s path %s" % (i,drive,new_path))
            utility.log(toCheck)
            if os.path.exists(toCheck):
                self.drive=i
                utility.log("OK selecting drive %d" % i)
                break
        if self.drive > 0:
            a,b,last = new_path.rpartition('/')
            #print('last a %s b %s last %s' % (a,b,last))
            #print('new_path unchanged %s' % new_path)
            if len(last):
                final = str(new_path)
            else:
                final = str(new_path[:-1])
            if final[0]=='/':
                return final[1:]
            return final
            
        utility.log("DOES NOT EXIST")
        raise ValidationError(u'Path does not exist '+new_path,code=u'invalid')


class MusicianCleanupForm(forms.ModelForm):
    """
    Used to complete remove a musician and all albums songs
    """
    class Meta:
        model=models.Musician
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Musician.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick musician(s)')


class CollectionCleanupForm(forms.ModelForm):
    """
    Used to remove a collection and everything in it
    """
    class Meta:
        model=models.Collection
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Collection.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick collection(s)')


class DirectorCleanupForm(forms.ModelForm):
    """
    Used to remove a director (does not remove movies)
    """
    class Meta:
        model=models.Director
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Director.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick director(s)')


class ActorCleanupForm(forms.ModelForm):
    """
    Used to remove an actor (does not remove movies)
    """
    class Meta:
        model=models.Actor
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Actor.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick actor(s)')


class TagCleanupForm(forms.ModelForm):
    """
    Used to remove an actor (does not remove movies)
    """
    class Meta:
        model=models.Tag
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick tag(s)')


class PictureCleanupForm(forms.ModelForm):
    """
    Used to remove a picture
    """
    class Meta:
        model=models.Picture
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Picture.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick picture(s)')


class SongCleanupForm(forms.ModelForm):
    """
    Used to remove a song
    """
    class Meta:
        model=models.Song
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Song.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick song(s)')


class MovieCleanupForm(forms.ModelForm):
    """
    Used to remove a movie
    """
    class Meta:
        model=models.Movie
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick movie(s)')

