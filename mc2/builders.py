
import urllib2

# let urllib2 deal with proxies
urllib2.install_opener( urllib2.build_opener( urllib2.ProxyHandler() ))


def download(target, source, env):

    for url_file in source:
        for url in open(str(url_file)).readlines():
            url = url.strip()
            if not url: continue
            if url[0] == '#': continue
            target = os.path.join(dl_dir, os.path.basename(url))
            if os.path.exists(target):
                continue
            infp = urllib2.urlopen(url)
            outfp = open(target, 'wb')
            outfp.write(infp.read())
            outfp.close()
    
