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

    def branch(self, ref):
        ''' Get url for branch name '''
        raise NotImplementedError

    def diff(self, diffspec):
        ''' Get url for diff '''
        raise NotImplementedError

    def tree(self, sha):
        ''' Get url for tree object '''
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


class RepoOrCzBrowser(RepoBrowser):
    ''' repo.or.cz public git hosting '''


class GithubBrowser(RepoBrowser):
    ''' github public repositories '''


class GithubPrivateBrowser(RepoBrowser):
    ''' github private repositories '''


class CgitBrowser(RepoBrowser):
    ''' cgit - web interface for git repositories, written in c '''

    def __init__(self, url):
        self.url = url

    def commit(self, sha):
        return self.join('commit', '?id=%s' % sha)

    def tree(self, sha):
        return self.join('tree', '?tree=%s' % sha)

    def branch(self, ref):
        shortref = ref.split('/')[-1]
        return self.join('log', '?h=%s' % shortref)

    def tag(self, name):
        return self.join('tag', '?id=%s' % name)

    def blob(self, sha, path, tree=None, raw=False):
        if tree and tree == 'HEAD^{tree}':
            tree = None

        url = self.path(path, tree)

        if raw:
            url = url.replace('tree', 'plain', 1)

        return url

    def path(self, path, tree=None):
        url = [self.url, 'tree', path]
        if tree:
            url.append('?tree=%s' % tree)

        return pjoin(*url)


names = {
    'cgit'           : CgitBrowser,
    'gitweb'         : GitwebBrowser,
    'repo.or.cz'     : RepoOrCzBrowser,
    'github'         : GithubBrowser,
    'github-private' : GithubPrivateBrowser,
}

