#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       htmljukebox.py
#
#       Authors:
#           Felipe Nogaroto Gonzalez
#           Thiago Coutinho
#
#       http://jukebox.bunghole.com.br - jukebox@bunghole.com.br
#       Copyright 2008
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
from index import *

def htmlheader(config):

    album_view = config.dict['album_view']
    carousel_includes = ''
    if album_view == 'carousel':
        carousel_includes = '''
        <link rel="stylesheet" type="text/css" href="/jukebox/carousel/carousel.css" />
        <script type="text/javascript" src="/jukebox/carousel/jMyCarousel.js"></script>
        <script type="text/javascript">
          $(function() {
            $(".jMyCarousel").jMyCarousel({
              visible: 5,
              eltByElt: false,
              speed: 100,
              circular: false
            });
          });
        </script>
        '''

    print 'Content-Type: text/html\n\n'

    print '''
<html>
    <head>
        <title>Bunghole Jukebox</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link type="text/css" rel="stylesheet" href="/jukebox/themes/%s/style.css">
        <script type="text/javascript" src="/jukebox/themes/reflex.js"></script>
        <script type="text/javascript" src="/jukebox/carousel/jquery-1.2.1.pack.js"></script>
        <!-- script type="text/javascript" src="/jukebox/themes/selectchangeorder.js"></script -->
        <!--[if lt IE 7]>
            <script defer type="text/javascript" src="/jukebox/themes/pngfix.js"></script>
        <![endif]-->
        %s
        <script type="text/javascript">
        $(function() {
        $('[@name=flash_player]').click(function() { if(this.value == 'enable') { $('#url_music').show() } else { $('#url_music').hide() }})
        })
        </script>
    </head>
    <body>
        <a href="?p=about" >
            <img title="Bunghole Jukebox" src="/jukebox/images/bunghole_jukebox.png" width="240" class="logo" />
        </a>
        <div class="top">
            <div class="letters"><a href="?p=artist&s=0">#</a>''' % (config.dict['theme'], carousel_includes)

    for letter in map(chr, range(65, 91)):
        print '|&nbsp;<a href="?p=artist&s=%s">%s</a>' % (letter, letter)

    print '''
            </div>
            <div class="menu">
                <a class="iconopacity" href="?p=settings" title="Settings"><img src="/jukebox/images/icons/settings.png"></a>&nbsp;
                <a class="iconopacity" href="?p=log" title="Log"><img src="/jukebox/images/icons/log.png"></a>&nbsp;
                <a class="iconopacity" href="?p=about" title="About"><img src="/jukebox/images/icons/about.png"></a><br /><br />
                <form method='get' action=''>
                    <input type='hidden' name='p' value='search' />
                    <div class="search">
                        <input type="text" size="10" name="q" value="Search by ..." onfocus='this.value=""' onblur='if(this.value==""){this.value="Search by ..."}' class="search_input" />
                        <input type="reset" value="&nbsp;" style="border:0; background: url(/jukebox/images/search_x.jpg) no-repeat; margin-right: 7px; margin-top: 4px; width: 15" />
                    </div>&nbsp;
                    <select name='t'>
                        <option value='artist'>artist</option>
                        <option value='album'>album</option>
                        <option value='music'>music</option>
                        <option value='year'>year</option>
                        <option value='genre'>genre</option>
                    </select>&nbsp;
                    <input type="submit" value="Go" />
                </form>
            </div>
            </div>'''

def htmlfooter():
    print '<div class="footer">Bunghole Jukebox \m/</div></body></html>'

def htmlindex(stats=[], total_size=[], total_time=[]):
    print '''
            <div class="title">
                <a href="?">
                    <img title="Home" border="0" src="/jukebox/images/icons/home.png">
                </a>
            </div>
            <div class="main">
                Some statistics about your mp3 colection: <br />
                Total of artists: %i <br />
                Total of albums: %i <br />
                Total of musics: %i <br />
                Total of size: %s <br />
                Total of time: %s <br />
            </div>''' % (stats[0], stats[1], stats[2], format_size(total_size), format_time(total_time))

