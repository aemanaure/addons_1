# -*- coding: utf-8 -*-
from core.libs import *
import unicodedata
import random

import xbmc
import xbmcaddon
from platformcode import platformsettings
import filecmp

try:
    import xbmcvfs
    translatePath = xbmcvfs.translatePath
except:
    translatePath = xbmc.translatePath


LNG = Languages({
    Languages.es: ['es']
})

QLT = Qualities({
    Qualities.sd: ['sd'],
    Qualities.hd_full: ['microhd', 'fullhd'],
    Qualities.m3d: ['tresd'],
    Qualities.uhd: ['cuatrok']
})

source = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/ult').data
host = scrapertools.find_single_match(source, r'<host>([^<]+)<')

data_path = translatePath(xbmcaddon.Addon(id="plugin.video.mediaexplorer").getAddonInfo('Profile'))

try:
    actu_xml = os.path.join(data_path, 'actu.xml')
    last_xml = os.path.join(data_path, 'last.xml')
    las0_xml = os.path.join(data_path, 'las0.xml')
    
    if os.path.exists(actu_xml) == False:
        dat1 = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/actu.xml', timeout=2).data
        filetools.write(actu_xml, dat1)

    if os.path.exists(last_xml) == False:
        dat2 = httptools.downloadpage(host, timeout=2).data
        filetools.write(last_xml, dat2)

    dat0 = httptools.downloadpage(host, timeout=2).data 
    filetools.write(las0_xml, dat0)
except:
    None

try:
    torrents_py_local = os.path.join(data_path, 'modules', 'user_channels', 'torrents.py')
    torrents_json_local = os.path.join(data_path, 'modules', 'user_channels', 'torrents.json')
    torrents_txt_remot = os.path.join(data_path, 'modules', 'user_channels', 'torrentsR.txt')
    
    data_py_remot = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/tornet/torrents.py', timeout=2).data
    data_json_remot = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/tornet/torrents.json', timeout=2).data
    filetools.write(torrents_txt_remot, data_json_remot)
        
    if os.path.exists(torrents_py_local) == False:
        filetools.write(torrents_py_local, data_py_remot)
    if os.path.exists(torrents_json_local) == False:
        filetools.write(torrents_json_local, data_json_remot)

    comp = filecmp.cmp(torrents_json_local, torrents_txt_remot, shallow=False)

    if comp == False:
        filetools.write(torrents_py_local, data_py_remot)
        filetools.write(torrents_json_local, data_json_remot)
    
except:
    None

def mainlist(item):
    logger.trace()
    itemlist = list()

    new_item = item.clone(
        type='label',
        label="Películas",
        category='movie',
        thumb='thumb/movie.png',
        icon='icon/movie.png',
        poster='poster/movie.png'
    )
    itemlist.append(new_item)
    itemlist.extend(menupeliculas(new_item))

    return itemlist


def menupeliculas(item):
    logger.trace()
    itemlist = list()

    try:
        data = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/ult').data
        active = scrapertools.find_single_match(data, r'<active>([^<]+)<')
        if active == "0" and os.path.exists(actu_xml) == True and os.path.exists(last_xml) == True and os.path.exists(las0_xml) == True:
            itemlist.append(item.clone(
                label="Últimas añadidas",
                action="last",
                content_type='movies',
                type="item",
                group=True
            ))
    except:
        None

    itemlist.append(item.clone(
        label="Cine destacado",
        action="selection",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Cine de culto",
        action="selection",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Por sagas",
        action="sagas",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Por calidad",
        action="calidad",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Por géneros",
        action="generos",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Por años",
        action="years",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Por letra (A-Z)",
        action="alfabeto",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Selección aleatoria",
        action="movies",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        action="search",
        label="Buscar",
        query=True,
        type='search',
        group=True,
        content_type='movies'
    ))

    try:
        data = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/ult').data
        kudos = scrapertools.find_single_match(data, r'<kudos>([^<]+)<')
        if kudos:
            itemlist.append(item.clone(
                label='[B][COLOR coral]KUDOS: %s[/COLOR][/B]' % kudos,
                action=None,
                type="item"
            ))
    except:
        None

    return itemlist


