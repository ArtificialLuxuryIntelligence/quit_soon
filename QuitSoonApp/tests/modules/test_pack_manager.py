#!/usr/bin/env python

"""Module testing save_pack module"""

from decimal import Decimal
import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from QuitSoonApp.models import Paquet, ConsoCig
from QuitSoonApp.modules import PackManager


class PackManagerTestCase(TestCase):
    """class testing PackManager """

    def setUp(self):
        """setup tests"""
        self.usertest = User.objects.create_user(
            'NewUserTest', 'test@test.com', 'testpassword')

    def test_get_unit_u(self):
        """test PackManager.get_unit method if type_cig == IND"""
        datas ={
            'type_cig':'IND',
            'brand':'Camel',
            'qt_paquet':20,
            'price':10,
            }
        pack = PackManager(self.usertest, datas)
        self.assertEqual(pack.get_unit, 'U')
        self.assertEqual(pack.unit, 'U')

    def test_get_unit_g(self):
        """test PackManager.get_unit method if type_cig == ROL"""
        datas ={
            'type_cig':'ROL',
            'brand':'1637',
            'qt_paquet':30,
            'price':11,
            }
        pack = PackManager(self.usertest, datas)
        self.assertEqual(pack.get_unit, 'G')
        self.assertEqual(pack.unit, 'G')

    def test_get_initial_g_per_cig_u(self):
        """test PackManager.get_g_per_cig method when create new pack & if type_cig == 'IND'"""
        datas ={
            'type_cig':'IND',
            'brand':'Camel',
            'qt_paquet':20,
            'price':10,
            }
        pack = PackManager(self.usertest, datas)
        self.assertEqual(pack.get_g_per_cig(), None)
        self.assertEqual(pack.g_per_cig, None)

    def test_get_initial_g_per_cig_g(self):
        """test PackManager.get_g_per_cig method when create new pack & if type_cig == 'ROL'"""
        datas ={
            'type_cig':'ROL',
            'brand':'1637',
            'qt_paquet':30,
            'price':11,
            }
        pack = PackManager(self.usertest, datas)
        self.assertEqual(pack.get_g_per_cig(), 0.8)
        self.assertEqual(pack.g_per_cig, 0.8)

    def test_get_new_g_per_cig(self):
        """test PackManager.get_g_per_cig method when create new pack & if type_cig == 'ROL'"""
        datas ={
            'type_cig':'ROL',
            'brand':'1637',
            'qt_paquet':30,
            'price':11,
            'g_per_cig':0.9
            }
        pack = PackManager(self.usertest, datas)
        self.assertEqual(pack.get_g_per_cig(datas['g_per_cig']), 0.9)
        self.assertEqual(pack.g_per_cig, 0.9)

    def tes_get_price_per_cig_u(self):
        """test PackManager.get_price_per_cig method if type_cig == 'IND'"""
        datas ={
            'type_cig':'IND',
            'brand':'Camel',
            'qt_paquet':20,
            'price':10,
        }
        pack = PackManager(self.usertest, datas)
        self.assertEqual(pack.get_price_per_cig, 0.5)
        self.assertEqual(pack.price_per_cig, 0.5)

    def test_get_price_per_cig_gr(self):
        """test PackManager.get_price_per_cig method if type_cig == 'IND'"""
        datas ={
            'type_cig':'ROL',
            'brand':'1637',
            'qt_paquet':30,
            'price':11,
            }
        pack = PackManager(self.usertest, datas)
        self.assertEqual(pack.get_price_per_cig, Decimal('0.2933333333333333333333333333'))
        self.assertEqual(pack.price_per_cig, Decimal('0.2933333333333333333333333333'))

    def test_create_new_pack_ind(self):
        """test PackManager.create_pack method if type_cig == 'IND'"""
        datas ={
            'type_cig':'IND',
            'brand':'CAMEL',
            'qt_paquet':20,
            'price':10,
            }
        pack = PackManager(self.usertest, datas)
        pack.create_pack()
        db_pack = Paquet.objects.filter(
            user=self.usertest,
            type_cig='IND',
            brand='CAMEL',
            qt_paquet=20,
            price=10,
            )
        self.assertTrue(db_pack.exists())
        self.assertEqual(db_pack[0].unit, 'U')
        self.assertEqual(db_pack[0].g_per_cig, None)
        self.assertEqual(db_pack[0].price_per_cig, 0.5)

    def test_create_new_pack_gr(self):
        """test PackManager.create_pack method if type_cig == 'GR'"""
        datas ={
            'type_cig':'GR',
            'brand':'TEST AUTRE',
            'qt_paquet':50,
            'price':30,
            }
        pack = PackManager(self.usertest, datas)
        pack.create_pack()
        db_pack = Paquet.objects.filter(
            user=self.usertest,
            type_cig='GR',
            brand='TEST AUTRE',
            qt_paquet=50,
            price=30,
            )
        self.assertTrue(db_pack.exists())
        self.assertEqual(db_pack[0].unit, 'G')
        self.assertEqual(db_pack[0].g_per_cig, Decimal('0.8'))
        self.assertEqual(db_pack[0].price_per_cig, Decimal('0.48'))

    def test_create_pack_already_in_db(self):
        """test PackManager.create_pack method if type_cig == 'GR'"""
        db_pack = Paquet.objects.filter(
            user=self.usertest,
            type_cig='GR',
            brand='TEST AUTRE',
            qt_paquet=50,
            price=30,
            display=False,
            )
        datas ={
            'type_cig':'GR',
            'brand':'TEST AUTRE',
            'qt_paquet':50,
            'price':30,
            }
        pack = PackManager(self.usertest, datas)
        pack.create_pack()
        db_pack = Paquet.objects.filter(
            user=self.usertest,
            type_cig='GR',
            brand='TEST AUTRE',
            qt_paquet=50,
            price=30,
            )
        self.assertFalse(db_pack.count() == 2)
        self.assertEqual(db_pack.count(), 1)
        self.assertEqual(db_pack[0].display, True)

    def test_delete_unused_pack_ind(self):
        """test PackManager.delete_pack method with unused pack"""
        db_pack = Paquet.objects.create(
            user=self.usertest,
            type_cig='IND',
            brand='CAMEL',
            qt_paquet=20,
            price=10,
            )
        datas = {'id_pack': db_pack.id}
        pack = PackManager(self.usertest, datas)
        pack.delete_pack()
        db_pack = Paquet.objects.filter(
            user=self.usertest,
            type_cig='IND',
            brand='CAMEL',
            qt_paquet=20,
            price=10,
            )
        self.assertFalse(db_pack.exists())

    def test_delete_used_pack_ind(self):
        """test PackManager.delete_pack method with used pack"""
        db_pack = Paquet.objects.create(
            user=self.usertest,
            type_cig='IND',
            brand='ELPASO',
            qt_paquet=5,
            price=10,
            )
        ConsoCig.objects.create(
            user=self.usertest,
            date_cig=datetime.date(2020, 5, 13),
            time_cig=datetime.time(13, 55),
            paquet=db_pack,
        )
        datas ={'id_pack': db_pack.id}
        pack = PackManager(self.usertest, datas)
        pack.delete_pack()
        filter_pack = Paquet.objects.filter(
            user=self.usertest,
            type_cig='IND',
            brand='ELPASO',
            qt_paquet=5,
            price=10,
            )
        self.assertTrue(filter_pack.exists())
        self.assertEqual(filter_pack[0].display, False)

    def test_update_pack_g_per_cig(self):
        """test PackManager.update_pack_g_per_cig method"""
        paquet = Paquet.objects.create(
            user=self.usertest,
            type_cig='ROL',
            brand='TABACO',
            qt_paquet=40,
            price=15,
            g_per_cig=0.8,
            price_per_cig=0.3
            )
        self.assertEqual(paquet.g_per_cig, 0.8)
        self.assertEqual(paquet.price_per_cig, 0.3)
        datas ={
            'type_cig':'ROL',
            'brand':'TABACO',
            'qt_paquet':40,
            'price':15,
            'g_per_cig':0.6
            }
        pack = PackManager(self.usertest, datas)
        pack.update_pack_g_per_cig()
        find_pack = Paquet.objects.get(
            id=paquet.id,
        )
        self.assertEqual(find_pack.g_per_cig, Decimal('0.6'))
        self.assertEqual(find_pack.price_per_cig, Decimal('0.22'))
