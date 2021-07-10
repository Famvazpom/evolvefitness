import os
import uuid
from django import template                                                                                                              
from django.utils.crypto import get_random_string

register = template.Library()                                                                                                            

@register.simple_tag(name='cache_bust')                                                                                                  
def cache_bust():                                                                                                                     
    return get_random_string(length=5)