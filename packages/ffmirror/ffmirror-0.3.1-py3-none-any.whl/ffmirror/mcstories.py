# Site module for mcstories.

import re
import dateutil.parser
from bs4 import BeautifulSoup  # type: ignore

from ffmirror.util import urlopen_retry, fold_string_indiscriminately

def get_author_list(soup):
    el = soup.find('table', id='index')
    rv = []
    for i in el('tr'):
        ca = {}
        ca['name'] = i.td.a.string
        ca['link'] = i.td.a['href']
        nst = i.td.find_next_sibling('td').string
        o = re.match(r"(\d+) stor(y|ies)", nst)
        ca['n_stories'] = int(o.group(1))
        rv.append(ca)
    return rv

# A site module needs to implement the following:
#  - get_user_url(self, md):
#    given a story metadata object, return a canonical link for the author
#  - get_story_url(self, md):
#    given a story metadata object, return a canonical link for the story
#  - download_metadata(self, sid):
#    given a story ID, download its metadata and TOC and return
#  - compile_story(self, md, toc, outfile):
#    given metadata and TOC, download a whole story and write it to outfile
#  - download_list(self, aid):
#    given author ID, download a list of stories as metadata (metadata entries
#    may be incomplete)
class MCStories(object):
    hostname = "www.mcstories.com"
    this_site = "mcstories"
    story_url = "http://{hostname}/{sid}/index.html"
    user_url = "http://{hostname}/Authors/{aid}.html"
    chapter_url = "http://{hostname}/{sid}/{chl}"

    story_url_re = re.compile(r"https?://(?P<hostname>[^/]+)/(?P<sid>[^/]+)/index\.html")  # noqa: E501
    user_url_re = re.compile(r"https?://(?P<hostname>[^/]+)/Authors/(?P<aid>[^/]+)\.html")  # noqa: E501

    def get_user_url(self, md):
        return self.user_url.format(hostname=self.hostname, aid=md['authorid'])

    def get_story_url(self, md):
        return self.story_url(hostname=self.hostname, sid=md['id'])

    def get_chapter_url(self, md, t):
        return self.chapter_url.format(hostname=self.hostname, sid=md['id'],
                                       chl=t[1])

    def _get_metadata(self, soup):
        rv = {}
        rv['title'] = soup.find('h3', class_='title').string
        al = soup.find('h3', class_='byline').a
        rv['author'] = al.string
        o = re.match(r"\.\./Authors/(.+)\.html$", al['href'])
        if o is None:
            raise ValueError("Badly formatted author link")
        rv['authorid'] = o.group(1)
        pe = soup.find('h3', class_='dateline', string=re.compile(r"^Added"))
        o = re.match(r"^Added (.+)", pe.string)
        rv['published'] = dateutil.parser.parse(o.group(1)).isoformat(' ')
        ue = soup.find('h3', class_='dateline', string=re.compile(r"^Updated"))
        if ue is None:
            rv['updated'] = rv['published']
        else:
            o = re.match(r"^Updated (.+)", ue.string)
            rv['updated'] = dateutil.parser.parse(o.group(1)).isoformat(' ')
        rv['site_tags'] = ','.join(sorted(set([i.string for i in
                                               soup.find('div',
                                                         class_='storyCodes')
                                               ('a')])))

        cc = 0
        wc = 0
        cl = []
        try:
            cel = soup.find('table', id='index')('tr')
            for i in cel:
                if i.td is None:
                    continue
                cc += 1
                tds = i('td')
                o = re.match(r"^(\d+) words", tds[1].string)
                wc += int(o.group(1))
                cl.append((tds[0].a.string, tds[0].a['href']))
        except TypeError:
            cel = soup.find('div', class_='chapter')
            cc = 1
            cl.append((cel.a.string, cel.a['href']))
            o = re.search(r"\((\d+) words\)", cel.get_text())
            wc = o.group(1)
        rv['chapters'] = cc
        rv['words'] = wc
        rv['site'] = self.this_site
        rv['summary'] = re.sub(r"\s+", " ", soup.find('section',
                                                      class_='synopsis').
                               get_text())
        return rv, cl

    def download_metadata(self, sid):
        url = self.story_url.format(hostname=self.hostname, sid=sid)
        r = urlopen_retry(url)
        html = r.read()
        soup = BeautifulSoup(html, 'html5lib')
        rv, cl = self._get_metadata(soup)
        rv['id'] = sid
        return rv, cl

    def _get_story_list(self, soup, aid):
        ans = soup.find('h3', class_='title').string
        o = re.match(r"Author: (.+)", ans)
        an = o.group(1)
        el = soup.find('table', id='index')
        rv = []
        for i in el('tr'):
            if i.td is None:
                continue
            cs = {}
            ds = i('td')
            cs['title'] = ds[0].a.cite.string
            ls = ds[0].a['href']
            o = re.match(r"\.\./([^/]+)/index\.html", ls)
            cs['id'] = o.group(1)
            cs['site_tags'] = ','.join(sorted(set(ds[1].string.split())))
            cs['published'] = (dateutil.parser.parse(ds[2].string).
                               isoformat(' '))
            try:
                us = ds[3].string.strip()
            except IndexError:
                us = ''
            if us != '':
                cs['updated'] = dateutil.parser.parse(us).isoformat(' ')
            else:
                cs['updated'] = cs['published']
            cs['author'] = an
            cs['authorid'] = aid
            cs['site'] = self.this_site
            rv.append(cs)
        info = { 'name': an, 'aid': aid, 'site': self.this_site }
        return rv, [], info

    def download_list(self, aid):
        url = self.user_url.format(hostname=self.hostname, aid=aid)
        r = urlopen_retry(url)
        data = r.read()
        soup = BeautifulSoup(data, 'html5lib')
        return self._get_story_list(soup, aid)

    def _chapter_title(self, t):
        return t[0]

    def _make_toc(self, contents):
        """Makes an HTML string table of contents to be concatenated into outstr, given
        the return value of _get_contents (array of chapter names).

        """
        rs = "<h2>Contents</h2>\n<ol>\n"
        for x, i in enumerate(contents):
            n = x + 1
            anc = "#ch{}".format(n)
            rs += ("<li><a href=\"{}\">{}</a></li>\n".
                   format(anc, self._chapter_title(i)))
        rs += "</ol>\n"
        return rs

    def _get_storytext(self, data):
        soup = BeautifulSoup(data, 'html5lib')
        a = soup.find('article', id='mcstories')
        try:
            a.find('div', class_='storyCodes').decompose()
        except AttributeError:
            pass
        for i in a('h3'):
            i.decompose()
        return str(a)

    def compile_story(self, md, toc, outfile, headers=True, contents=False,
                      callback=None, **kwargs):
        outfile.write("""<html>
<head>
<meta charset="UTF-8" />
<meta name="Author" content="{author}" />
<title>{title}</title>
<style type="text/css">
body {{ font-family: sans-serif }}
</style>
</head>
<!-- Fic ID: {id}
""".format(title=md['title'], id=md['id'], author=md['author']))
        for k, v in sorted(md.items()):
            outfile.write("{}: {}\n".format(k, v))
        outfile.write("-->\n<body>\n")
        if headers:
            outfile.write("<h1>{}</h1>\n".format(md['title']))
        if contents:
            outfile.write(self._make_toc(toc))
        for n, t in enumerate(toc):
            x = n + 1
            url = self.get_chapter_url(md, t)
            if callback:  # For printing progress as it runs.
                callback(n, self._chapter_title(t))
            r = urlopen_retry(url)
            data = r.read().decode()
            text = self._get_storytext(data)
            if headers:
                outfile.write("""<h2 id="ch{}" class="chapter">{}</h2>\n""".
                              format(x, self._chapter_title(t)))
            text = fold_string_indiscriminately(text)
            outfile.write(text + "\n\n")
        outfile.write("</body>\n</html>\n")

    def get_tags_for(self, md):
        return set(md['site_tags'].split(','))

    def compare_mds(self, r, cr):
        """Check two metadata entries to see if they 1. refer to the same story, 2. at
        the same length. Used to check for updates."""
        try:
            if r['updated'] != cr['updated']:
                return False
        except KeyError as e:  # if the metadata is incomplete
            return False
        return True