def htmlabout():
    print '''
            <div class="title">
                <a href="?">
                    <img title="Home" border="0" src="/jukebox/images/icons/home.png">
                </a>
            </div>
            <div class="main">
                <h2>About</h2>
                <hr />
                <div align="center">
                    <br /><br />
                    <a href="http://jukebox.bunghole.com.br" target="_blank" title="Bunghole Jukebox">
                    <img src="/jukebox/images/bunghole_jukebox.png" border="0" /><br />http://jukebox.bunghole.com.br</a><br />
                        <p>Bunghole Jukebox is a web interface to your MP3 collection.<br>
                        Use it to access your music collection wherever you are,<br>
                        publish in your website/blog and share with friends.<br>
                        You will can show your collection for anybody, from anywhere.</p>
                </div>
                <br /><br /><br /><br /><br />Authors:<br />
                <a href="http://felipe.bunghole.com.br" target="_blank">Felipe Nogaroto Gonzalez</a><br />
                <a href="http://thiago.bunghole.com.br" target="_blank">Thiago Coutinho</a><br /><br />
                <a href="http://jukebox.bunghole.com.br" target="_blank">Bunghole Jukebox</a> it's another product of the organization
                <a href="http://www.bunghole.com.br" target="_blank">Bunghole S/A</a>.
            </div>'''


def htmllog(log, type):

    # MELHORAR A LOGICA - string vazia
    if type != 'success' and type != 'notag' and type != 'notmp3':
        divmain = "main"
    else:
        divmain = "main_auto"

    i = 0
    count_success = 0
    count_notag = 0
    count_notmp3 = 0

    for lines in log:
        if lines.startswith('/'):
           count_success += i + 1
        if lines.startswith('(NOTAG)'):
           count_notag += i + 1
        if lines.startswith('(NOTMP3)'):
           count_notmp3 += i + 1


    print '''<div class="title">
                <a href="?">
                    <img title="Home" border="0" src="/jukebox/images/icons/home.png">
                </a>
            </div>
            <div class="%s">
            <h2>Log</h2><hr />
            <p>Select a specific log for more information.</p>
            <table align="center" style="text-align: center;">
                <tr>
                    <td><a class="iconopacity" href="?p=log&view=success"><img src="/jukebox/images/icons/success.png" alt="Success" title="Success" /> success (%s)</a></td>
                    <td><a class="iconopacity" href="?p=log&view=notag"><img src="/jukebox/images/icons/notag.png" alt="NoTag" title="NoTag" /> notag (%s)</a></td>
                    <td><a class="iconopacity" href="?p=log&view=notmp3"><img src="/jukebox/images/icons/notmp3.png" alt="Not Mp3" title="Not Mp3" /> notmp3 (%s)</a></td>
                    </td>
                <tr>
                    <td class="comment" width="170">added to database with success</td>
                    <td class="comment" width="170">invalid or without some ID3 TAG</td>
                    <td class="comment" width="170">file is not a .mp3 file</td>
                    </td>
                </tr>
            </table><br />''' % (divmain, count_success, count_notag, count_notmp3)

    for lines in log:
        if type == 'success':
            if not lines.startswith('(NOTAG)') and not lines.startswith('(NOTMP3)'):
                print lines + '<br />'
        elif type == 'notag':
            if lines.startswith('(NOTAG)'):
                print lines + '<br />'
        elif type == 'notmp3':
            if lines.startswith('(NOTMP3)'):
                print lines + '<br />'
    print '</div>'

def htmlsettings(config):
    size = config.dict['cover_size']
#    cover_mask = config.dict['cover_mask']
    album_view = config.dict['album_view']
    flash_player = config.dict['flash_player']
    url_music = config.dict['url_music']
    mp3_dir = config.dict['mp3_dir']

    if url_music == "":
        url_music = 'http://' + os.environ.get('HTTP_HOST') + "/jukebox/music"

    options_theme = ''
    for theme in config.dict['themes']:
        options_theme += '<option value="%s">%s</option>' % tuple([theme] * 2)

    options_view = ''
    if album_view == 'carousel':
        options_view += '<input type="radio" name="album_view" value="carousel" checked>Carousel'
        options_view += '<input type="radio" name="album_view" value="list">List'
    if album_view == 'list':
        options_view += '<input type="radio" name="album_view" value="carousel">Carousel'
        options_view += '<input type="radio" name="album_view" value="list" checked>List'

    options_player = ''
    if flash_player == 'enable':
        options_player += '<input type="radio" name="flash_player" value="enable" checked>Enable'
        options_player += '<input type="radio" name="flash_player" value="disable">Disable'
    if flash_player == 'disable':
        options_player += '<input type="radio" name="flash_player" value="enable">Enable'
        options_player += '<input type="radio" name="flash_player" value="disable" checked>Disable'

