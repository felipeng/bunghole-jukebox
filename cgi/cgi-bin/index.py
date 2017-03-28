#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       index.py
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

import sys, os, glob, stat, shutil, types
import cgi, cgitb; cgitb.enable()
from pysqlite2 import dbapi2 as sqlite
from htmljukebox import *

reload(sys)
sys.setdefaultencoding('utf-8')

class Config(object):
    def __init__(self):
        self.dict = {}

    def load(self):
        configfile = open('../html/jukebox/config/jukebox.conf').readlines()
        for line in configfile:
            line = line.strip()
            if line == '' or line.startswith('#'): continue
            key, value = line.split('#')[0].split('=')
            value = value.strip().replace(' ', '').split(',')
            if len(value) == 1: value = value[0]

            self.dict[key.strip()] = value

        themes = os.listdir(self.dict['html_path'] + '/themes')
        self.dict['themes'] = [x for x in themes if x[0] != '.']

    def save(self):
        configfile = open('../html/jukebox/config/jukebox.conf', 'w')
        for key in self.dict.keys():
            value = self.dict[key]
            if isinstance(value, list): value = ','.join(value)
            configfile.write('='.join([key, value]) + '\n')
        configfile.close()

def connect():
    conn = sqlite.connect('../html/jukebox/config/jukebox.db')
    conn.row_factory = sqlite.Row
    cursor = conn.cursor()
    return conn, cursor

def become_daemon():
    pid = os.fork()
    if pid != 0: # if pid is not child...
        sys.exit(0)

    os.setsid() # Create new session and sets process group.
    pid = os.fork() # Will have INIT (pid 1) as parent process...
    if pid != 0: # if pid is not child...
        sys.exit(0)

def make_thumbnail(path_in, path_out, size=(128, 128)):
    from PIL import Image

    img = Image.open(path_in)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(path_out, 'JPEG')

def checktags(audio, path):
    '''Check if the audio file have all the necessary tags.'''

    msg = '(NOTAG) Invalid ID3 tag'
    if not audio.tags: 
        log(msg + ': ' + path)
        return False
    elif not audio.has_key('title'):
        log(msg + ' (Title): ' + path)
        return False
    elif not audio.has_key('album'):
        log(msg + ' (Album): ' + path)
        return False
    elif not audio.has_key('artist'):
        log(msg + ' (Artist): ' + path)
        return False
    elif not audio.has_key('date'):
        log(msg + ' (Year): ' + path)
        return False
    elif not audio.has_key('tracknumber'):
        log(msg + ' (Track): ' + path)
        return False
    return True

def log(msg, method='a'):
    file = open('../html/jukebox/config/jukebox.log', method)
    file.write(msg + '\n')
    file.close()

