#!/usr/bin/env python

from django import forms
from django.core.exceptions import ValidationError

from QuitSoonApp.models import Alternative, ConsoAlternative

from .base_user_related_forms import UserRelatedModelForm


class TypeAlternativeForm(UserRelatedModelForm):

    class Meta:
        model = Alternative
        fields = ['type_alternative']


class ActivityForm(UserRelatedModelForm):

    class Meta:
        model = Alternative
        fields = ['type_activity', 'activity']

    def clean_activity(self):
        data = self.cleaned_data['activity']
        return data.upper()


class SubstitutForm(UserRelatedModelForm):

    class Meta:
        model = Alternative
        fields = ['substitut', 'nicotine']


class ChooseAlternativeForm(forms.Form):

    type_alternative_field = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select
            (attrs={'class':"form-control"}),
        label='',
        )

    def alternative_field():
        return forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select
            (attrs={'class':"form-control hide"}),
        label='',
        )

    sp_field = alternative_field()
    so_field = alternative_field()
    lo_field = alternative_field()
    su_field = alternative_field()

    def __init__(self, user, *args, **kwargs):

        self.user = user
        super(ChooseAlternativeForm, self).__init__(*args, **kwargs)

        self.user_alternatives = Alternative.objects.filter(user=self.user, display=True)
        self.user_conso = ConsoAlternative.objects.filter(user=self.user)

        #########################################################################################
        # define type alternative configuration (choices + initial)
        # choices = Sport, Loisir, Soin, Substitut (if alternatives of this types saved by user)
        # initial = last alternative type_activity or last alternative type_alternative(if =='Su')
        #########################################################################################
        TYPE_ALTERNATIVE_CHOICES = []
        for alternative in self.user_alternatives.filter(type_alternative='Ac').order_by('type_activity').distinct('type_activity'):
            # include user activity types
            TYPE_ALTERNATIVE_CHOICES.append((alternative.type_activity, alternative.get_type_activity_display))
            if alternative.type_activity == self.last_alternative().type_activity:
                self.initial['type_alternative_field'] = (alternative.type_activity, alternative.get_type_activity_display)
        # if user has substituts, choice substitut
        if Alternative.objects.filter(user=self.user, type_alternative='Su'):
            TYPE_ALTERNATIVE_CHOICES.append(('Su', 'Substitut'))
        if self.last_alternative().type_alternative == 'Su':
            self.initial['type_alternative_field'] = ('Su', 'Substitut')
        # define type_alternative_choices
        TYPE_ALTERNATIVE_CHOICES = tuple(TYPE_ALTERNATIVE_CHOICES)
        self.fields['type_alternative_field'].choices = TYPE_ALTERNATIVE_CHOICES

        #########################################################################################
        # define type fields configuration (choices + initial)
        #########################################################################################

        SP_FIELD_CHOICES = self.config_field('sp_field', 'Ac', 'Sp')
        self.fields['sp_field'].choices = SP_FIELD_CHOICES

        SO_FIELD_CHOICES = self.config_field('so_field', 'Ac', 'So')
        self.fields['so_field'].choices = SO_FIELD_CHOICES

        LO_FIELD_CHOICES = self.config_field('lo_field', 'Ac', 'Lo')
        self.fields['lo_field'].choices = LO_FIELD_CHOICES

        SU_FIELD_CHOICES = self.config_field('su_field', 'Su')
        self.fields['su_field'].choices = SU_FIELD_CHOICES

    def last_alternative(self, type_alternative=None, type_activity=None):
        """get user last healthy action or last created alternative"""
        if type_alternative == 'Su':
            conso = self.user_conso.filter(alternative__type_alternative=type_alternative)
        elif type_alternative == 'Ac':
            conso = self.user_conso.filter(alternative__type_activity=type_activity)
        else:
            # get last conso unrelated to type
            conso = self.user_conso

        if conso:
            lastalternative = conso.last().alternative
            if lastalternative:
                return lastalternative
        else:
            filter = self.user_alternatives
            if type_alternative:
                filter = self.user_alternatives.filter(type_alternative=type_alternative)
            if type_activity:
                filter = self.user_alternatives.filter(type_activity=type_activity)
            return filter.last()

    def config_field(self, field_name, type_alternative, type_activity=None):
        """
        configurate field depending on:
            type_activity if type_alternative='Ac' (get one field for each type of activity)
            type_alternative if type_alternative='Su' (get all substitutes in one field)
        """
        CHOICES = []
        if type_alternative == 'Ac':
            for alternative in self.user_alternatives.filter(type_activity=type_activity):
                CHOICES.append((alternative.id, alternative.activity))
                if alternative.activity == self.last_alternative(type_alternative, type_activity).activity:
                    self.initial[field_name] = (alternative.id, alternative.activity)
            return tuple(CHOICES)
        elif type_alternative == 'Su':
            for alternative in self.user_alternatives.filter(type_alternative=type_alternative):
                display = "{} ({}mg)".format(alternative.get_substitut_display(), alternative.nicotine)
                CHOICES.append((alternative.id, display))
                if alternative.substitut == self.last_alternative(type_alternative).substitut and alternative.nicotine == self.last_alternative(type_alternative).nicotine:
                    self.initial[field_name] = (alternative.id, display)
            return tuple(CHOICES)
        else:
            return None