#    options_mask = ''
#    for mask in cover_mask:
#        options_mask += '<option label="%s" value="%s">%s</option>' % tuple([mask] * 3)

    print '''<div class="title">
                <a href="?">
                    <img title="Home" border="0" src="/jukebox/images/icons/home.png">
                </a>
            </div>
             <div class="main">
                <h2>Settings</h2>
                <hr />
                <form action="index.py" method="get">
                <!-- form action="index.py" method="get" onsubmit="$('#selectb option').each(function() {$(this).attr('selected', 'selected')});" -->
                    <h3>Flash Player</h3>
                    %s
                    </p>
                    <div id="url_music" style="display: none;">URL Music:
                        <input type="text" size="60" id="url_music" name="url_music" value="%s" /><br /></div>
                    <h3>Apparence</h3>
                    <p>Theme:
                        <select id="theme" name="theme" value="%s" />
                        %s
                        </select>
                    <p>Albums View:
                        %s
                    <h3>Database</h3>
                    <p>Cover Size:
                        <input type="text" size="3" id="cover_x" value="%s" name="cover_size" /> x
                        <input type="text" size="3" id="cover_y" value="%s" name="cover_size" /> px</p>
                    <!-- p>Warning to create database. Database will never be updated, always will be deleted and created again, including cache of the covers. -->
                     <p>MP3 Directory:
                        <input type="text" size="60" id="path" name="mp3_dir" value="%s"/>&nbsp;<input type="button" value="create" onclick='$.post("?", {path: $("#path").val()});' />
                    <!-- p>Cover Mask: <br />
                        <select id="selectb" name="selectb" size="5" multiple="" />
                            s
                        </select>
                        <p><input type="button" value="up" onClick="move(this.form,this.form.selectb,-1)"> | 
                        <input type="button" value="down" onClick="move(this.form,this.form.selectb,+1)"></p -->
                    <p>

                    <input type="hidden" name="p" value="settings" />
                    <input type="hidden" name="a" value="save" />
                    <input type="reset" value="default" />
                    <input type="submit" value="save" />
                </form>
            </div>''' % (options_player, url_music, theme, options_theme, options_view, size[0], size[1], mp3_dir)


def htmlartists(artists=[], letter_stats=[], letter=[], stats=[]):
    if letter == '0':
        letter = '#'

    col1 = ""
    col2 = ""
    col3 = ""
    resto = ""
    n = 0
    for artist in artists:
        n += 1
        if n < 26:
            col1 += '<a href="?p=album&artist=%s">%s</a><br />' % (artist['id'], artist['name'])
        elif n < 56:
            col2 += '<a href="?p=album&artist=%s">%s</a><br />' % (artist['id'], artist['name'])
        elif n < 85:
            col3 += '<a href="?p=album&artist=%s">%s</a><br />' % (artist['id'], artist['name'])
        else:
            resto += '<a href="?p=album&artist=%s">%s</a><br />' % (artist['id'], artist['name'])

    print '''
            <div class="title">
                <div class="title_path">
                    <a href="?"><img title="Home" border="0" src="/jukebox/images/icons/home.png"></a>
                </div>
                <div class="stats">
                    %i artists - %i albums - %i musics
                </div>
            </div>
            <div class="main">
                <div style="float: left; width: 32%%;">
                <h2>%s</h2><hr /><br />%s</div>
                <div style="float: left; width: 32%%;">%s</div>
                <div style="float: left; width: 32%%;">%s</div>
                %s
                </div>''' % (letter_stats[0], letter_stats[1], letter_stats[2], letter, col1, col2, col3, resto)


