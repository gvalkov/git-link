#!/usr/bin/env python
# encoding: utf-8


from util import *
from gitlink.git import *


def pytest_funcarg__repo(request):
    repo = Repo('../', '%s/test-git' % test_repo_dir)
    repo.clone()
    repo.chdir()

    return repo


def test_get_config(repo):
    repo.config('link.browser', '123')
    repo.config('link.url', 'asdf')
    repo.config('link.clipboard', 'true')

    assert get_config('link') == {
            'url'     : 'asdf',
            'browser' : '123',
            'clipboard' : True
            }

    assert get_config('link', False) == {
            'link.url'       : 'asdf',
            'link.browser'   : '123',
            'link.clipboard' : True,
            }


def test_cat_commit(repo):
    assert cat_commit('v0.1.0') == {
        'author': 'Georgi Valkov <georgi.t.valkov@gmail.com> 1329252276 +0200',
        'committer': 'Georgi Valkov <georgi.t.valkov@gmail.com> 1329252276 +0200',
        'sha': '29faca327f595c01f795f9a2e9c27dca8aabcaee',
        'tree': '80f10ec249b6916adcf6c95f575a0125b8541c05',
        'parent': 'f5d981a75b18533c270d4aa4ffffa9fcf67f9a8b',
    }


def test_commit(repo):
    assert commit('v0.1.0^') == commit('v0.1.0~')
    assert commit('v0.1.0~5')['sha'] == 'eb17e35ec82ab6ac947d73d4dc782d1f680d191d'


def test_tree(repo):
    assert tree('v0.1.0^^{tree}') == tree('v0.1.0~^{tree}')
    assert tree('v0.1.0~5^{tree}')['sha'] == 'cfa9b260c33b9535c945c14564dd50c8ffa3c89e'


def test_blob(repo):
    assert blob('v0.1.0^:setup.py') == blob('v0.1.0~:setup.py')
    assert blob('v0.1.0~2:setup.py') == blob('v0.1.0~2:setup.py')
    assert blob('v0.1.0~2:setup.py') == blob('v0.1.0~2:setup.py')

    assert blob('v0.1.0~5:gitlink/main.py') == {
        'path': 'gitlink/main.py',
        'sha': '489de118c078bd472073d2f20267e441a931b9d0',
        'type': LT.blob,
        'commit_sha': 'eb17e35ec82ab6ac947d73d4dc782d1f680d191d',
        'tree_sha': '42706139a2f62814251c5b027f8e9d38239fbcee'
    }


def test_branch(repo):
    assert branch('master')['ref'] == 'refs/remotes/origin/master'
    assert branch('master')['shortref'] == 'master'
    assert branch('origin/master')['ref'] == 'refs/remotes/origin/master'
    assert branch('origin/master')['shortref'] == 'master'


def test_tag(repo):
    assert cat_tag('v0.1.0') == {
        'sha': '29faca327f595c01f795f9a2e9c27dca8aabcaee',
        'tagger': 'Georgi Valkov <georgi.t.valkov@gmail.com> 1329252311 +0200',
        'object': 'f54a0b6ad8518babf440db870dc778acc84877a8',
        'type': 'commit',
        'tag': 'v0.1.0'
        }


def test_path(repo):
    assert path('gitlink/main.py', 'v0.1.0') == {
        'tree_sha': 'b8ff9fc80e42bec20cfb1638f4efa0215fe4987a',
        'commit_sha': 'f54a0b6ad8518babf440db870dc778acc84877a8',
        'top_tree_sha': '80f10ec249b6916adcf6c95f575a0125b8541c05',
        'sha': 'd930815a23f0cf53a471e2993bc42401926793fa',
        'path': 'gitlink/main.py',
        'type': LT.blob,
        }

    assert path('tests', 'v0.1.0') == {
        'tree_sha': 'None',
        'commit_sha': 'f54a0b6ad8518babf440db870dc778acc84877a8',
        'top_tree_sha': '80f10ec249b6916adcf6c95f575a0125b8541c05',
        'sha': '1a5bf01fcd47ff9936aac0344c587b616f081dfd',
        'path': 'tests',
        'type': LT.path,
        }

    assert path('non-existant') == {}

