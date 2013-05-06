import os
import re
from ConfigParser import SafeConfigParser, NoOptionError
from collections import namedtuple

def read_config(fname):
    cfg = SafeConfigParser()
    cfg.read(fname)
    return cfg

def package_sections(sections, package):
    '''
    Return all sections in list of sections that match a given pacakge
    '''
    pat = r'package %s\b' % package
    ret = []
    for sec in sections:
        if re.match(pat,sec):
            #print 'Checking %s' % (sec,)
            ret.append(sec)

    if not ret:
        raise ValueError, 'No package sections for package "%s"' % package

    return ret

def version_consistent(version, constraint):
    '''
    Return true if the constraint string is consistent with the version string.
    '''
    from pkg_resources import parse_version
    cleaned = []
    for token in [x.strip() for x in constraint.split()]:
        if token in ['version','and','or','==','!=','<','>','<=','>=']:
            cleaned.append(token)
            continue
        cleaned.append('pv("%s")' % token)
    code = ' '.join(cleaned)
    return eval(code, {'version':parse_version(version), 'pv':parse_version})
        
def dep_constraints(pkg_ver, dep_string):
    '''
    Return True if all dependencies in dep_string are consistent with package versions.
    '''
    for dep in [x.strip() for x in dep_string.split(',')]:
        parts = dep.split(' ',1)
        if len(parts) == 1:
            continue
        name, constraint = parts
        version = pkg_ver[name]
        if constraint and not version_consistent(version, constraint):
            return False
    return True
            
def section_constraint(section, type='package'):
    '''Return a constraint from a section title or None.
    Section title is of form: "<type> <name> [<the constraint>]"'''
    if not section.startswith('%s ' % type):
        raise ValueError, 'Section not of type %s: %s' % (type, section)
    parts = section.split(' ',2)
    if len(parts) == 2:         # no constraint
        return
    return parts[2]
    

def interpolate_dict(d):
    depth = 10
    last_d = dict(d)
    while depth:
        depth -= 1
        new_d = {}
        for k,v in last_d.items():
            try:
                new_v = v.format(**last_d)
            except ValueError:
                print 'Attempted interpolation on: "%s"' % v
                raise
            new_d[k] = new_v
        if new_d == last_d:         # converged
            return new_d
        last_d = new_d
    raise ValueError, 'Exceeded maximum interpolation recursion'


def resolve_suite(cfg, suite):
    '''Resolve elemnts of given suite from the config object into a list
    of package-specific strings
    '''

    suitesec = 'suite %s' % suite
    tags = [x.strip() for x in cfg.get(suitesec, 'tags').split()]

    defsec = cfg.get(suitesec, 'defaults')
    defaults = cfg.items('defaults ' + defsec, raw = True)

    pkgsec = cfg.get(suitesec, 'packages', raw=True)
    pkg_ver = dict(cfg.items('packagelist ' + pkgsec, raw = True))

    uname_fields = ['kernelname', 'hostname', 'kernelversion', 'vendorstring', 'machine']
    hostinfo = { k:v for k,v in zip(uname_fields, os.uname()) }

    package_list = []
    for pkgname,version in pkg_ver.items():
        totry = package_sections(cfg.sections(), pkgname)

        matching = []
        for section in totry:

            constraint = section_constraint(section)
            if constraint and not version_consistent(version, constraint):
                print 'Constraint on %s %s does not match "%s"' % (pkgname, version, constraint)
                continue

            try:
                deps = cfg.get(section, 'depends')
            except NoOptionError, err:
                print 'Accepting section "%s" for %s/%s (no deps)' % \
                    (section, pkgname, version)
                matching.append(section)
                continue

            if not dep_constraints(pkg_ver, deps):
                print '%s (%s) fails section %s due to dependency constraints' % \
                    (pkgname, version, section)
                continue
            print 'Accepting section "%s" for %s/%s (consistent dependencies)' % \
                (section, pkgname, version)
            matching.append(section)
            continue
        if len(matching) != 1:
            raise ValueError, 'Got %d package sections matching %s %s (%s)' % \
                (len(matching), pkgname, version, ', '.join(matching))

        pkg = dict(package=pkgname, version=version, suite=suite,
                   tags=' '.join(tags), tagsdashed='-'.join(tags))
        pkg.update(hostinfo)
        pkg.update(defaults)

        actions = []
        for k,v in cfg.items(matching[0], raw=True):
            if k == 'action':
                actions += [x.strip() for x in v.split(',')]
                continue
            pkg[k] = v

        pkg = interpolate_dict(pkg)
        actions = [x.format(**pkg) for x in actions]

        package_list.append((pkg,actions))
        continue

    return package_list


def main():
    import sys
    import pprint
    cfg = read_config(sys.argv[2:])
    pl = resolve_suite(cfg,sys.argv[1])
    pp = pprint.PrettyPrinter(indent=4)
    print 'Configuration:'
    pp.pprint(pl)



if '__main__' == __name__:
    main()