def htmlalbums(config, albums, stats=[]):
    html_path = config.dict['html_path']
    album_view = config.dict['album_view']

    print '''
            <div class="title">
                <div class="title_path">
                    <a href="?"><img title="Home" border="0" src="/jukebox/images/icons/home.png"></a> > %s
                </div>
                <!-- div class="stats">
                    %i artists - %i albums - %i musics
                </div -->
            </div>''' %  (albums[0]['artist_name'], stats[0], stats[1], stats[2])

    if album_view == 'carousel':
        print '<div class="main"> <h2>%s</h2><hr />' % albums[0]['artist_name']
        carousel = False
        if len(albums) > 5:
            carousel = True
            print '<div class="jMyCarousel" style="margin-top: 5%; margin-left: 20%"><ul>'
        else:
            print '<div style="text-align: center; margin-top: 5%;">'
        for album in albums:
            if os.path.exists('%s/cache/%.4i.jpg' % (config.dict['html_path'], int(album['id']))):
                img = '/jukebox/cache/%.4i.jpg' % int(album['id'])
            else:
                img = "/jukebox/images/nocover.jpg"
            if carousel:
                print '<li><a href="?p=music&album=%s" title="%s - %s" class="thickbox">\
                <img src="%s" style="width: 137px; height: 124px;" /></a></li>'\
                % (album['id'], album['year'], album['name'], img)
            else:
                print '''<a href="?p=music&album=%s" title="%s - %s">
                            <img src="%s" style="border: 1px solid #d8d8d8; padding: 3px; 137px; height: 124px;" /></a>''' \
                        % (album['id'], album['year'], album['name'], img)
        print '</ul></div>'

    elif album_view == 'list':
        print '<div class="main_auto"> <h2>%s</h2><hr /><br /><table align="center" style="width: 80%%;">' % albums[0]['artist_name']
        for album in albums:
            if os.path.exists('%s/cache/%.4i.jpg' % (config.dict['html_path'], int(album['id']))):
                img = '/jukebox/cache/%.4i.jpg' % int(album['id'])
            else:
                img = "/jukebox/images/nocover.jpg"
            print '''<tr><td style="text-align: center; width: 130px;">
                     <a href="?p=music&album=%s">
                        <img title="%s - %s" src="%s" style="border: 1px solid #d8d8d8; padding: 3px; 137px; height: 124px;" />
                     </a><br />%s (%s)</td><td>''' \
                     % (album['id'], album['year'], album['name'], img, album['name'], album['year'])

            ix = 0
            musics = get_all_musics(int(album['id']))
            print '<table cellspacing="0" cellpadding="2" style="width: 100%">'
            for music in musics:
                ix += 1
                zebra = 'zebra1'
                if ix % 2 == 0:
                    zebra = 'zebra2'
                print '''<tr class="%s">
                            <td width="1">%s</td>
                            <td style="width: 50%%; text-align: left;">%s</td>
                            <td class="tabrow">%s kbps</td>
                            <td class="tabrow">%s</td>
                            <td class="tabrow">%s</td>
                        </tr>''' \
                % (zebra, music['track'], music['name'], (int(music['bitrate']) / 1000),\
                str(format_time(music['length'])), format_size(music['size']))
            print '</table></td><tr><td>&nbsp;</td></tr>'
        print '</tr></table>'
    print '</div>'

def htmlmusics(config, musics, stats=[]):
    stasts = ""
    if musics[0]['album_id'] == 666:
        stasts = "(Album possessed by devil)"

    if os.path.exists('%s/cache/%.4i.jpg' % (config.dict['html_path'], int(musics[0]['album_id']))):
            img = '/jukebox/cache/%.4i.jpg' % int(musics[0]['album_id'])
    else:
            img = "/jukebox/images/nocover.jpg"

    print '''
            <div class="title">
                <div class="title_path">
                    <a href="?"><img title="Home" border="0" src="/jukebox/images/icons/home.png"></a> > <a href="?p=album&artist=%s">%s</a> > %s - %s <font color=red>%s</font>
                </div>
                <!-- div class="stats">
                    %i artists - %i albums - %i musics
                </div -->
            </div>
            <div class="main_auto">
            <table align="center" style="width: 95%%">
                <tr>
                    <td style="vertical-align: top; padding: 10px; width: 20%%">
                        <img src="%s" width="300px" class="reflex iopacity50" />
                    </td>
                    <td style="vertical-align: top; padding: 20px;">
                        <table cellspacing="0" cellpadding="2" align="center" width="100%%">''' \
                % (musics[0]['artist_id'], musics[0]['artist_name'], musics[0]['album_year'], musics[0]['album_name'], \
                   stasts, stats[0], stats[1], stats[2], img)

    if config.dict['flash_player'] == "enable":
        import urllib
        playlist = '''<?xml version="1.0" encoding="UTF-8"?>\n<playlist version="0" xmlns = "http://xspf.org/ns/0/">\n<trackList>\n'''
        for music in musics:
            music_file = urllib.pathname2url(music['path'].encode('utf-8'))
            playlist += '''<track><location>%s%s</location><title>%s</title><duration>%s</duration><image>/jukebox/cache/%.4i.jpg</image></track>\n''' % (config.dict['url_music'], music_file, music['name'], str(format_time(music['length'])), int(musics[0]['album_id']))
        playlist += '''</trackList>\n</playlist>\n'''

        file = open('../html/jukebox/player/playlist.xml', 'w')
        file.write(playlist)
        file.close()

        print '''<div>
                   <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="600" height="340" align="middle">
                        <embed src="/jukebox/player/xspf_jukebox.swf?skin_url=/jukebox/player/Bunghole&loadurl=/jukebox/player/variables.txt" wmode="transparent"
                        width="600" height="340" align="middle" type="application/x-shockwave-flash" zpluginspage="http://www.macromedia.com/go/getflashplayer" quality="high"style="margin-left: auto; margin-right: auto; display: block;"/>
                    </object>
                </div>'''

    else:
        total_time = 0
        total_size = 0

        ix = 0
        for music in musics:
            ix += 1
            total_time += music['length']
            total_size += music['size']
            zebra = 'zebra1'
            if ix % 2 == 0:
                zebra = 'zebra2'
    
            print '''<tr class="%s">
                        <td width="1px">%s</td>
                        <td style="width: 50%%; text-align: left;">%s</td>
                        <td class="tabrow">%s kbps</td>
                        <td class="tabrow">%s</td>
                        <td class="tabrow">%s</td>
                    </tr>''' \
            % (zebra, music['track'], music['name'], (int(music['bitrate']) / 1000),\
            str(format_time(music['length'])), format_size(music['size']))

        print '''<tr class="zebra_total">
                    <td colspan="3" style="text-align: left;">Total</td>
                    <td class="tabrow">%s</td>
                    <td class="tabrow">%s</td>
                </tr>''' % (format_time(total_time), format_size(total_size))
    print '''</table></td></tr></table></div>'''