def walktree(top='.', depthfirst=True):
    #Walk the directory tree, starting from top. Credit to Noah Spurrier and Doug Fort.
    names = os.listdir(top)
    names.sort()
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            st = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for(newtop, children) in walktree(os.path.join(top, name), depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

def get_all_artists():
    conn, cursor = connect()
    artists = cursor.execute('SELECT * FROM artist ORDER BY name').fetchall()
    conn.close()
    return artists

def get_all_albums(artist_id):
    conn, cursor = connect()
    albums = cursor.execute('SELECT artist.id artist_id, artist.name artist_name, album.* \
                            FROM album, artist WHERE artist.id=album.artist_id AND artist.id=%s \
                            ORDER BY album.year' % artist_id).fetchall()
    conn.close()
    return albums

def get_all_musics(album_id):
    conn, cursor = connect()
    musics = cursor.execute('SELECT artist.id artist_id, artist.name artist_name, album.id album_id, album.name album_name, \
                            album.genre album_genre, album.year album_year, music.* \
                            FROM artist, album, music WHERE artist.id=album.artist_id AND album.id=music.album_id AND album.id=%s \
                            ORDER BY music.track' % album_id).fetchall()
    conn.close()
    return musics

def gettotalinfo():
    conn, cursor = connect()
    artists = cursor.execute('SELECT COUNT(*) FROM artist').fetchone()[0]
    albums  = cursor.execute('SELECT COUNT(*) FROM album').fetchone()[0]
    musics  = cursor.execute('SELECT COUNT(*) FROM music').fetchone()[0]
    conn.close()
    return artists, albums, musics

def gettotalinfostartswith(letter):
## FIXME = Selecionado o # retorna 0
    conn, cursor = connect()
    artists = cursor.execute('SELECT COUNT(*) FROM artist WHERE upper(name) LIKE "%s%%"' % letter).fetchone()[0]
    albums  = cursor.execute('SELECT COUNT(*) FROM artist, album WHERE artist.id = album.artist_id and upper(artist.name) LIKE "%s%%"' % letter).fetchone()[0]
    musics  = cursor.execute('SELECT COUNT(*) FROM artist, album, music WHERE artist.id = album.artist_id and album.id = music.album_id and upper(artist.name) LIKE "%s%%"' % letter).fetchone()[0]
    conn.close()
    return artists, albums, musics

def gettotalsize():
    conn, cursor = connect()
    total_size = cursor.execute('SELECT SUM(size) from music').fetchone()[0]
    conn.close()
    return total_size

def gettotaltime():
    conn, cursor = connect()
    total_size = cursor.execute('SELECT SUM(length) from music').fetchone()[0]
    conn.close()
    return total_size

def getartiststartswith(letter):
    sql = 'SELECT * FROM artist WHERE '
    if letter == '0':
        for i in map(chr, range(65, 91)):
            if i != 'A':
                sql += ' and '
            sql += 'upper(name) not like "%s%%"' % i
    else:
        sql += 'upper(name) like "%s%%"' % letter
    sql += 'ORDER BY name'

    conn, cursor = connect()
    artists = cursor.execute(sql).fetchall()
    conn.close()
    return artists

def search_by(sql):
    conn, cursor = connect()
    result = cursor.execute(sql).fetchall()
    conn.close()
    return result

def search_artists_by_name(name):
    sql = 'SELECT * FROM artist WHERE upper(name) \
           like "%%%s%%" ORDER BY name' % name
    return search_by(sql)

def search_albums_by_name(name):
    sql = 'SELECT artist.id, artist.name, album.id, \
          album.name FROM artist, album WHERE \
          album.artist_id = artist.id AND album.name like "%%%s%%"' % name
    return search_by(sql)

def search_albums_by_year(year):
    sql = 'SELECT artist.id, artist.name, album.id, \
          album.name FROM artist, album WHERE \
          album.artist_id = artist.id AND year like "%%%s%%"' % year
    return search_by(sql)

def search_albums_by_genre(genre):
    sql = 'SELECT artist.id, artist.name, album.id, \
          album.name FROM artist, album WHERE \
          album.artist_id = artist.id AND genre like "%%%s%%"' % genre
    return search_by(sql)

def search_musics_by_name(name):
    sql = 'SELECT artist.id artist_id, artist.name artist_name, \
    album.id album_id, album.name album_name, \
    music.name music_name \
    FROM artist, album, music WHERE \
    album.artist_id = artist.id AND \
    music.album_id = album.id AND upper(music.name) like "%%%s%%" \
    ORDER BY artist.name, album.name, music.name' % name
    return search_by(sql)

def main(config={}, mediadir='~/mp3'):
    try:
        from mutagen.mp3 import MP3
        from mutagen.easyid3 import EasyID3
    except ImportError:
        return 1

    CACHE_PATH = config.dict['html_path'] + '/cache'
    log('', 'w') # zera o log

    sql = open('../html/jukebox/config/create_tables.sql', 'r').read()

    conn, cursor = connect()
    cursor.executescript(sql) # zera o banco

    if os.path.isdir(CACHE_PATH):
        shutil.rmtree(CACHE_PATH)

    os.mkdir(CACHE_PATH)

    for dir, files in walktree(mediadir, False):
        for file in files:
            fullpath = os.path.join(dir, file)
            relativepath = fullpath.split(mediadir)

            ext = file[-3:].lower()
            if ext != 'mp3':
                log('(NOTMP3) The file isn\'t an audio file: %s' % fullpath)
                continue

            try:
                audio = MP3(fullpath, ID3=EasyID3)
            except Exception:
                log('(NOTMP3) The file isn\'t an audio file: %s' % fullpath)
                continue

            if not checktags(audio, fullpath):
                continue

            cursor.execute('SELECT id FROM artist WHERE name LIKE "%s"' %  audio['artist'][0])
            artist = cursor.fetchone()
            if not artist:
                cursor.execute('INSERT INTO artist (name) VALUES ("%s")' %  audio['artist'][0])
                artist = cursor.lastrowid
            else:
                artist = artist[0]

            cursor.execute('SELECT album.id FROM album WHERE album.name LIKE "%s" AND artist_id = "%s"' % (audio['album'][0], artist))
            album = cursor.fetchone()
            if not album:
                genre = None
                if audio.has_key('genre'):
                    genre = audio['genre'][0]

                cursor.execute('INSERT INTO album (name, artist_id, year, genre) VALUES ("%s", "%s", "%s", "%s")' %
                (audio['album'][0], artist, audio['date'][0][:4], genre))

                album = cursor.lastrowid
            else:
                album = album[0]

            # imagens dos álbuns
            size = [int(x) for x in config.dict['cover_size']]
            if not os.path.exists('%s/%.4i.jpg' % (CACHE_PATH, album)):
                img_list = []
#                for i in config.dict['cover_mask']:
#                    img_list.extend(glob.glob(dir +  '/' + i))

                if len(img_list) > 0:
                    make_thumbnail(img_list[0], '%s/%.4i.jpg' % (CACHE_PATH, album), size)
                else:
                    f = MP3(fullpath)

                    apic_keys = []
                    for key in f.keys():
                        if key[:4] == 'APIC':
                            apic_keys.append(key)

                    if len(apic_keys) > 0:
                        if len(apic_keys) > 1:
                            for key in apic_keys:
                                if f.get(key).type == 3:
                                    apic = f.get(key).data
                        else:
                            apic = f.get(apic_keys[0]).data

                        apic_path = '%s/%.4i.jpg' % (CACHE_PATH, album)
                        f = open(apic_path, 'w')
                        f.write(apic)
                        f.close()

                        make_thumbnail(apic_path, apic_path, size)

            size = os.path.getsize(fullpath)

            cursor.execute(u'INSERT INTO music (name, album_id, track, length, bitrate, path, size) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' %
            (audio['title'][0].replace('"', '\''), album, audio['tracknumber'][0], audio.info.length, audio.info.bitrate, relativepath[1], size))
            conn.commit()
            log(fullpath)

    conn.close()

if __name__ == '__main__':
    config = Config()
    config.load()

    htmlheader(config)

    form = cgi.FieldStorage()
    page = form.getvalue('p')

    if page:
        if page == 'log':
            log = open('../html/jukebox/config/jukebox.log', 'r').readlines()
            htmllog(log, form.getvalue('view'))
        elif page == 'artist':
            if form.has_key('s'):
                letter = form.getvalue('s')
                artists = getartiststartswith(letter)
                letter_stats = gettotalinfostartswith(letter)
                htmlartists(artists, letter_stats, letter, stats=gettotalinfo())
        elif page == 'album':
            albums = get_all_albums(form.getvalue('artist'))
            htmlalbums(config, albums, stats=gettotalinfo())
        elif page == 'music':
            musics = get_all_musics(form.getvalue('album'))
            htmlmusics(config, musics, stats=gettotalinfo())
        elif page == 'search':
            criteria = form.getvalue('q')
            type = form.getvalue('t')
            if type == 'artist':
                result = search_artists_by_name(criteria)
                htmlsearch(artists=result, stats=gettotalinfo())
            elif type == 'album':
                result = search_albums_by_name(criteria)
                htmlsearch(albums=result, stats=gettotalinfo())
            elif type == 'year':
                result = search_albums_by_year(criteria)
                htmlsearch(years=result, stats=gettotalinfo())
            elif type == 'genre':
                result = search_albums_by_genre(criteria)
                htmlsearch(genres=result, stats=gettotalinfo())
            else:
                result = search_musics_by_name(criteria)
                htmlsearch(musics=result, stats=gettotalinfo())
        elif page == 'settings':
            if form.has_key('a'):
                config.dict['theme'] = form.getvalue('theme') 
                config.dict['cover_size'] = form.getvalue('cover_size')
#                config.dict['cover_mask'] = form.getvalue('selectb')
                config.dict['album_view'] = form.getvalue('album_view')
                config.dict['flash_player'] = form.getvalue('flash_player')
                config.dict['url_music'] = form.getvalue('url_music')
                config.dict['mp3_dir'] = form.getvalue('mp3_dir')
                config.save()
            htmlsettings(config)
        elif page == 'about':
            htmlabout()
    else:
        if form.has_key('path'):
            become_daemon()
            main(config, form.getvalue('path'))
        else:
            htmlindex(stats=gettotalinfo(), total_size=gettotalsize(), total_time=gettotaltime())

    htmlfooter()
