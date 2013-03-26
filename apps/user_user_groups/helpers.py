from settings import THISAPP
from urls import URLS_THISAPP

from django.shortcuts import render

import os.path

def url_add_app(url_noapp):
    """given a url name without app preffix, returns it with the app prefix

    the app prefix is taken from settings.THISAPP
    
    >>> url_noapp('asdf')
    thisapp_adsf
    """
    return THISAPP + '_' + url_noapp

def template_add_app(template_noapp):
    """given a template without app preffix, returns it with the app prefix

    the app prefix is taken from settings.THISAPP
    
    >>> url_noapp('asdf')
    thisapp/adsf.html
    """
    return os.path.join(THISAPP, template_noapp+'.html')

def render_appcontext(template_noapp):
    """given a template without app preffix, returns it with the app prefix

    the app prefix is taken from settings.THISAPP
    
    >>> url_noapp('asdf')
    thisapp/adsf.html
    """
    return THISAPP + '_' + url_noapp

def render_thisapp(
            request,
            template_noapp,
            context={},
            url_context_name='urls_thisapp',
            *args,**kwargs
        ):
    """django.shortcuts.render wrapper to factor out app stuff

    it modifies the args passed as:

    1) template that will be passed to django render is first transformed by
        template_noapp_to_app
    2) urls.URLS_THISAPP is added to context as a variable.
        the name of this variable is :url_context_name:
    """
    context.update({url_context_name:URLS_THISAPP})
    return render(
        request,
        template_add_app(template_noapp),
        context,
        *args,
        **kwargs
    )

