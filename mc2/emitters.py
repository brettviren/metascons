#!/usr/bin/env python

import os

def download(target, source, env):
    'Convert URL source to .url file holding it'
    suite = env['mc_suite_data']

    dl_dir = env['mc_download_dir']
    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)

    new_source = []
    for url in map(str, source):
        urlfile = '%s-%s.url' % (env['mc_package'], env['mc_version'])
        urlpath = os.path.join(dl_dir, urlfile)
        new_source.append(urlpath)
        if os.path.exists(urlpath):
            continue

        urlfp = open(urlpath,'w')
        urlfp.write(url + '\n')
        urlfp.close()
    return target, new_source

