import datetime

from django import forms
from django.core.exceptions import ValidationError

from FHLBuilder import models, choices

class RandomForm(forms.ModelForm):
    """
    The idea is to allow the user to create a list of count
    random objects matching a kind and/or tag
    For songs, a playlist can be created in html
    but the ultimate goal is to create a playlist for kodi
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    kind = forms.ChoiceField(choices = choices.LIVE_CHOICES,
        widget=forms.RadioSelect, label = 'Pick a kind',
        initial=choices.MOVIE)
    tag = forms.CharField(max_length=models.CHAR_LENGTH,required=False)
    
    atitle = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='title contains')
    
    count = forms.IntegerField(initial=15, label='How many would you like')

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class RecentForm(forms.ModelForm):
    """
    The idea is to allow the user to create a list of count
    most recent objects matching a kind and/or tag
    For songs, a playlist can be created in html
    but the ultimate goal is to create a playlist for kodi
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    kind = forms.ChoiceField(choices = choices.LIVE_CHOICES,
        widget=forms.RadioSelect, label = 'Pick a kind',
        initial=choices.MOVIE)
        
    count = forms.IntegerField(initial=15, label='How many would you like')

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class CountForm(forms.ModelForm):
    """
    Used for specialty channels to get only a count, the rest is
    selected automatically
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    count = forms.IntegerField(initial=15, label='How many would you like')

    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class RadioForm(forms.ModelForm):
    """
    Used for radio stations which pick random songs based on 
    selected users
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    count = forms.IntegerField(initial=40, label='How many would you like')
    kind = forms.ChoiceField(choices = choices.RADIO_CHOICES,
        widget=forms.RadioSelect,
        initial=choices.ALL,label = 'who is listening')
    xmas = forms.BooleanField(label = 'include Christmas', 
        initial=False,required=False)
    classic = forms.BooleanField(label = 'include classical', 
        initial=False,required=False)        
    recent = forms.BooleanField(label = 'select only recent', 
        initial=True,required=False)
        
    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')


class MusicianRadioForm(forms.ModelForm):
    """
    Used for radio stations which pick songs based on 
    selected musicians
    """
    class Meta:
        model=models.Musician
        fields=[]
     
    xmas = forms.BooleanField(label = 'include Christmas', 
        initial=False,required=False)
        
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Musician.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick musician(s)')


class CollectionRadioForm(forms.ModelForm):
    """
    Used for radio stations which pick songs based on selected 
    collections
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    xmas = forms.BooleanField(label = 'include Christmas', 
        initial=False,required=False)
        
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Collection.song_objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick collection(s)')


class SongRadioForm(forms.ModelForm):
    """
    Used for radio stations which pick songs based on selected 
    songs
    """
    class Meta:
        model=models.Song
        fields=[]
             
    choices = forms.ModelMultipleChoiceField(
        queryset=models.Song.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        label = 'Pick song(s)')
    
    

class MovieChannelForm(forms.ModelForm):
    """
    The idea is to allow the user to create a playlist of count
    random items, optionally matching by tag or title
    """
    class Meta:
        model=models.Collection
        fields=[]
     
    atitle = forms.CharField(max_length=models.CHAR_LENGTH,
        required=False,
        label='title contains')
    atag = forms.CharField(max_length=models.CHAR_LENGTH,required=False,
        label='with tag')
    count = forms.IntegerField(initial=15)

    random = forms.BooleanField(label = 'random? ', 
        initial=False,required=False)


    def clean_count(self):
        count=self.cleaned_data['count']
        if count > 0:
            return count
        raise ValidationError(u'please select a count above 0')



class DateAddedForm(forms.ModelForm):
    """
    The idea is to allow the user to create a playlist
    based on a year and optional month
    """
    class Meta:
        model=models.Song
        fields=[]
     
    yearA = forms.IntegerField(initial=datetime.date.today().year, 
        required=True,label='Starting Year')
        
    monthA = forms.ChoiceField(choices = choices.MONTH_CHOICES,
        label = 'Starting Month (optional)',
        initial=choices.SKIP, required = False)

    yearB = forms.IntegerField(initial=0, 
        required=False,label='To Year (optional)')
        
    monthB = forms.ChoiceField(choices = choices.MONTH_CHOICES,
        label = 'To Month (optional)',
        initial=choices.SKIP, required = False)

    random = forms.BooleanField(label = 'random? ', 
        initial=False,required=False)


    def check_year(self,year):
        try:
            iyear = int(year)
        except:
            raise ValidationError(u'Invalid Year')
        if iyear > 1999 and iyear <= datetime.date.today().year:
            return year
        elif iyear == 0:
            return year
        raise ValidationError(u'please select a year since 2000')

    def check_month(self,month):
        try:
            imonth = int(month)
            print('month %d' % imonth)
        except ValueError:
            raise ValidationError(u'Invalid Month')
        if imonth >=0  and imonth <= 12:
            return month
        raise ValidationError(u'Invalid Month')

    def clean_yearA(self):
        year=self.cleaned_data['yearA']
        return self.check_year(year)

    def clean_monthA(self):
        month=self.cleaned_data['monthA']
        return self.check_month(month)
        
    def clean_yearB(self):
        year=self.cleaned_data['yearB']
        return self.check_year(year)

    def clean_monthB(self):
        month=self.cleaned_data['monthB']
        return self.check_month(month)
        
    def clean(self):
        try:
            # required
            ya = int(self.cleaned_data['yearA'])
            yb = 0
            ma = 0
            mb = 0
            # optional
            if 'yearB' in self.cleaned_data:
                yb = int(self.cleaned_data['yearB'])
            if 'monthA' in self.cleaned_data:
                ma = int(self.cleaned_data['monthA'])
            if 'monthB' in self.cleaned_data:
                mb = int(self.cleaned_data['monthB'])
                
        except ValueError:
            raise ValidationError(u'Invalid Year')
            
        print('yearA %d yearB %d' % (ya,yb))
        if ya and yb:
            if ya > yb:
                raise ValidationError(u'Years are not consecutive')
            if ma and mb:
                pass
            elif ma or mb:
                raise ValidationError(u'Specify no months or both')
            

class DateAddedRadioForm(DateAddedForm):
    xmas = forms.BooleanField(label = 'include Christmas', 
        initial=False,required=False)

    playback = forms.ChoiceField(choices = choices.SONGPLAY_CHOICES,
        label = 'Playback',
        initial=choices.WEB, required = False)



class DateAddedPictureForm(DateAddedForm):
    thumb = forms.BooleanField(label = 'include Thumbnails', 
        initial=False,required=False)

    smut = forms.BooleanField(label = 'include Smut', 
        initial=False,required=False)

    playback = forms.ChoiceField(choices = choices.PICTUREPLAY_CHOICES,
        label = 'SlideShow',
        initial=choices.FLIST, required = False)

