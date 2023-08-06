#!/usr/bin/python
# -*- coding: utf-8 -*-

from strip_accents import text_to_id
import hashlib
import re
import datetime

# flake8: noqa: C901
def generate_GUID2(nom, prenom, age, sexe):

    if '-' in age:
        if re.match(r"^[0-9]{2}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str, r'%d-%m-%Y').strftime(r'%d-%m-%Y')
            key = nom + prenom + date_time_obj + sexe

            keygood = text_to_id(key)

            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

            return GUID

        if re.match(r"^[0-9]{4}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str,
            r'%Y-%m-%d').strftime(r'%d-%m-%Y')
            key = nom + prenom + date_time_obj + sexe
            keygood = text_to_id(key)
            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()
            return GUID

    if '/' in age:
        if re.match(r"^[0-9]{2}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str, r'%d/%m/%Y').strftime(r'%d/%m/%Y')

            key = nom + prenom + date_time_obj + sexe

            keygood = text_to_id(key)
            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

            return GUID

        if re.match(r"^[0-9]{4}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str, r'%Y/%m/%d').strftime(r'%d/%m/%Y')

            key = nom + prenom + date_time_obj + sexe

            keygood = text_to_id(key)
            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

            return GUID

    if r"\\" in age:
        if re.match(r"^[0-9]{2}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str, r'%d\%m\%d').strftime(r'%d\%m\%Y')

            key = nom + prenom + date_time_obj + sexe

            keygood = text_to_id(key)
            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

            return GUID

        if re.match(r"^[0-9]{4}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str, r'%Y\%m\%d').strftime(r'%d\%m\%Y')

            key = nom + prenom + date_time_obj + sexe

            keygood = text_to_id(key)
            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

            return GUID

    if ' ' in age:
        if re.match(r"^[0-9]{2}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str, r'%d %m %Y').strftime(r'%d %m %Y')

            key = nom + prenom + date_time_obj + sexe
            keygood = text_to_id(key)
            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

            return GUID

        if re.match(r"^[0-9]{4}\D", age):
            date_time_str = str(age)
            date_time_obj = datetime.datetime.strptime(date_time_str, r'%Y %m %d').strftime(r'%d %m %Y')

            key = nom + prenom + date_time_obj + sexe
            keygood = text_to_id(key)
            GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

            return GUID
    else:

        key = nom + prenom + age + sexe
        keygood = text_to_id(key)
        GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()

        return GUID


def generate_GUID(keyInput):

    key = keyInput
    keygood = text_to_id(key)
    GUID = hashlib.sha256(keygood.encode('utf-8')).hexdigest()
    return GUID
