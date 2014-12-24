# -*- coding: utf-8 -*-

from nose.tools import eq_
from nose.tools import ok_
from nose.tools import raises

from sqlalchemy.orm.exc import NoResultFound

import transaction


from tracim.model.data import Content
from tracim.model.data import ContentType
from tracim.model.data import Workspace

from tracim.model.serializers import Context
from tracim.model.serializers import ContextConverterNotFoundException
from tracim.model.serializers import CTX
from tracim.model.serializers import DictLikeClass

from tracim.model.data import ActionDescription

from tracim.lib.user import UserApi

from tracim.tests import TestStandard



class TestSerializers(TestStandard):

    def test_DictLikeClass(self):
        instance = DictLikeClass()

        instance.bob = 'titi'
        ok_(instance.bob==instance['bob'])

        instance['titi'] = 'bob'
        ok_(instance.titi==instance['titi'])

        instance2 = DictLikeClass(instance)
        ok_(instance2.bob==instance2['bob'])
        ok_(instance2.bob==instance.bob)
        ok_(instance2.titi==instance2['titi'])
        ok_(instance2.titi==instance.titi)

        instance3 = DictLikeClass({'bob': 'titi', 'toto': 'bib'})
        ok_(instance3.bob=='titi')
        ok_(instance3.bob==instance3['bob'])

        ok_(instance3.toto=='bib')
        ok_(instance3.toto==instance3['toto'])

    def test_ContextConverterNotFoundException(self):
        class DummyClass(object):
            pass
        context = 'some_context'
        e = ContextConverterNotFoundException(context, DummyClass)
        eq_('converter not found (context: some_context - model: DummyClass)', e.__str__())

    def test_serialize_ActionDescription_DEFAULT(self):
        obj = ActionDescription('archiving')
        obj.icon = 'places/folder-remote'
        obj.label = 'edit the content'

        res = Context(CTX.DEFAULT).toDict(obj)
        eq_(res.__class__, DictLikeClass)
        eq_(obj.id, res.id)
        eq_(obj.label, res.label)
        eq_(obj.icon, res.icon)
        eq_(3, len(res.keys()))

    def test_serialize_Content_DEFAULT(self):
        obj = Content()
        obj.content_id = 132
        obj.label = 'Some label'
        obj.description = 'Some Description'

        res = Context(CTX.DEFAULT).toDict(obj)
        eq_(res.__class__, DictLikeClass, res)
        eq_(obj.content_id, res.id, res)
        eq_(obj.label, res.label, res)

        ok_('folder' in res.keys())
        ok_('id' in res.folder.keys())
        eq_(None, res.folder.id)
        eq_(1, len(res.folder.keys()))

        ok_('workspace' in res.keys())
        eq_(None, res.workspace, res)
        eq_(4, len(res.keys()), res)



    def test_serialize_Content_comment_THREAD(self):

        wor = Workspace()
        wor.workspace_id = 4

        fol = Content()
        fol.type = ContentType.Folder
        fol.content_id = 72
        fol.workspace = wor

        par = Content()
        par.type = ContentType.Thread
        par.content_id = 37
        par.parent = fol
        par.workspace = wor

        obj = Content()
        obj.type = ContentType.Comment
        obj.content_id = 132
        obj.label = 'some label'
        obj.description = 'Some Description'
        obj.parent = par

        res = Context(CTX.THREAD).toDict(obj)
        eq_(res.__class__, DictLikeClass, res)

        ok_('label' in res.keys())
        eq_(obj.label, res.label, res)

        ok_('content' in res.keys())
        eq_(obj.description, res.content, res)

        ok_('created' in res.keys())

        ok_('icon' in res.keys())
        eq_(ContentType.icon(obj.type), res.icon, res)

        ok_('id' in res.folder.keys())
        eq_(obj.content_id, res.id, res)

        ok_('owner' in res.folder.keys())
        eq_(None, res.owner, res) # TODO - test with a owner value

        ok_('type' in res.folder.keys())
        eq_(obj.type, res.type, res)

        ok_('urls' in res.folder.keys())
        ok_('delete' in res.urls.keys())

        eq_(8, len(res.keys()), res)