from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ..models import Menu

register = template.Library()


@register.inclusion_tag("auto_menu/menu.html", takes_context=True)
def draw_menu(context, name_menu):
    all_point = Menu.objects.filter(menu_name=name_menu)
    slug = context.request.GET
    return None
