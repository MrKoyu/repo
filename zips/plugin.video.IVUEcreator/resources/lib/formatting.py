import os, xbmc, xbmcgui, xbmcaddon,xbmcplugin,urllib
import re


path_to_ivue = xbmc.translatePath('special://profile/addon_data/script.ivueguide')
path_to_creator = xbmc.translatePath('special://profile/addon_data/plugin.video.IVUEcreator')


def message(message, title = 'Debug'):
    dialog = xbmcgui.Dialog()
    dialog.ok(title, message)

def strip_label(label):

    label = re.sub(r'\*', 'star', label)
    label = re.sub('[^A-Za-z0-9+!]+', ' ', label)
    label = re.sub('&amp;','',label)
    label = re.sub(' ', '', label)

    return label.lower()


def changenumbers(s):

    numbers = {'1' : 'one' ,'2' : 'two', '3' : 'three', '4':'four', '5' : 'five' ,'6' : 'six' ,
               '7' : 'seven', '8' : 'eight', '9':'nine', '10' : 'ten', '11':'eleven', '12' : 'twelve',}

    for src, target in numbers.iteritems():
        if src in s:
            s = s.replace(src, target)

    return s

def get_channel_names(channels_ini):

    names =  [line.rstrip('\n') for line in open(channels_ini)]

    return names

def get_clean_names(channels_ini):

    clean_names = {"clean_name": list(),
                   "stripped_name": list(),}

    clean_labels = get_channel_names(channels_ini)
    for clean_label in clean_labels:
        clean_names["clean_name"].append(clean_label)
        clean_names["stripped_name"].append(strip_label(clean_label))

    return clean_names


def clean_label(dirty_label, clean_names):

    orig_label = dirty_label
    stripped_label = strip_label(changenumbers(dirty_label))

    stripped_tags = ['uhd', 'hd', 'hq', ]

    stripped_label_tag, item_stripped = '',''

    for item in stripped_tags:

        if stripped_label[-len(item):] == item:
            stripped_label_tag = stripped_label[0:-len(item)]
            item_stripped = item

    for ii in range(0, len(clean_names["clean_name"])):

        cn_name = changenumbers(clean_names["stripped_name"][ii])

        if stripped_label == cn_name:
            return clean_names["clean_name"][ii]

        if stripped_label_tag is not '':

            if stripped_label_tag == cn_name:

                return clean_names["clean_name"][ii]+' '+item_stripped

    return orig_label


def remove_tags(label, formatting_referal = False):

    for rep in [r"\[/?[BI]\]", r"\[/?COLOR.*?\]",]:
        label = re.sub(rep, '', label)
    label = re.sub("\xa9", "c", label)
    label = re.sub("\xae", "r", label)

    if not formatting_referal:
        label = re.sub(r"[^A-Za-z0-9+!]+", ' ', label)

    return label


def remove_formatting(label, clean_names, id):

    for replace in ['facebook', 'twitter','updated','link','welcome','enter','latest','playlist','streams','beware','property',]:

        if replace in label.lower():
            return '<nolabel>'

    if id == 'plugin.video.ottalpha':

        label = label.split('-')

        if isinstance(label, list):
            label = label[0]

        label = remove_tags(label, True).lower().strip()

        parental_lock = xbmcaddon.Addon(id).getSetting("vanemalukk")
        if parental_lock == 'true':

            blacklist = ['xxx','adult','rissa','girl','ariadna','brasileirinhas','vod','demida','amanda','extinf','play korea',]

            for item in blacklist:

                if item in label:
                    return '<nolabel>'

            for ii in range(1,10):

                if label == str(ii):
                    return '<nolabel>'

        if label[0:3] == 'usa':
            label = label[3:]

    if id == 'plugin.video.xtream-codes':
        label = label.split(')')
        if isinstance(label, list):
            label = label[0]

    if id == 'plugin.video.gmgm':

        label = label.split('-')

        if isinstance(label, list):
            label = label[0]

    label = remove_tags(label, True)

    for replace in  [':','-','_',]:

        if len(label) > 3 and label.lower()[:1] is not 'bt' and label[:2] == replace:
            label = label.split(replace,1)[1]

    replace = ["usa/ca",
               "local",
               "sports uk english",
               "movie channels",
               "uk english",
               "us english",
               "uk english",
               "english",
               'london',
               "skyuk",
               'ccloudtv.org',
               'test',
               'sd',
               'entertainment',]

    for rep in replace:
        label =  label.lower().replace(rep, '')

    label = re.sub(r'\(.*?\)', '', label.lower())
    label = re.sub(r'\*', 'star', label)
    label = re.sub('[^A-Za-z0-9+!]+', ' ', label)

    replace = ['usa','us','uk',]
    for rep in replace:
        if label[0:len(rep)] == rep:
            label = label[len(rep):]

    label = label.strip()
    label = re.sub('bt sports', 'bt sport', label.lower())

    if "sky" in label.lower():

        items = ['disney',
                 'action',
                 'family',
                 'scifi and horror',
                 'premiere',
                 'comedy',
                 'select',
                 'showcase',
                 'thriller',
                 'greats',
                 'drama',]

        for item in items:
            if item in label:
                label = 'sky cinema ' + item

        label = label.strip().lower()
        label = re.sub('movies', 'cinema', label)
        label = re.sub('sport ', 'sports', label)

    cl_label = clean_label(label, clean_names)

    if len(cl_label) < 1:
        return '<nolabel>'
    else:#aftercare for non matched channels
        cl_label = re.sub('uhq', 'UHQ', cl_label)
        cl_label = re.sub('hq', 'HQ', cl_label)
        cl_label = re.sub('hd', 'HD',cl_label)

        if 'bbc' in cl_label:

            cl_label = re.sub('bbc', 'BBC', cl_label)
            cl_label = changenumbers(cl_label)

        if cl_label == 'itv':
            cl_label = 'itv1'
        cl_label = re.sub('itv', 'ITV', cl_label)

        return cl_label



