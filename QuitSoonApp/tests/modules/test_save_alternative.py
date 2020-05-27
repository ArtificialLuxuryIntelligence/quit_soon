from decimal import Decimal
import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from QuitSoonApp.models import Alternative, ConsoAlternative
from QuitSoonApp.modules import SaveAlternative

class SavePackTestCase(TestCase):

    def setUp(self):
        """setup tests"""
        self.usertest = User.objects.create_user(
            'NewUserTest', 'test@test.com', 'testpassword')

    def test_if_strNone_get_None_or_str(self):
        data = 'None'
        self.assertEqual(SaveAlternative.if_strNone_get_None_or_str(data), None)
        data = 1637
        self.assertEqual(SaveAlternative.if_strNone_get_None_or_str(data), '1637')
        data = 'str'
        self.assertEqual(SaveAlternative.if_strNone_get_None_or_str(data), 'str')

    def if_strNone_get_None_or_float(self):
        data = 'None'
        self.assertEqual(SaveAlternative.if_strNone_get_None_or_str(data), None)
        data = 2
        self.assertEqual(SaveAlternative.if_strNone_get_None_or_str(data), 2.0)
        data = 2.0
        self.assertEqual(SaveAlternative.if_strNone_get_None_or_str(data), 2.0)
        data = 'erreur'
        self.assertEqual(SaveAlternative.if_strNone_get_None_or_str(data), None)

    def test_create_new_alternative(self):
        """test SavePack.create_alternative method if type_alternative != 'Su'"""
        datas ={
            'type_alternative':'Ac',
            'type_activity':'Sp',
            'activity': 'COURSE',
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.create_alternative()
        db_create_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Ac',
            type_activity='Sp',
            activity='COURSE',
            )
        self.assertTrue(db_create_alternative.exists())

    def test_create_new_alternative_already_in_db(self):
        """test SavePack.create_alternative method if type_alternative == 'Su' and alternative already in db"""
        Alternative.objects.create(
            user=self.usertest,
            type_alternative='Su',
            substitut='P24',
            nicotine=2.0,
            display=False,
            )
        datas ={
            'type_alternative':'Su',
            'substitut':'P24',
            'nicotine': 2,
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.create_alternative()
        db_create_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Su',
            substitut='P24',
            nicotine=2.0,
            )
        self.assertFalse(db_create_alternative.count() == 2)
        self.assertEqual(db_create_alternative.count(), 1)
        self.assertEqual(db_create_alternative[0].display, True)

    def test_create_new_alternative_substitut(self):
        """test SavePack.create_alternative method if type_alternative == 'Su'"""
        datas ={
            'type_alternative':'Su',
            'substitut':'P24',
            'nicotine': 2,
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.create_alternative()
        db_create_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Su',
            substitut='P24',
            nicotine=2.0,
            )
        self.assertTrue(db_create_alternative.exists())

    def test_create_new_alternative_substitut_already_in_db(self):
        """test SavePack.create_alternative method if type_alternative == 'Su'"""
        Alternative.objects.create(
            user=self.usertest,
            type_alternative='Su',
            substitut='ECIG',
            nicotine=2.0,
            )
        datas ={
            'type_alternative':'Su',
            'substitut':'ECIG',
            'nicotine': 2,
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.create_alternative()
        db_create_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Su',
            substitut='ECIG',
            nicotine=2.0,
            )
        self.assertFalse(db_create_alternative.count() == 2)

    def test_delete_unused_alternative_activity(self):
        """test SaveAlternative.delete_alternative method with unused alternative"""
        Alternative.objects.create(
            user=self.usertest,
            type_alternative='Ac',
            type_activity='So',
            activity='PSYCHOLOGUE',
            )
        datas ={
            'type_alternative':'Ac',
            'type_activity':'So',
            'activity':'PSYCHOLOGUE',
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.delete_alternative()
        db_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Ac',
            type_activity='So',
            activity='PSYCHOLOGUE',
            )
        self.assertFalse(db_alternative.exists())

    def test_delete_unused_alternative_substitut(self):
        """test SaveAlternative.delete_alternative method with unused alternative"""
        Alternative.objects.create(
            user=self.usertest,
            type_alternative='Su',
            substitut='ECIG',
            nicotine=2.0,
            )
        datas ={
            'type_alternative':'Su',
            'substitut':'ECIG',
            'nicotine':2,
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.delete_alternative()
        db_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Su',
            substitut='ECIG',
            nicotine=2.0,
            )
        self.assertFalse(db_alternative.exists())

    def test_delete_used_alternative_activity(self):
        """test SavePack.delete_alternative method with used alternative"""
        alternative = Alternative.objects.create(
            user=self.usertest,
            type_alternative='Ac',
            type_activity='So',
            activity='PSYCHOLOGUE',
            )
        conso = ConsoAlternative.objects.create(
            user=self.usertest,
            date_alter=datetime.date(2020, 5, 13),
            time_alter=datetime.time(13, 55),
            alternative=alternative,
        )
        datas ={
            'type_alternative':'Ac',
            'type_activity':'So',
            'activity':'PSYCHOLOGUE',
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.delete_alternative()
        db_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Ac',
            type_activity='So',
            activity='PSYCHOLOGUE',
            )
        self.assertTrue(db_alternative.exists())
        self.assertEqual(db_alternative[0].display, False)

    def test_delete_used_alternative_substitut(self):
        """test SavePack.delete_alternative method with used alternative"""
        alternative = Alternative.objects.create(
            user=self.usertest,
            type_alternative='Su',
            substitut='ECIG',
            nicotine=2.0,
            )
        conso = ConsoAlternative.objects.create(
            user=self.usertest,
            date_alter=datetime.date(2020, 5, 13),
            time_alter=datetime.time(13, 55),
            alternative=alternative,
        )
        datas ={
            'type_alternative':'Su',
            'substitut':'ECIG',
            'nicotine':'2',
            }
        alternative = SaveAlternative(self.usertest, datas)
        alternative.delete_alternative()
        db_alternative = Alternative.objects.filter(
            user=self.usertest,
            type_alternative='Su',
            substitut='ECIG',
            nicotine=2.0,
            )
        self.assertTrue(db_alternative.exists())
        self.assertEqual(db_alternative[0].display, False)
