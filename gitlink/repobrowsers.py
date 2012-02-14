#!/usr/bin/env python
# encoding: utf-8

from os.path import join as pjoin


class RepoBrowser(object):
    ''' I represent a repository browser and my methods return links to the
        various git objects that I am capable of showing '''

    def tag(self, name):
        ''' Get url for tag name '''
        raise NotImplementedError

    def commit(self, sha):
        ''' Get url for commit object '''
        raise NotImplementedError

    def branch(self, ref, shortref):
        ''' Get url for branch name '''
        raise NotImplementedError

    def diff(self, diffspec):
        ''' Get url for diff '''
        raise NotImplementedError

    def tree(self, sha):
        ''' Get url for tree object '''
        raise NotImplementedError

    def path(self, path, tree, commit):
        ''' Get url for a path relative to the root of repository '''
        raise NotImplementedError

    def blob(self, sha, path, tree, commit, raw):
        ''' Get url for a blob object '''
        raise NotImplementedError

    def join(self, *args):
        l = [self.url] ; l.extend(args)
        return pjoin(*l)


class LinkType(object):
    unknown = 0x1
    commit  = 0x2
    tree    = 0x3
    tag     = 0x4
    branch  = 0x5
    diff    = 0x6
    blob    = 0x7
    path    = 0x8


class GitwebBrowser(RepoBrowser):
    ''' gitweb - git's default web interface '''

    options = {
        'head-view' : {
            'help'    : 'default head view',
            'choices' : ('shortlog', 'log', 'tree'),
        },
        'commit-view' : {
            'help'    : 'default commit view',
            'choices' : ('commit', 'commitdiff', 'tree'),
        },
        'tag-view' : {
            'help'    : 'default tag view',
            'choices' : ('commit', 'shortlog', 'log'),
        },
    }

    def __init__(self, url,
                 head_view='shortlog',
                 commit_view='commitdiff',
                 tag_view='commit'):

        self.url = url.rstrip('/')

        self.tag_view = tag_view
        self.head_view = head_view
        self.commit_view = commit_view

    def commit(self, sha):
        l = (self.url, 'a=%s' % self.commit_view, 'h=%s' % sha)
        return ';'.join(l)

    def tree(self, sha, path=None):
        l = [self.url, 'a=tree', 'h=%s' % sha]
        if path: l.append('f=%s' % path)
        return ';'.join(l)

    def branch(self, ref, shortref):
        l = (self.url, 'a=%s' % self.head_view, 'h=%s' % shortref)
        return ';'.join(l)

    def tag(self, name):
        l = (self.url, 'a=%s' % self.tag_view, 'h=%s' % name)
        return ';'.join(l)

    def blob(self, sha, path, tree=None, commit=None, raw=False):
        if tree and tree == 'HEAD^{tree}':
            tree = None

        l = [self.url, 'a=blob', 'h=%s' % sha]

        if path:
            l.append('f=%s' % path)

        url =  ';'.join(l)

        if raw:
            url = url.replace('a=blob', 'a=blob_plain', 1)

        return url

    def path(self, path, tree=None, commit=None):
        l = (self.url, 'a=tree', 'f=%s' % path, 'h=%s' % tree)
        return ';'.join(l)


class GithubBrowser(RepoBrowser):
    ''' github public repositories '''

    def __init__(self, url):
        self.url = url

    def commit(self, sha):
        return self.join('commit', sha)

    def tree(self, sha):
        ''' TBD '''

    def branch(self, ref, shortref):
        return self.join('tree', shortref)

    def tag(self, name):
        return self.join('tree', name)

    def blob(self, sha, path, tree=None, commit=None, raw=False):
        url = self.join('tree', commit, path) # @bug

        if raw:
            url = url.replace('github.com', 'raw.github.com', 1)
            url = url.replace('/tree/', '/', 1)

        return url

    def path(self, path, tree, commit):
        return self.join('tree', commit, path)


class GithubPrivateBrowser(GithubBrowser):
    ''' github private repositories (I don't know how a private repo looks
        like, but I assume it's the same) '''


class CgitBrowser(RepoBrowser):
    ''' cgit - web interface for git repositories, written in c '''

    def __init__(self, url):
        self.url = url

    def commit(self, sha):
        return self.join('commit', '?id=%s' % sha)

    def tree(self, sha):
        return self.join('tree', '?tree=%s' % sha)

    def branch(self, ref, shortref):
        if not shortref: return None
        return self.join('log', '?h=%s' % shortref)

    def tag(self, name):
        return self.join('tag', '?id=%s' % name)

    def blob(self, sha, path, tree=None, commit=None, raw=False):
        if tree and tree == 'HEAD^{tree}':
            tree = None

        url = self.path(path, tree)

        if raw:
            url = url.replace('tree', 'plain', 1)

        return url

    def path(self, path, tree=None, commit=None):
        url = [self.url, 'tree', path]
        if tree:
            url.append('?tree=%s' % tree)

        return pjoin(*url)


names = {
    'cgit'           : CgitBrowser,
    'gitweb'         : GitwebBrowser,
    'github'         : GithubBrowser,
    'github-private' : GithubPrivateBrowser,
}