def htmlsearch(artists=[], albums=[], musics=[], stats=[], years=[], genres=[]):

    print '''<div class="title">
                <div class="title_path">
                    <a href="?">
                        <img title="Home" border="0" src="/jukebox/images/icons/home.png">
                    </a>
                </div>
                <!-- div class="stats">
                    %i artistss - %i albums - %i musics
                </div -->
            </div>
            <div class="main_auto">''' % (stats[0], stats[1], stats[2])

    for artist in artists:
        print '<a href="?p=album&artist=%s">%s</a><br />' % (artist['id'], artist['name'])

    for album in albums:
        print '<a href="?p=album&artist=%s">%s</a> > <a href="?p=music&album=%s">%s</a><br />' % (album[0], album[1], album[2], album[3])

    for year in years:
        print '<a href="?p=album&artist=%s">%s</a> > <a href="?p=music&album=%s">%s</a><br />' % (year[0], year[1], year[2], year[3])

    for genre in genres:
        print '<a href="?p=album&artist=%s">%s</a> > <a href="?p=music&album=%s">%s</a><br />' % (genre[0], genre[1], genre[2], genre[3])

    for music in musics:
        print '<a href="?p=album&artist=%s">%s</a> > <a href="?p=music&album=%s">%s</a> > %s<br />' % \
        (music['artist_id'], music['artist_name'], music['album_id'], music['album_name'], music['music_name'])
    print '</div>'

def format_time(mtime):

    def time_tuple(ts):
        if ts is None or ts < 0:
            ts = 0
        days = ts / 86400
        hours = (ts % 86400) / 3600
        mins = (ts % 3600) / 60
        secs = (ts % 3600) % 60
        tstr = '%02d:%02d' % (mins, secs)
        if int(days):
            tstr = '%02d days %02d:%s' % (days, hours, tstr)
        elif int(hours):
            tstr = '%02d:%s' % (hours, tstr)
        return (int(days), int(hours), int(mins), int(secs), tstr)

    days, hours, mins, secs, curr_str = time_tuple(mtime)
    return curr_str

def format_size(sz):

    KB_BYTES = 1024
    MB_BYTES = 1048576
    GB_BYTES = 1073741824
    KB_UNIT = 'KB'
    MB_UNIT = 'MB'
    GB_UNIT = 'GB'

    unit = 'Bytes'
    if sz >= GB_BYTES:
        sz = float(sz) / float(GB_BYTES)
        unit = GB_UNIT
    elif sz >= MB_BYTES:
        sz = float(sz) / float(MB_BYTES)
        unit = MB_UNIT
    else:
        sz = float(sz) / float(KB_BYTES)
        unit = KB_UNIT
    return "%.2f %s" % (sz, unit)