class ChooseAlternativeFormWithEmptyFields(ChooseAlternativeForm):
    """
    Form displaying packs already used by user in order to filter consCig displayed in smoke_list
    """
    def __init__(self, user, *args, **kwargs):
        ChooseAlternativeForm.__init__(self, user)
        super(ChooseAlternativeFormWithEmptyFields, self).__init__(user, *args, **kwargs)

        #########################################################################################
        # define type alternative configuration (choices + initial)
        # choices = Sport, Loisir, Soin, Substitut (if alternatives of this types saved by user)
        # initial = last alternative type_activity or last alternative type_alternative(if =='Su')
        #########################################################################################
        TYPE_ALTERNATIVE_CHOICES = []
        for conso in self.user_conso.filter(alternative__type_alternative='Ac').order_by('alternative__type_activity').distinct('alternative__type_activity'):
            # include user activity types
            TYPE_ALTERNATIVE_CHOICES.append((conso.alternative.type_activity, conso.alternative.get_type_activity_display))
        # if user has substituts, choice substitut
        if self.user_conso.filter(alternative__type_alternative='Su'):
            TYPE_ALTERNATIVE_CHOICES.append(('Su', 'Substitut'))
        TYPE_ALTERNATIVE_CHOICES.insert(0, ('empty', '------------------'))
        self.initial['type_alternative_field'] = ('empty', '------------------')
        # define type_alternative_choices
        TYPE_ALTERNATIVE_CHOICES = tuple(TYPE_ALTERNATIVE_CHOICES)
        self.fields['type_alternative_field'].choices = TYPE_ALTERNATIVE_CHOICES

        #########################################################################################
        # define type fields configuration (choices + initial)
        #########################################################################################

        SP_FIELD_CHOICES = self.config_field('sp_field', 'Ac', 'Sp')
        self.fields['sp_field'].choices = SP_FIELD_CHOICES

        SO_FIELD_CHOICES = self.config_field('so_field', 'Ac', 'So')
        self.fields['so_field'].choices = SO_FIELD_CHOICES

        LO_FIELD_CHOICES = self.config_field('lo_field', 'Ac', 'Lo')
        self.fields['lo_field'].choices = LO_FIELD_CHOICES

        SU_FIELD_CHOICES = self.config_field('su_field', 'Su')
        self.fields['su_field'].choices = SU_FIELD_CHOICES

    def config_field(self, field_name, type_alternative, type_activity=None):
        """
        configurate field depending on:
            type_activity if type_alternative='Ac' (get one field for each type of activity)
            type_alternative if type_alternative='Su' (get all substitutes in one field)
        """
        CHOICES = []
        if type_alternative == 'Ac':
            CHOICES.insert(0, ('empty', '------------------'))
            self.initial[field_name] = ('empty', '------------------')
            for conso in self.user_conso.filter(alternative__type_activity=type_activity).order_by('alternative__activity').distinct('alternative__activity'):
                CHOICES.append((conso.alternative.id, conso.alternative.activity))
            return tuple(CHOICES)
        elif type_alternative == 'Su':
            CHOICES.insert(0, ('empty', '------------------'))
            self.initial[field_name] = ('empty', '------------------')
            for conso in self.user_conso.filter(alternative__type_alternative=type_alternative).order_by('alternative__substitut').distinct('alternative__substitut'):
                display = "{} ({}mg)".format(conso.alternative.get_substitut_display(), conso.alternative.nicotine)
                CHOICES.append((conso.alternative.id, display))
            return tuple(CHOICES)
        else:
            return None