def last(item):
    logger.trace()
    itemlist = list()
    auxlist = set()

    try:
        diff = filecmp.cmp(las0_xml, last_xml, shallow=False)
        
        if diff == False:
            data = open(last_xml).read()
            filetools.write(actu_xml, data)

            data = open(las0_xml).read()
            filetools.write(last_xml, data)
    except:
        None

    try:
        actu_xml = os.path.join(data_path, 'actu.xml')
        dat1 = open(actu_xml).read()
    except:
        ur1 = 'https://raw.githubusercontent.com/pepemebe/mag/main/poc/actu.xml'
        dat1 = httptools.downloadpage(ur1).data
    
    dat1 = re.sub(r"\n|\r|\t|<b>|\s{2}| ", "", dat1)
    patro1 = r'<title>([^<]+)</'
    
    for tit in scrapertools.find_multiple_matches(dat1, patro1):
        title = normalizar(tit)
        if not title in auxlist:
            auxlist.add(title)

    try:
        las0_xml = os.path.join(data_path, 'las0.xml')
        dat2 = open(las0_xml).read()
    except:
        ur0 = host
        dat2 = httptools.downloadpage(ur0).data
    
    dat2 = re.sub(r"\n|\r|\t|<b>|\s{2}| ", "", dat2)
    patro2 = r'<item.*?<title>([^<]+)</.*?<micro(.*?)/cuatrok>.*?<thumbnail>([^<]+)</.*?<fanart>' \
             r'([^<]+)</.*?<date>([^<]+)</.*?<info>([^<]+)</'

    for tit, calidades, poster, fanart, year, plot in scrapertools.find_multiple_matches(dat2, patro2):

        title = normalizar(tit)
        cals = qualities(calidades)

        if not title in auxlist:
            itemlist.append(item.clone(
                title=title,
                tit=tit,
                type='movie',
                lang=LNG.get('es'),
                lab=tit,
                quality=sorted(list(cals), key=lambda i: i.level, reverse=True),
                poster=poster,
                fanart=fanart,
                year=year,
                plot=plot,
                content_type='servers',
                action='findvideos'
            ))

    return itemlist


