# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

admin.site.register(UserModel)
admin.site.register(PostModel)
admin.site.register(SessionToken)
admin.site.register(CommentModel)
admin.site.register(LikeModel)