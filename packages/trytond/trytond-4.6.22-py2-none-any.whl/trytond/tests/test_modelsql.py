# -*- coding: utf-8 -*-
# This file is part of Tryton.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

import unittest
import time

from mock import patch, call

from trytond import backend
from trytond.exceptions import UserError, ConcurrencyException
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.tests.test_tryton import activate_module, with_transaction


class ModelSQLTestCase(unittest.TestCase):
    'Test ModelSQL'

    @classmethod
    def setUpClass(cls):
        activate_module('tests')

    @unittest.skipIf(backend.name() == 'sqlite',
        'SQLite not concerned because tryton don\'t set "NOT NULL"'
        'constraint: "ALTER TABLE" don\'t support NOT NULL constraint'
        'without default value')
    @with_transaction()
    def test_required_field_missing(self):
        'Test error message when a required field is missing'
        pool = Pool()
        Modelsql = pool.get('test.modelsql')
        transaction = Transaction()

        fields = {
            'desc': '',
            'integer': 0,
            }
        for key, value in fields.iteritems():
            try:
                Modelsql.create([{key: value}])
            except UserError, err:
                # message must not quote key
                msg = "'%s' not missing but quoted in error: '%s'" % (key,
                        err.message)
                self.assertTrue(key not in err.message, msg)
            else:
                self.fail('UserError should be caught')
            transaction.rollback()

    @with_transaction()
    def test_check_timestamp(self):
        'Test check timestamp'
        pool = Pool()
        ModelsqlTimestamp = pool.get('test.modelsql.timestamp')
        transaction = Transaction()
        # transaction must be committed between each changes otherwise NOW()
        # returns always the same timestamp.
        record, = ModelsqlTimestamp.create([{}])
        transaction.commit()

        timestamp = ModelsqlTimestamp.read([record.id],
            ['_timestamp'])[0]['_timestamp']

        if backend.name() in ('sqlite', 'mysql'):
            # timestamp precision of sqlite is the second
            time.sleep(1)

        ModelsqlTimestamp.write([record], {})
        transaction.commit()

        transaction.timestamp[str(record)] = timestamp
        self.assertRaises(ConcurrencyException,
            ModelsqlTimestamp.write, [record], {})

        transaction.timestamp[str(record)] = timestamp
        self.assertRaises(ConcurrencyException,
            ModelsqlTimestamp.delete, [record])

        transaction.timestamp.pop(str(record), None)
        ModelsqlTimestamp.write([record], {})
        transaction.commit()
        ModelsqlTimestamp.delete([record])
        transaction.commit()

    @with_transaction()
    def test_create_field_set(self):
        'Test field.set in create'
        pool = Pool()
        Model = pool.get('test.modelsql.field_set')

        with patch.object(Model, 'set_field') as setter:
            records = Model.create([{'field': 1}])
            setter.assert_called_with(records, 'field', 1)

        # Different values are not grouped
        with patch.object(Model, 'set_field') as setter:
            records = Model.create([{'field': 1}, {'field': 2}])
            setter.assert_has_calls([
                    call([records[0]], 'field', 1),
                    call([records[1]], 'field', 2),
                    ])

        # Same values are grouped in one call
        with patch.object(Model, 'set_field') as setter:
            records = Model.create([{'field': 1}, {'field': 1}])
            setter.assert_called_with(records, 'field', 1)

        # Mixed values are grouped per value
        with patch.object(Model, 'set_field') as setter:
            records = Model.create([{'field': 1}, {'field': 2}, {'field': 1}])
            setter.assert_has_calls([
                    call([records[0], records[2]], 'field', 1),
                    call([records[1]], 'field', 2),
                    ])

    @with_transaction()
    def test_integrity_error_with_created_record(self):
        "Test integrity error with created record"
        pool = Pool()
        ParentModel = pool.get('test.one2many')
        TargetModel = pool.get('test.one2many.target')

        # Create target record without required name
        # to ensure create_records is filled to prevent raising
        # foreign_model_missing
        record = ParentModel(name="test")
        record.targets = [TargetModel()]
        with self.assertRaises(UserError) as cm:
            record.save()
        err = cm.exception
        msg = 'The field "%s" on "%s" is required.' % (
            TargetModel.name.string, TargetModel.__doc__)
        self.assertEqual(err.message, msg)

    @with_transaction()
    def test_null_ordering(self):
        'Test NULL ordering'
        pool = Pool()
        NullOrder = pool.get('test.null_order')

        NullOrder.create([{
                    'integer': 1,
                    }, {
                    'integer': 3,
                    }, {
                    'integer': None,
                    }])
        integers = NullOrder.search([], order=[('integer', 'ASC NULLS FIRST')])
        self.assertListEqual([i.integer for i in integers], [None, 1, 3])

        integers = NullOrder.search(
            [], order=[('integer', 'DESC NULLS FIRST')])
        self.assertListEqual([i.integer for i in integers], [None, 3, 1])

        integers = NullOrder.search([], order=[('integer', 'ASC NULLS LAST')])
        self.assertListEqual([i.integer for i in integers], [1, 3, None])

        integers = NullOrder.search([], order=[('integer', 'DESC NULLS LAST')])
        self.assertListEqual([i.integer for i in integers], [3, 1, None])


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(ModelSQLTestCase)
