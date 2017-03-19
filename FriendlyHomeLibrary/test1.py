#!/usr/bin/env python
import os
import sys
from FHLBuilder.models import Tag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FriendlyHomeLibrary.settings")

t1 = Tag(name='test',slug='test')
t1
