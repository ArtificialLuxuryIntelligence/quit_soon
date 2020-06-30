#!/usr/bin/env python

import datetime
from datetime import datetime as dt
from datetime import date
import calendar
import pandas as pd
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import transaction


from QuitSoonApp.models import Trophee


class Trophee_checking:

    def __init__(self, stats):
        self.stats = stats
        self.df = self.smoking_values_per_dates_with_all_dates_df(self.all_dates, self.values_per_dates)
        self.challenges = {
            'conso' : {
                'nb_cig': [20, 15, 10, 5, 4, 3, 2, 1],
                'nb_days' : [3, 7]
                },
            'zero_cig': {
                'nb_cig': [0],
                'nb_days': [1, 2, 3, 4, 7, 10, 15, 20, 25, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
                },
            }

    @property
    def values_per_dates(self):
        """ get count cig smoked (col nb_cig) per dates(index) in DataFrame """
        qs = self.stats.user_conso_full_days.values()
        data_cig = pd.DataFrame(qs)
        # combine stae_cig and time_cig into a datetime column
        data_cig['date'] = data_cig.apply(lambda r : dt.combine(r['date_cig'],r['time_cig']),1)
        # get nb_cig per date sorted
        nb_cig_per_date_serie = data_cig.date.dt.date.value_counts().sort_index()
        # rename serie to nb_cig and index to date
        nb_cig_per_date_serie.rename("nb_cig", inplace=True)
        nb_cig_per_date_serie.index.name = 'date'
        # convert date to datetime
        nb_cig_per_date_serie.index = pd.to_datetime(nb_cig_per_date_serie.index)
        # convert serie to dataframe
        return nb_cig_per_date_serie.to_frame()

    @property
    def all_dates(self):
        """get all passed dates, index of empty dataframe"""
        ### get dataframe with all dates ###
        all_days_df = pd.DataFrame(self.stats.list_dates, columns=['date']).set_index('date')
        # take out the current day (only full pasts days)
        all_days_df.drop(all_days_df.tail(1).index,inplace=True)
        # convert date to datetime
        all_days_df.index = pd.to_datetime(all_days_df.index)
        return all_days_df

    def smoking_values_per_dates_with_all_dates_df(self, all_days_df, nb_cig_per_date_df):
        """
        get dataframe with all passed dates(index) and count cig per dates (col nb_cig)
        """
        # concats in dataframe and format as needed
        nb_cig_per_date_df = pd.concat([all_days_df, nb_cig_per_date_df], axis=1)
        nb_cig_per_date_df.reset_index(inplace=True)
        return nb_cig_per_date_df

    ##### consecutive dates without smoking #####

    def get_conso_occurence(self, challenge):
        """get occurence conso lower than challenge"""
        self.df['lower'] = self.df['nb_cig'].apply(lambda x: False if x > challenge else True)
        lower = self.df.lower
        self.df['upper'] = self.df['nb_cig'].apply(lambda x: True if x > challenge else False)
        upper = self.df.upper
        return lower.groupby(upper.cumsum()).sum()

    def get_nans_occurence(self):
        """ get NaNs occurence in dataframe """
        return self.df.nb_cig.isnull().groupby(self.df.nb_cig.notnull().cumsum()).sum()

    @property
    def list_user_challenges(self):
        """
        get challenges in a list of tupples (nb_cig, nb_consecutive_days)
        take only relevant challenge to check
        """
        challenges_list = []
        for type, challenge in self.challenges.items():
            for cig in challenge['nb_cig']:
                # only challenges with less cig then usual user conso
                if cig < self.stats.starting_nb_cig:
                    for days in challenge['nb_days']:
                        # only challenges if enough days in user history
                        if days <= self.stats.nb_full_days_since_start:
                            # only if challenge not already saved as trophee in db
                            if not Trophee.objects.filter(user=self.stats.user, nb_cig=cig, nb_jour=days).exists():
                                challenges_list.append((cig, days))
        return challenges_list

    @property
    def trophees_accomplished(self):
        """ get list of trophees accomplished by user and to be created in DB """
        trophee_to_create = []
        for challenge in self.list_user_challenges:
            if challenge[1] < 30:
                if self.check_days_trophees(challenge):
                    trophee_to_create.append(challenge)
            else:
                if self.check_month_trophees(challenge[1]):
                    trophee_to_create.append(challenge)
        return trophee_to_create

    def check_days_trophees(self, challenge):
        """
        ##################### non smoking days trophees #########################
        for element in occurence, check if >= element in trophee to succeed
        """
        if challenge[0] > 0:
            occurence = self.get_conso_occurence(challenge[0])
        else:
            occurence = self.get_nans_occurence()
        for element in occurence:
            if element >= challenge[1]:
                return True
        return False

    def check_month_trophees(self, challenge):
        """
        ##################### non smoking month trophees #####################
        check if completed trophees months without smoking
        """
        non_smoking_month = self.parse_smoking_month
        compared_month = range(int((challenge / 30) - 1))
        # for each bool non_smoking_month => True if full month and no smoking
        # compare with following bool
        while True:
            for i in range(len(non_smoking_month)):
                compare = [non_smoking_month[i]]
                n = 0
                # based on trophee compared following data would be different size
                for month in compared_month:
                    try:
                        n+=1
                        compare.append(non_smoking_month[i+n])
                    except IndexError:
                        # comparing data out of list index, pass next trophee checking
                        break
                if not False in compare:
                    # only full month and non smoked, break to pass next trophee checking
                    return True
            # end index in non_smoking_month, pass next trophee checking
            break
        return False


    @property
    def parse_smoking_month(self):
        """
        for each month check if full and not smoking (True), else False
        """
        non_smoking_month = []
        # proceed year after year to get appropriate calendar
        for year in self.df.date.dt.year.drop_duplicates().tolist():
            df_year = self.df[self.df.date.dt.year == year]
            for index, value in df_year.date.dt.month.value_counts().sort_index().items():
                # if full month
                if value == calendar.monthrange(year, index)[1]:
                    # Get True if all data in this month are NaNs
                    nb_Nans_in_month = df_year[(df_year.date.dt.month == index)].isnull().sum().nb_cig
                    total_rows_in_month = df_year[(df_year.date.dt.month == index)].shape[0]
                    if nb_Nans_in_month == total_rows_in_month:
                        ## one month without smoking
                        non_smoking_month.append(True)
                    else:
                        non_smoking_month.append(False)
                else:
                    non_smoking_month.append(False)
        return non_smoking_month

    def create_trophees(self):
        for trophee in self.trophees_accomplished:
            try:
                with transaction.atomic():
                    Trophee.objects.create(user=self.stats.user, nb_cig=trophee[0], nb_jour=trophee[1])
            except IntegrityError:
                # method already called
                pass