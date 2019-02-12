# -*- coding: UTF-8 -*-
'''
    Updated and refactored by someone.
    Originally created by others.
'''
# Addon Name: MTB
# Addon id: plugin.video.movietheaterbutter
# Addon Provider: SomeBody

from resources.lib.modules import control, log_utils

try:
    import resolveurl

    debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(
        order_matters=True) if resolver.isUniversal()]

    if len(debrid_resolvers) == 0:
        # Support Rapidgator accounts! Unfortunately, `sources.py` assumes that rapidgator.net is only ever
        # accessed via a debrid service, so we add rapidgator as a debrid resolver and everything just works.
        # As a bonus(?), rapidgator links will be highlighted just like actual debrid links
        debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(
            order_matters=True, include_universal=False) if 'rapidgator.net' in resolver.domains]

except Exception:
    debrid_resolvers = []


def status(torrent=False):
    debrid_check = debrid_resolvers != []
    if debrid_check is True:
        if torrent:
            enabled = control.setting('torrent.enabled')
            if enabled == '' or enabled.lower() == 'true':
                return True
            else:
                return False
    return debrid_check


def resolver(url, debrid):
    try:
        debrid_resolver = [resolver for resolver in debrid_resolvers if resolver.name == debrid][0]
        debrid_resolver.login()
        _host, _media_id = debrid_resolver.get_host_and_id(url)
        stream_url = debrid_resolver.get_media_url(_host, _media_id)

        return stream_url
    except Exception as e:
        log_utils.log('%s Resolve Failure: %s' % (debrid, e), log_utils.LOGWARNING)
        return None
