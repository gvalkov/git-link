#!/usr/bin/env python
# encoding: utf-8


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


names = {
    'cgit'           : CgitBrowser,
    'gitweb'         : GitwebBrowser,
    'repo.or.cz'     : RepoOrCzBrowser,
    'github'         : GithubBrowser,
    'github-private' : GithubPrivateBrowser,
}