class HealthForm(ChooseAlternativeForm):
    """Class generating a form for user healthy action"""

    date_health = forms.DateField(
        required=True,
        label='Date',
        widget=forms.DateInput(
            attrs={'class':"form-control currentDate",
                    'type':'date'},
    ))

    time_health = forms.TimeField(
        required=True,
        label='Heure',
        widget=forms.DateInput
            (attrs={'class':"form-control currentTime",
                    'type':'time'},
    ))

    ecig_vape_or_start = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple
            (attrs={'class':"hide"},
             ),
        choices=[('V', "J'ai vapoté aujourd'hui"),
                 ('S', "J'ai démarré un nouveau flacon")],
        label='',
        )

    duration_hour = forms.IntegerField(
        required=False,
        label="Pendant:",
        widget=forms.Select
            (attrs={'class':"form-control show"},
             choices= [tuple([x,x]) for x in range(25)]),
    )

    duration_min = forms.IntegerField(
        required=False,
        label='',
        widget=forms.Select
            (attrs={'class':"form-control show"},
             choices= [tuple([x,x]) for x in range(0, 60, 5)]),
    )

    def clean(self):
        """Clean all_field and specialy make sure total duration in not none for activities"""
        cleaned_data = super().clean()
        date_alter = cleaned_data.get('date_health')
        duration_hour = cleaned_data.get('duration_hour')
        duration_min = cleaned_data.get('duration_min')
        type_alternative = cleaned_data.get('type_alternative_field')

        # check if duration for user activiy
        if not duration_hour and not duration_min and type_alternative != 'Su':
            raise forms.ValidationError("Vous n'avez pas renseigné de durée pour cette activité")

        try:
            ecig_data = cleaned_data.get('ecig_vape_or_start')

            id_subsitut = int(cleaned_data.get('su_field'))
            if type_alternative == 'Su':
                # if a Ecig substitut alternative is selected in su_field
                if id_subsitut:
                    if Alternative.objects.get(id=id_subsitut).substitut.upper() == 'ECIG':
                        # check if at least one choice has been selected
                        if ecig_data == []:
                            raise forms.ValidationError("""
                                Vous avez sélectionné la cigarette électronique,
                                indiquez si vous avez vapoté aujourd'hui et/ou si vous avez démarré un nouveau flacon.
                                Ceci nous permettra de calculer le dosage quotidien moyen de votre consommation de nicotine
                                """)
                    filterV = ConsoAlternative.objects.filter(user=self.user, ecig_choice='V', date_alter=date_alter).exists()
                    filterVS = ConsoAlternative.objects.filter(user=self.user, ecig_choice='VS', date_alter=date_alter).exists()
                    if filterV or filterVS:
                        if ecig_data == ['V']:
                            raise forms.ValidationError("""
                                Vous avez déjà renseigné aujourd'hui avoir vapoté.
                                Nous prenons en compte le nombre de jours vapoté et non chaque vapotage.
                                L'information a donc déjà été renseignée.
                                """)
                        if ecig_data == ['V', 'S']:
                            self.cleaned_data['ecig_vape_or_start'] = ['S']
        except ValueError:
            pass