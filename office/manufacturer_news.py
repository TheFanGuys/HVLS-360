"""Bounded first-party news-index discovery; publisher dates/claims stay unverified."""
import datetime as dt
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit
import urllib.request

MAX_BYTES=700_000
MAX_ARTICLES=40
class NewsIndex(HTMLParser):
    def __init__(self,base):
        super().__init__();self.base=base;self.rows=[];self.item=None;self.capture=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);classes=attrs.get('class','').split()
        if tag=='article':self.item={'title':'','date':''};self.capture=None
        if self.item is None:return
        if tag=='span' and 'post-date' in classes:self.capture=('date','span')
        if tag=='a' and 'post-link' in classes:
            self.item['url']=urljoin(self.base,attrs.get('href',''));self.capture=('title','a')
    def handle_data(self,data):
        if self.item is not None and self.capture:self.item[self.capture[0]]+=data
    def handle_endtag(self,tag):
        if self.capture and tag==self.capture[1]:self.capture=None
        if tag!='article' or self.item is None:return
        item=self.item;self.item=None;self.capture=None
        if len(self.rows)>=MAX_ARTICLES:return
        link=urlsplit(item.get('url',''));base=urlsplit(self.base)
        if link.scheme!='https' or link.hostname!=base.hostname or link.username or link.password:return
        if not link.path.startswith('/news/'):return
        try:date=dt.datetime.strptime(' '.join(item['date'].split()),'%b %d, %Y').date().isoformat()
        except ValueError:return
        title=' '.join(item['title'].split())
        if not title:return
        self.rows.append({'title':title,'url':item['url'],'published':date,
                          'date_basis':'publisher_reported_date_only','source_kind':'official_manufacturer_index',
                          'discovery_url':self.base,'index_scope':f'First {MAX_ARTICLES} dated articles within {MAX_BYTES} bytes; not exhaustive coverage'})
def entries(html,url):
    parser=NewsIndex(url);parser.feed(html.decode('utf-8',errors='replace') if isinstance(html,bytes) else html)
    return parser.rows

def fetch(url):
    request=urllib.request.Request(url,headers={'User-Agent':'HVLS360-ResearchDesk/1.0','Accept':'text/html'})
    with urllib.request.urlopen(request,timeout=12) as response:
        actual=urlsplit(response.geturl());expected=urlsplit(url)
        if actual.scheme!='https' or actual.hostname!=expected.hostname:raise ValueError('Official index redirected outside source')
        if 'text/html' not in response.headers.get('Content-Type','').lower():raise ValueError('Official index is not HTML')
        raw=response.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:
            sample=raw[:MAX_BYTES]
            if len(entries(sample,url))<MAX_ARTICLES:
                raise ValueError('Official index exceeds bounded sample without enough complete dated entries')
            # A complete bounded latest-news sample is sufficient; do not fetch the archive/footer.
            return sample
        return raw