@LimitResults
def movies(item):
    logger.trace()
    itemlist = list()

    alea = "LA" if item.label == "Selección aleatoria" else "NO"

    try:
        las0_xml = os.path.join(data_path, 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|<b>|\s{2}| ", "", data)

    patron = r'<item.*?<title>([^<]+)</.*?<micro(.*?)/cuatrok>.*?<thumbnail>([^<]+)</.*?<fanart>' \
             r'([^<]+)</.*?<date>([^<]+)</.*?<info>([^<]+)</'
    
    for tit, calidades, poster, fanart, year, plot in scrapertools.find_multiple_matches(data, 
        patron):
        
        title = normalizar(tit)
        cals = qualities(calidades)

        if 'CLASICOS DE DISNEY' in tit or 'EL REY LEON 2' in tit or 'EL REY LEON 3' in tit:
            cals.remove(QLT.get('fullhd'))
            cals.add(QLT.get('sd'))

        if 'PRIMER VENGADOR' in tit:
            year = '2011'
        if year == '1019':
            year = '1917'
        elif year == '2031':
            year = '2013'
        
        if 'LA CENICIENTA. TRILOGIA' in tit:
            year = 'VARIOS'
        
        if alea == "LA":
            item.alea = "LA"
            if 'MARVEL' in tit or 'STAR WARS' in tit:
                title = title.split('- ')[1].strip() if 'MARVEL' in tit else title.split(' -')[1].strip()
            if 'DEADPOOL' in tit and ':' in tit:
                title = title.split(': ')[1].strip()
            if 'ANIMALES FANTASTICOS' in tit and ':' in tit:
                title = title.split(': ')[1].strip()

        itemlist.append(item.clone(
            title=title,
            type='movie',
            lab=tit,
            poster=poster,
            fanart=fanart,
            plot=plot,
            lang=LNG.get('es'),
            year=year.upper(),
            content_type='servers',
            action='findvideos',
            quality=sorted(list(cals), key=lambda i: i.level, reverse=True)
        ))

    return random.sample(itemlist, k = 10) if item.alea == "LA" else sorted(itemlist, key=lambda i: i.title)


def qualities(qlt):

    patron = 'hd>([^<]+)</.*?<fullhd>([^<]+)</.*?<tresd>([^<]+)</.*?<cuatrok>([^<]+)<'

    for cal1, cal2, cal3, cal4 in scrapertools.find_multiple_matches(qlt, patron):

        cals = set()
        
        if cal1 != 'NA':
                cals.add(QLT.get('microhd'))
        if cal2 != 'NA':
                cals.add(QLT.get('fullhd'))
        if cal3 != 'NA':
                cals.add(QLT.get('tresd'))
        if cal4 != 'NA':
                cals.add(QLT.get('cuatrok'))

    return cals


def normalizar(t):

    t = re.sub(r"0N", "ON", t)
    t = re.sub(r" PANTER", " PANTHER", t)

    if t == 'BABY':
        t = 'BABY (DEL TEMOR AL AMOR)'
    elif t == 'DESTINO FATAL II':
        t = 'DESTINO FINAL 2'
    
    if "(SD)" in t or "( sd)" in t or "( sd )" in t or "( 1994 )" in t:
        t = re.sub(r"\(SD\)|\( sd\)|\( sd \)|\( 1994 \)", "", t)

    t = t.strip()

    t = six.ensure_text(t.lower())

    return ''.join((c for c in unicodedata.normalize('NFD', t.title()) if unicodedata.category(c) != 'Mn'))


def generos(item):
    logger.info()
    itemlist = []

    generos = {
        'Accion': 'Acción',
        'Infantil': 'Animación y Familiar',
        'Aventura': 'Aventura',
        'Belico': 'Bélico',
        'Ciencia Ficcion': 'Ciencia ficción',
        'Comedia': 'Comedia',
        'Drama': 'Drama',
        'Fantastico': 'Fantástico',
        'Intriga': 'Intriga',
        'Musical': 'Musical',
        'Romance': 'Romance',
        'Terror': 'Terror',
        'Thriller': 'Thriller'
        }

    for gen in sorted(generos):
        itemlist.append(item.clone(
            title=generos[gen],
            query=gen,
            lab='g',
            action='search'
        ))

    return sorted(itemlist, key=lambda i: i.title)


def alfabeto(item):
    logger.info()
    itemlist = []

    for letra in '#ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if letra == '#':
            let = r"{0,1,2,3,4,5,6,7,8,9}"
        else:
            let = letra

        itemlist.append(item.clone(
            title=letra,
            query=let,
            lab='a',
            action='search'
        ))

    return itemlist


def calidad(item):
    logger.info()
    itemlist = []
    aux = set()

    calidad = {
        'cuatrok': '4K',
        'tresd': '3D',
        'fullhd': 'FullHD',
        'microhd': 'MicroHD',
        'sd': 'SD'
        }

    for cal in sorted(calidad):
        if not QLT.get(cal) in aux:
            aux.add(QLT.get(cal))
            itemlist.append(item.clone(
                title=calidad[cal] if QLT.get(cal) != QLT.get('fullhd') else 'FullHD / MicroHD',
                query=cal,
                quality=QLT.get(cal),
                lab='c',
                action='search'
            ))

    return sorted(itemlist, key=lambda i: i.quality.level, reverse=True)


@LimitResults
def search(item):
    logger.trace()
    itemlist = list()
    aux = set()

    try:
        las0_xml = os.path.join(data_path, 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|<b>|\s{2}| ", "", data)

    patron = r'<item.*?<title>([^<]+)</.*?<micro(.*?)/cuatrok>.*?<thumbnail>([^<]+)</.*?<fanart>' \
             r'([^<]+)</.*?<date>([^<]+)</.*?<genre>([^<]+)</.*?<info>([^<]+)</'
    
    if item.lab == 's':
        urs = 'https://raw.githubusercontent.com/pepemebe/mag/main/poc/cor'
        dats = httptools.downloadpage(urs).data

        for s in scrapertools.find_multiple_matches(dats, r" '(.*?)',"):
            aux.add(s)
    
    for tit, calidades, poster, fanart, year, genre, plot in scrapertools.find_multiple_matches(
        data, patron):

        title = normalizar(tit)
        cals = qualities(calidades)

        if 'MARVEL' in tit or 'STAR WARS' in tit:
            title = title.split('- ')[1].strip() if 'MARVEL' in tit else title.split(' -')[1].strip()
        if 'DEADPOOL' in tit and ':' in tit:
            title = title.split(': ')[1].strip()
        if 'ANIMALES FANTASTICOS' in tit and ':' in tit and item.lab == 's':
            title = title.split(': ')[1].strip()
        
        tit2 = normalizar(tit)
        item.query = normalizar(item.query)
        
        if 'LA CENICIENTA. TRILOGIA' in tit:
            tit2 = normalizar('CLASICOS DE DISNEY LA CENICIENTA. TRILOGIA')
            year = 'VARIOS'
        if 'LA SIRENITA ( TRILOGIA )' in tit:
            tit2 = normalizar('CLASICOS DE DISNEY LA SIRENITA ( TRILOGIA )')
            year = 'VARIOS'

        if item.lab == 's':
            for s in aux:
                if s in tit:
                    genre = genre + ' Saga'
        if 'PRIMER VENGADOR' in tit:
            year = '2011'
        if year == '1019':
            year = '1917'
        elif year == '2031':
            year = '2013'

        if 'CLASICOS DE DISNEY' in tit or 'EL REY LEON 2' in tit or 'EL REY LEON 3' in tit:
            cals.remove(QLT.get('fullhd'))
            cals.add(QLT.get('sd'))

        if item.lab == 's':
            if 'Saga' in genre:
                item.query = re.sub(r"\s", "", item.query)
                tit2 = re.sub(r"\s", "", tit2)
                if item.query.lower() in tit2.lower():
                    if 'MARVEL' in tit or 'STAR WARS' in tit:
                        if item.label == 'SPIDER-MAN':
                            y = year.upper()
                        else:
                            y = None
                    elif 'CLASICOS DE DISNEY' in tit:
                        y = tit
                    else:
                        y = year.upper()
                    

                    itemlist.append(item.clone(
                        title=title,
                        type='movie',
                        lab=tit,
                        y=y,
                        poster=poster,
                        fanart=fanart,
                        plot=plot,
                        lang=LNG.get('es'),
                        year=year.upper(),
                        content_type='servers',
                        action='findvideos',
                        quality=sorted(list(cals), key=lambda i: i.level, reverse=True)
                    ))

        elif item.lab == 'y':
            if item.query.upper() == year.upper():
                itemlist.append(item.clone(
                    title=title,
                    type='movie',
                    lab=tit,
                    poster=poster,
                    fanart=fanart,
                    plot=plot,
                    lang=LNG.get('es'),
                    year=year.upper(),
                    content_type='servers',
                    action='findvideos',
                    quality=sorted(list(cals), key=lambda i: i.level, reverse=True)
                ))

        elif item.lab == 'g':
            if item.query.lower() in genre.lower():
                itemlist.append(item.clone(
                    title=title,
                    type='movie',
                    lab=tit,
                    poster=poster,
                    fanart=fanart,
                    lang=LNG.get('es'),
                    year=year.upper(),
                    content_type='servers',
                    action='findvideos',
                    quality=sorted(list(cals), key=lambda i: i.level, reverse=True)
                ))

        elif item.lab == 'a':
            if title[0].lower() in item.query.lower():
                itemlist.append(item.clone(
                    title=title,
                    type='movie',
                    lab=tit,
                    poster=poster,
                    fanart=fanart,
                    lang=LNG.get('es'),
                    year=year.upper(),
                    content_type='servers',
                    action='findvideos',
                    quality=sorted(list(cals), key=lambda i: i.level, reverse=True)
                ))

        elif item.lab == 'c':
            if QLT.get(item.query.lower()) in list(cals):
                itemlist.append(item.clone(
                    title=title,
                    type='movie',
                    lab=tit,
                    cal=item.query,
                    poster=poster,
                    fanart=fanart,
                    lang=LNG.get('es'),
                    year=year.upper(),
                    content_type='servers',
                    action='findvideos',
                    quality=item.quality
                ))

        else:
            if item.query.lower() in title.lower():
                itemlist.append(item.clone(
                    title=title,
                    type='movie',
                    lab=tit,
                    poster=poster,
                    fanart=fanart,
                    plot=plot,
                    lang=LNG.get('es'),
                    year=year.upper(),
                    content_type='servers',
                    action='findvideos',
                    quality=sorted(list(cals), key=lambda i: i.level, reverse=True)
                ))

    if item.lab == 's':
        return sorted(itemlist, key=lambda i: i.y)
    elif item.lab == 'y':
        return sorted(itemlist, key=lambda i: i.title)
    else:
        return itemlist


@LimitResults
def selection(item):
    logger.trace()
    itemlist = list()

    if item.label == 'Cine destacado':
        item.com = 'Estreno'
    elif item.label == 'Cine de culto':
        item.com = 'Culto'

    try:
        las0_xml = os.path.join(data_path, 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|<b>|\s{2}| ", "", data)

    patron = r'<item.*?<title>([^<]+)</.*?<micro(.*?)/cuatrok>.*?<thumbnail>([^<]+)</.*?<fanart>' \
             r'([^<]+)</.*?<date>([^<]+)</.*?<extra>([^<]+)</.*?<info>([^<]+)</'
    
    for tit, calidades, poster, fanart, year, extra, plot in scrapertools.find_multiple_matches(
        data, patron):
        
        title = normalizar(tit)
        cals = qualities(calidades)

        if 'MARVEL' in tit or 'STAR WARS' in tit:
            title = title.split('- ')[1].strip() if 'MARVEL' in tit else title.split(' -')[1].strip()
        if 'DEADPOOL' in tit and ':' in tit:
            title = title.split(': ')[1].strip()
        if 'ANIMALES FANTASTICOS' in tit and ':' in tit:
            title = title.split(': ')[1].strip()
        
        if extra == item.com or item.com == 'last':
            itemlist.append(item.clone(
                title=title,
                type='movie',
                lab=tit,
                last='NO',
                poster=poster,
                fanart=fanart,
                plot=plot,
                lang=LNG.get('es'),
                year=year.upper(),
                content_type='servers',
                action='findvideos',
                quality=sorted(list(cals), key=lambda i: i.level, reverse=True)
            ))

    return sorted(itemlist, key=lambda i: i.title)


def sagas(item):
    logger.trace()
    itemlist = list()

    url = 'https://raw.githubusercontent.com/pepemebe/mag/main/poc/sag'
    data = httptools.downloadpage(url).data
    data = re.sub(r"\n|\r|\t|\(|\)|<b>|\s{2}| ", "", data)

    for s in scrapertools.find_multiple_matches(data, r" '(.*?)',"):
        r = s
        r = re.sub(r"\.\.\.", "", r)
        if r == 'SPIDER-MAN':
            r = 'SPIDER'
        
        itemlist.append(item.clone(
            label=s,
            query=r,
            lab='s',
            action='search'
        ))

    return itemlist


def years(item):
    logger.trace()
    itemlist = list()
    aux = set()

    try:
        las0_xml = os.path.join(data_path, 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|\(|\)|<b>|\s{2}| ", "", data)

    for year in scrapertools.find_multiple_matches(data, r'<date>([^<]+)</'):
        year = year.upper()
        if year == '1019':
            year = '1917'
        elif year == '2031':
            year = '2013'
        elif year == '1950 - 2007':
            year = 'VARIOS'
        
        if not year in aux:
            aux.add(year)
            itemlist.append(item.clone(
                label=year,
                query=year,
                lab='y',
                action='search'
            ))

    return sorted(itemlist, key=lambda i: i.label, reverse=True)


def findvideos(item):
    logger.trace()
    itemlist = list()

    try:
        las0_xml = os.path.join(data_path, 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|\(|\)|\¿|\?|<b>|\s{2}| ", "", data)
    item.lab =re.sub(r"\(|\)|\¿|\?", "", item.lab)

    patron = r'<item.*?<title>%s</.*?tle>(.*?)<thumb' % item.lab

    cal = scrapertools.find_single_match(data, patron)
    
    for calidad, url in scrapertools.find_multiple_matches(cal, r'<([^<]+)>([^<]+)</'):
        if 'CLASICOS DE DISNEY' in item.lab or 'EL REY LEON 2' in item.lab or 'EL REY LEON 3' in item.lab:
            cal = QLT.get('sd')
        else:
            cal = QLT.get(calidad)

        if item.cal and cal != QLT.get('sd'):
            if url != 'NA' and QLT.get(item.cal.lower()) == QLT.get(calidad):
                itemlist.append(item.clone(
                    action="play",
                    url='magnet:?xt=urn:btih:' + url,
                    quality=cal,
                    poster=item.poster,
                    fanart=item.fanart,
                    lang=item.lang,
                    type='server',
                    server='torrent'
                ))

        elif url != 'NA':
            itemlist.append(item.clone(
                action="play",
                url='magnet:?xt=urn:btih:' + url,
                quality=cal,
                poster=item.poster,
                fanart=item.fanart,
                lang=item.lang,
                type='server',
                server='torrent'
            ))

    return servertools.get_servers_from_id(itemlist)

