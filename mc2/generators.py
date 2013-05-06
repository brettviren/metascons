import os

def make(target, source, env, for_signature):
    mt = env.get('make_target','')

    return 'make %s' % mt


def unpack(target, source, env, for_signature):
    
    up_dir = os.path.dirname(str(target[0]))
    if not os.path.exists(up_dir):
        os.makedirs(up_dir)

    base, ext = os.path.splitext(str(source[0]))

    upmap = [
        ('.tgz',         'tar -xzf %s'),
        ('.tar.gz',      'tar -xzf %s'),
        ('.tar.bz2',     'tar -xjf %s'),
        ('.zip',         'unzip %s'),
    ]
    
    archive = str(source[0])
    for maybe, unpacker in upmap:
        if archive.endswith(maybe):
            return unpacker % archive
    raise ValueError, 'Unknown archive format %s' % archive


def autoconf(target, source, env, for_signature):
    return './configure --prefix=%s' % env['mc_install_dir']
