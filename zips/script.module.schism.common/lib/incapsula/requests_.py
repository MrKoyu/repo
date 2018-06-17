import random
import time

import requests
from BeautifulSoup import BeautifulSoup

from methods import *
from config import endpoints

logger = logging.getLogger('incapsula')


def _load_encapsula_resource(sess, response):
    timing = []
    start = now_in_seconds()
    timing.append('s:{0}'.format(now_in_seconds() - start))

    code = get_obfuscated_code(response.content)
    parsed = parse_obfuscated_code(code)
    resource1, resource2 = get_resources(parsed, response.url)[1:]
    sess.get(resource1)

    timing.append('c:{0}'.format(now_in_seconds() - start))
    time.sleep(0.02)  # simulate page refresh time
    timing.append('r:{0}'.format(now_in_seconds() - start))
    sess.get(resource2 + urllib.quote('complete ({0})'.format(",".join(timing))))


def crack(sess, response):
    """
    Pass a response object to this method to retry the url after the incapsula cookies have been set.

    Usage:
        >>> import incapsula
        >>> import requests
        >>> session = requests.Session()
        >>> response = incapsula.crack(session, session.get('http://www.incapsula-blocked-resource.com'))
        >>> print response.content  # response content should be incapsula free.
    :param sess: A requests.Session object.
    :param response: The response object from an incapsula blocked website.
    :return: Original response if not blocked, or new response after unblocked
    :type sess: requests.Session
    :type response: requests.Response
    :rtype: requests.Response
    """
    soup = BeautifulSoup(response.content)
    meta = soup.find('meta', {'name': re.compile('robots', re.IGNORECASE)})
    if not meta:  # if the page is not blocked, then just return the original request.
        return response
    set_incap_cookie(sess, response)
    # populate first round cookies
    scheme, host = urlparse.urlsplit(response.url)[:2]
    #logger.debug('scheme={} host={}'.format(scheme, host))
    # Check if the host is in pre-configured incapsula endpoints
    # If it is, use the pre-configured endpoint to get the obfuscated code,
    # otherwise use the default resource
    if host in endpoints:
        params = endpoints.get(host, {'SWKMTFSR': '1', 'e': random.random()})
        url_params = urllib.urlencode(params)
        #logger.debug('url_params={}'.format(url_params))
        r = sess.get('{scheme}://{host}/_IncapsulaResource?{url_params}'.format(scheme=scheme, host=host, url_params=url_params), headers={'Referer': response.url})
        _load_encapsula_resource(sess, r)
    else:
        sess.get('{scheme}://{host}/_Incapsula_Resource?SWKMTFSR=1&e={rdm}'.format(scheme=scheme, host=host, rdm=random.random()), headers={'Referer': response.url})
        _load_encapsula_resource(sess, response)

    return sess.get(response.url)


def _get_session_cookies(sess):
    cookies_ = []
    for cookie_key, cookie_value in sess.cookies.items():
        if 'incap_ses_' in cookie_key:
            cookies_.append(cookie_value)
    return cookies_


def set_incap_cookie(sess, response):
    logger.debug('loading encapsula extensions and plugins')
    extensions = load_plugin_extensions(navigator['plugins'])
    extensions.append(load_plugin(navigator['plugins']))
    extensions.extend(load_config())
    cookies = _get_session_cookies(sess)
    digests = []
    for cookie in cookies:
        digests.append(simple_digest(",".join(extensions) + cookie))
    res = ",".join(extensions) + ",digest=" + ",".join(str(digests))
    cookie = create_cookie("___utmvc", res, 20, response.url)
    sess.cookies.set(**cookie)


class IncapSession(requests.Session):
    """
    requests.Session subclass to wrap all get requests with incapsula.crack.
    """

    def get(self, url, **kwargs):
        """Sends a GET request wrapped with incapsula.crack. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        kwargs.setdefault('allow_redirects', True)
        r = self.request('GET', url, **kwargs)
        return crack(self, r)
