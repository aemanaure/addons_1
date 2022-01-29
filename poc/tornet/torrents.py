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

#HOST = 'https://gitlab.com/stiletto1/s/-/raw/main/c'
source = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/ult').data
host = scrapertools.find_single_match(source, r'<host>([^<]+)<')
try:
    actu_xml = os.path.join(config.get_runtime_path(), 'actu.xml')
    last_xml = os.path.join(config.get_runtime_path(), 'last.xml')
    las0_xml = os.path.join(config.get_runtime_path(), 'las0.xml')
    
    if os.path.exists(actu_xml) == False:
        dat1 = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/actu.xml', timeout=2).data
        filetools.write(actu_xml, dat1)

    if os.path.exists(last_xml) == False:
        dat2 = httptools.downloadpage(host, timeout=2).data
        filetools.write(last_xml, dat2)

    if os.path.exists(las0_xml) == False:
        dat0 = httptools.downloadpage(host, timeout=2).data 
        filetools.write(las0_xml, dat0)
except:
    None

runtime_path = translatePath(xbmcaddon.Addon(id="plugin.video.mediaexplorer").getAddonInfo('Path')).rstrip(os.sep)

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

    '''try:
        data = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/ult').data
        active = scrapertools.find_single_match(data, r'<active>([^<]+)<')
        if active == "0":
            itemlist.append(item.clone(
                label="Últimas añadidas",
                action="selection",
                content_type='movies',
                type="item",
                group=True
            ))
    except:
        None'''

    try:
        data = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/ult').data
        active = scrapertools.find_single_match(data, r'<active>([^<]+)<')
        if active == "0":
            itemlist.append(item.clone(
                label="Últimas añadidas",
                action="last",
                content_type='movies',
                type="item",
                group=True
            ))
    except:
        None

    '''itemlist.append(item.clone(
        label="Última adición",
        action="last_added",
        content_type='movies',
        type="item",
        group=True
    ))'''

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
        label="Sagas",
        action="sagas",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Géneros",
        action="generos",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Listado por años",
        action="years",
        content_type='movies',
        type="item",
        group=True
    ))

    itemlist.append(item.clone(
        label="Listado alfabético",
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
        actu_xml = os.path.join(runtime_path, 'actu.xml')
        last_xml = os.path.join(runtime_path, 'last.xml')
        las0_xml = os.path.join(runtime_path, 'las0.xml')

        if os.path.exists(actu_xml) == False:
            dat1 = httptools.downloadpage('https://raw.githubusercontent.com/pepemebe/mag/main/poc/actu.xml', timeout=2).data
            filetools.write(actu_xml, dat1)

        if os.path.exists(last_xml) == False:
            dat2 = httptools.downloadpage(host, timeout=2).data
            filetools.write(last_xml, dat2)

        if os.path.exists(las0_xml) == False:
            dat0 = httptools.downloadpage(host, timeout=2).data 
            filetools.write(las0_xml, dat0)

        diff = filecmp.cmp(las0_xml, last_xml, shallow=False)
        
        if diff == False:
            if os.path.exists(actu_xml):
                os.remove(actu_xml)
            data = open(last_xml).read()
            filetools.write(actu_xml, data)

            if os.path.exists(last_xml):
                os.remove(last_xml)
            data = open(las0_xml).read()
            filetools.write(last_xml, data)
    except:
        url = 'https://raw.githubusercontent.com/pepemebe/mag/main/poc/actu.xml'
        data = httptools.downloadpage(url).data
        filetools.write(actu_xml, data)

    try:
        actu_xml = os.path.join(runtime_path, 'actu.xml')
        dat1 = open(actu_xml).read()
    except:
        ur1 = 'https://raw.githubusercontent.com/pepemebe/mag/main/poc/actu.xml'
        dat1 = httptools.downloadpage(ur1).data
    
    dat1 = re.sub(r"\n|\r|\t|<b>|\s{2}|&nbsp;", "", dat1)
    patro1 = r'<title>([^<]+)</'
    
    for tit in scrapertools.find_multiple_matches(dat1, patro1):
        title = normalizar(tit)
        if not title in auxlist:
            auxlist.add(title)

    try:
        las0_xml = os.path.join(runtime_path, 'las0.xml')
        dat2 = open(las0_xml).read()
    except:
        ur0 = 'https://gitlab.com/stiletto1/s/-/raw/main/c'
        dat2 = httptools.downloadpage(ur0).data
    
    dat2 = re.sub(r"\n|\r|\t|<b>|\s{2}|&nbsp;", "", dat2)
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


'''def last_added(item):
    logger.trace()
    itemlist = list()
    
    url = 'https://github.com/lamalanovela/tacones/commits/main/nuevo'
    data = httptools.downloadpage(url).data
    data = re.sub(r"\n|\r|\t|<b>|\s{2}|&nbsp;", "", data)

    patron = r'href="([^"]+)">Update nuevo</a>'
    commit = 'https://github.com' + scrapertools.find_single_match(data, patron)
    data = httptools.downloadpage(commit).data
    data = re.sub(r"\n|\r|\t|<b>|\s{2}|&nbsp;|&lt;|&gt;|<span class=\"pl-ent\">|</span>", "", data)

    patron = r'data-code-marker="\+"><item>' \
             r'.*?data-code-marker="\+"><title>([^<]+)</title' \
             r'.*?data-code-marker="\+"><micro(.*?)/cuatrok' \
             r'.*?data-code-marker="\+"><thumbnail>([^<]+)</thumbnail' \
             r'.*?data-code-marker="\+"><fanart>([^<]+)</fanart' \
             r'.*?data-code-marker="\+"><date>([^<]+)</date' \
             r'.*?data-code-marker="\+"><info>([^<]+)</info'
    
    for tit, calidades, poster, fanart, year, plot in scrapertools.find_multiple_matches(data, patron):

        title = normalizar(tit)
        cals = qualities(calidades)

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

    return itemlist'''


@LimitResults
def movies(item):
    logger.trace()
    itemlist = list()

    alea = "LA" if item.label == "Selección aleatoria" else "NO"

    try:
        las0_xml = os.path.join(config.get_runtime_path(), 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|<b>|\s{2}|&nbsp;", "", data)

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


@LimitResults
def search(item):
    logger.trace()
    itemlist = list()

    try:
        las0_xml = os.path.join(config.get_runtime_path(), 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|<b>|\s{2}|&nbsp;", "", data)

    patron = r'<item.*?<title>([^<]+)</.*?<micro(.*?)/cuatrok>.*?<thumbnail>([^<]+)</.*?<fanart>' \
             r'([^<]+)</.*?<date>([^<]+)</.*?<genre>([^<]+)</.*?<info>([^<]+)</'
    
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
        
        #cals = set()

        if 'MEN IN BLACK' in tit or 'CICLO CLINT EASTWOOD' in tit or 'CLASICOS DE DISNEY' in tit \
            or 'CHARLOT' in tit or 'DEADPOOL' in tit or 'LA CENICIENTA. TRILOGIA' in tit \
            or 'WONDER WOMAN' in tit or 'TRANSFORMERS' in tit or 'EL REY LEON' in tit \
            or 'LA SIRENITA ( TRILOGIA )' in tit or 'LA PURGA' in tit in tit or 'HOTEL TRANSILVANIA' in tit \
            or 'RESIDENT EVIL' in tit:
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
    elif item.label == 'Últimas añadidas':
        item.com = 'last'

    '''if item.label == 'Últimas añadidas':
        url = 'https://raw.githubusercontent.com/pepemebe/mag/main/poc/last'
    else:
        url = host'''

    try:
        las0_xml = os.path.join(config.get_runtime_path(), 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|<b>|\s{2}|&nbsp;", "", data)

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
                last='last' if item.label == 'Últimas añadidas' else 'NO',
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
    data = re.sub(r"\n|\r|\t|\(|\)|<b>|\s{2}|&nbsp;", "", data)

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
        las0_xml = os.path.join(config.get_runtime_path(), 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|\(|\)|<b>|\s{2}|&nbsp;", "", data)

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

    '''if item.last == 'last':
        url = 'https://raw.githubusercontent.com/pepemebe/mag/main/poc/last'
    else:
        url = host'''

    try:
        las0_xml = os.path.join(config.get_runtime_path(), 'las0.xml')
        data = open(las0_xml).read()
    except:
        url = host
        data = httptools.downloadpage(url).data

    data = re.sub(r"\n|\r|\t|\(|\)|\¿|\?|<b>|\s{2}|&nbsp;", "", data)
    item.lab =re.sub(r"\(|\)|\¿|\?", "", item.lab)

    patron = r'<item.*?<title>%s</.*?tle>(.*?)<thumb' % item.lab

    cal = scrapertools.find_single_match(data, patron)
    
    for calidad, url in scrapertools.find_multiple_matches(cal, r'<([^<]+)>([^<]+)</'):
        if 'CLASICOS DE DISNEY' in item.lab or 'EL REY LEON 2' in item.lab or 'EL REY LEON 3' in item.lab:
            cal = QLT.get('sd')
        else:
            cal = QLT.get(calidad)
            
        if url != 'NA':
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

