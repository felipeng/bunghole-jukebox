from werkzeug import redirect
from werkzeug.exceptions import NotFound
from jukebox.utils import Pagination, render_template, expose, validate_url, url_for
from brain import *

@expose('/')
def index(request):
    return render_template('index.html', totalinfo=get_total_info(), totalsize=format_size(get_total_size()), totaltime=format_time(get_total_time()))

@expose('/about/')
def about(request):
    return render_template('about.html')

@expose('/settings/')
def settings(request):
    return render_template('settings.html')

@expose('/log/')
def log(request):
    log = open('jukebox/static/config/jukebox.log').readlines()

    stat_success = 0
    stat_notag = 0
    stat_notmp3 = 0
    log_success = []

    for lines in log:
        if lines.startswith('/'):
           stat_success += 1
           log_success += lines
        if lines.startswith('(NOTAG)'):
           stat_notag += 1
        if lines.startswith('(NOTMP3)'):
           stat_notmp3 += 1

    return render_template('log.html', info=get_total_info(), stat_success=stat_success, stat_notag=stat_notag, stat_notmp3=stat_notmp3, log_success=log_success)

@expose('/log/success')
def artists(request, success):
    return render_template('log_success.html')

@expose('/artists')
def artists(request, letter):
    return render_template('artists.html', letter=letter, info=get_total_info_starts_with(letter), artists=get_artist_starts_with(letter))

@expose('/artist')
def artist(request, artist):

    albums=get_all_albums(artist)

    for album in albums:
        if os.path.exists('jukebox/static/cache/%.4i.jpg' % int(album['id'])):
            cover = '/cache/%.4i.jpg' % int(album['id'])
        else:
            cover = "/images/nocover.jpg"

    return render_template('artist.html', artist=artist, info=get_total_info_of_artist(artist), albums=get_all_albums(artist), cover=cover)

@expose('/album')
def album(request, album):

    musics=get_all_musics(album)

    if os.path.exists('jukebox/static/cache/%.4i.jpg' % int(album)):
        cover = '/cache/%.4i.jpg' % int(album)
    else:
        cover = "/images/nocover.jpg"

    return render_template('album.html', musics=musics, cover=cover)

@expose('/list/', defaults={'page': 1})
@expose('/list/<int:page>')
def list(request, page):
    query = URL.query.filter_by(public=True)
    pagination = Pagination(query, 30, page, 'list')
    if pagination.page > 1 and not pagination.entries:
        raise NotFound()
    return render_template('list.html', pagination=pagination)

def not_found(request):
    return render_template('not_found.html')
