# -*- coding: utf-8 -*-
import datetime
import copy
import httplib2
import apiclient
import time
import pytz
import yaml
import zipfile
from six import string_types, text_type, PY2
if PY2:
    import collections as abc
else:
    import collections.abc as abc
from PIL import Image, ImageEnhance
from twilio.rest import Client as TwilioRestClient
import pycountry
import docassemble.base.ocr
if PY2:
    import cPickle as pickle
else:
    import pickle
from docassemble.base.logger import logmessage
from docassemble.base.error import DAError, DAValidationError
import docassemble.base.pandoc
import docassemble.base.pdftk
import docassemble.base.file_docx
from docassemble.base.file_docx import include_docx_template
from docassemble.base.functions import alpha, roman, item_label, comma_and_list, get_language, set_language, get_dialect, set_country, get_country, word, comma_list, ordinal, ordinal_number, need, nice_number, quantity_noun, possessify, verb_past, verb_present, noun_plural, noun_singular, space_to_underscore, force_ask, force_gather, period_list, name_suffix, currency_symbol, currency, indefinite_article, nodoublequote, capitalize, title_case, url_of, do_you, did_you, does_a_b, did_a_b, were_you, was_a_b, have_you, has_a_b, your, her, his, their, is_word, get_locale, set_locale, process_action, url_action, get_info, set_info, get_config, prevent_going_back, qr_code, action_menu_item, from_b64_json, defined, define, value, message, response, json_response, command, single_paragraph, quote_paragraphs, location_returned, location_known, user_lat_lon, interview_url, interview_url_action, interview_url_as_qr, interview_url_action_as_qr, interview_email, get_emails, this_thread, static_image, action_arguments, action_argument, language_functions, language_function_constructor, get_default_timezone, user_logged_in, interface, user_privileges, user_has_privilege, user_info, task_performed, task_not_yet_performed, mark_task_as_performed, times_task_performed, set_task_counter, background_action, background_response, background_response_action, background_error_action, us, set_live_help_status, chat_partners_available, phone_number_in_e164, phone_number_is_valid, countries_list, country_name, write_record, read_records, delete_record, variables_as_json, all_variables, server, language_from_browser, device, plain, bold, italic, states_list, state_name, subdivision_type, indent, raw, fix_punctuation, set_progress, get_progress, referring_url, undefine, dispatch, yesno, noyes, split, showif, showifdef, phone_number_part, set_parts, log, encode_name, decode_name, interview_list, interview_menu, server_capabilities, session_tags, get_chat_log, get_user_list, get_user_info, set_user_info, get_user_secret, create_user, get_session_variables, set_session_variables, get_question_data, go_back_in_session, manage_privileges, salutation, redact, ensure_definition, forget_result_of, re_run_logic, reconsider, set_title, set_save_status, single_to_double_newlines, CustomDataType, verbatim
from docassemble.base.core import DAObject, DAList, DADict, DAOrderedDict, DASet, DAFile, DAFileCollection, DAStaticFile, DAFileList, DAEmail, DAEmailRecipient, DAEmailRecipientList, DATemplate, DAEmpty, DALink, selections, objects_from_file, RelationshipTree, DAContext
from decimal import Decimal
import sys
#sys.stderr.write("importing async mail now from util\n")
from docassemble.base.filter import markdown_to_html, to_text, ensure_valid_filename

#file_finder, url_finder, da_send_mail

import docassemble.base.filter
import dateutil
import dateutil.parser
import json
import codecs
import babel.dates
#import redis
import re
import phonenumbers
import tempfile
import os
import shutil
import subprocess
from io import open
from bs4 import BeautifulSoup
import types

valid_variable_match = re.compile(r'^[^\d][A-Za-z0-9\_]*$')

__all__ = ['alpha', 'roman', 'item_label', 'ordinal', 'ordinal_number', 'comma_list', 'word', 'get_language', 'set_language', 'get_dialect', 'set_country', 'get_country', 'get_locale', 'set_locale', 'comma_and_list', 'need', 'nice_number', 'quantity_noun', 'currency_symbol', 'verb_past', 'verb_present', 'noun_plural', 'noun_singular', 'indefinite_article', 'capitalize', 'space_to_underscore', 'force_ask', 'force_gather', 'period_list', 'name_suffix', 'currency', 'static_image', 'title_case', 'url_of', 'process_action', 'url_action', 'get_info', 'set_info', 'get_config', 'prevent_going_back', 'qr_code', 'action_menu_item', 'from_b64_json', 'defined', 'define', 'value', 'message', 'response', 'json_response', 'command', 'single_paragraph', 'quote_paragraphs', 'location_returned', 'location_known', 'user_lat_lon', 'interview_url', 'interview_url_action', 'interview_url_as_qr', 'interview_url_action_as_qr', 'LatitudeLongitude', 'RoleChangeTracker', 'Name', 'IndividualName', 'Address', 'City', 'Event', 'Person', 'Thing', 'Individual', 'ChildList', 'FinancialList', 'PeriodicFinancialList', 'Income', 'Asset', 'Expense', 'Value', 'PeriodicValue', 'OfficeList', 'Organization', 'objects_from_file', 'send_email', 'send_sms', 'send_fax', 'map_of', 'selections', 'DAObject', 'DAList', 'DADict', 'DAOrderedDict', 'DASet', 'DAFile', 'DAFileCollection', 'DAFileList', 'DAStaticFile', 'DAEmail', 'DAEmailRecipient', 'DAEmailRecipientList', 'DATemplate', 'DAEmpty', 'DALink', 'last_access_time', 'last_access_delta', 'last_access_days', 'last_access_hours', 'last_access_minutes', 'returning_user', 'action_arguments', 'action_argument', 'timezone_list', 'as_datetime', 'current_datetime', 'date_difference', 'date_interval', 'year_of', 'month_of', 'day_of', 'dow_of', 'format_date', 'format_datetime', 'format_time', 'today', 'get_default_timezone', 'user_logged_in', 'interface', 'user_privileges', 'user_has_privilege', 'user_info', 'task_performed', 'task_not_yet_performed', 'mark_task_as_performed', 'times_task_performed', 'set_task_counter', 'background_action', 'background_response', 'background_response_action', 'background_error_action', 'us', 'DARedis', 'DACloudStorage', 'DAGoogleAPI', 'MachineLearningEntry', 'SimpleTextMachineLearner', 'SVMMachineLearner', 'RandomForestMachineLearner', 'set_live_help_status', 'chat_partners_available', 'phone_number_in_e164', 'phone_number_is_valid', 'countries_list', 'country_name', 'write_record', 'read_records', 'delete_record', 'variables_as_json', 'all_variables', 'ocr_file', 'ocr_file_in_background', 'read_qr', 'get_sms_session', 'initiate_sms_session', 'terminate_sms_session', 'language_from_browser', 'device', 'interview_email', 'get_emails', 'plain', 'bold', 'italic', 'path_and_mimetype', 'states_list', 'state_name', 'subdivision_type', 'indent', 'raw', 'fix_punctuation', 'set_progress', 'get_progress', 'referring_url', 'run_python_module', 'undefine', 'dispatch', 'yesno', 'noyes', 'split', 'showif', 'showifdef', 'phone_number_part', 'pdf_concatenate', 'set_parts', 'log', 'encode_name', 'decode_name', 'interview_list', 'interview_menu', 'server_capabilities', 'session_tags', 'include_docx_template', 'get_chat_log', 'get_user_list', 'get_user_info', 'set_user_info', 'get_user_secret', 'create_user', 'get_session_variables', 'set_session_variables', 'go_back_in_session', 'manage_privileges', 'start_time', 'zip_file', 'validation_error', 'DAValidationError', 'redact', 'forget_result_of', 're_run_logic', 'reconsider', 'action_button_html', 'url_ask', 'overlay_pdf', 'get_question_data', 'text_type', 'string_types', 'PY2', 'set_title', 'set_save_status', 'single_to_double_newlines', 'RelationshipTree', 'DAContext', 'DAOAuth', 'DAStore', 'explain', 'clear_explanations', 'explanation', 'set_status', 'get_status', 'verbatim']

#knn_machine_learner = DummyObject

# def TheSimpleTextMachineLearner(*pargs, **kwargs):
#     return knn_machine_learner(*pargs, **kwargs)

class DAStore(DAObject):
    """A class used to save objects to SQL."""
    def init(self, *pargs, **kwargs):
        super(DAStore, self).init(*pargs, **kwargs)
    def is_encrypted(self):
        """Returns True if the storage object is using encryption, otherwise returns False."""
        if hasattr(self, 'encrypted'):
            return self.encrypted
        if hasattr(self, 'base'):
            if self.base == 'interview':
                return False
            if self.base == 'user':
                return True
            if self.base == 'global':
                return False
            return False
        return True
    def _get_base_key(self):
        if hasattr(self, 'base'):
            if self.base == 'interview':
                return 'da:i:' + this_thread.current_info.get('yaml_filename', '')
            if self.base == 'user':
                return 'da:userid:' + text_type(this_thread.current_info['user']['the_user_id'])
            if self.base == 'global':
                return 'da:global'
            return text_type(self.base)
        return 'da:userid:' + text_type(this_thread.current_info['user']['the_user_id'])
    def defined(self, key):
        """Returns True if the key exists in the data store, otherwise returns False."""
        the_key = self._get_base_key() + ':' + key
        return server.server_sql_defined(the_key)
    def get(self, key):
        """Reads an object from the data store for the given key."""
        the_key = self._get_base_key() + ':' + key
        return server.server_sql_get(the_key, secret=this_thread.current_info.get('secret', None))
    def set(self, key, value):
        """Writes an object to the data store under the given key."""
        the_key = self._get_base_key() + ':' + key
        server.server_sql_set(the_key, value, encrypted=self.is_encrypted(), secret=this_thread.current_info.get('secret', None), the_user_id=this_thread.current_info['user']['the_user_id'])
    def delete(self, key):
        """Deletes an object from the data store"""
        the_key = self._get_base_key() + ':' + key
        server.server_sql_delete(the_key)

class DARedis(DAObject):
    """A class used to interact with the redis server."""
    def key(self, keyname):
        """Returns a key that combines the interview name with the keyname."""
        return this_thread.current_info.get('yaml_filename', '') + ':' + str(keyname)
    def get_data(self, key):
        """Returns data from Redis and unpickles it."""
        result = server.server_redis_user.get(key)
        if result is None:
            return None
        try:
            result = server.fix_pickle_obj(result)
        except:
            logmessage("get_data: could not unpickle contents of " + str(key))
            result = None
        return result
    def set_data(self, key, data, expire=None):
        """Saves data in Redis after pickling it."""
        pickled_data = pickle.dumps(data)
        if expire is not None:
            if not isinstance(expire, int):
                raise DAError("set_data: expire time must be an integer")
            pipe = server.server_redis_user.pipeline()
            pipe.set(key, pickled_data)
            pipe.expire(key, expire)
            pipe.execute()
        else:
            server.server_redis_user.set(key, pickled_data)
    def __getattr__(self, funcname):
        return getattr(server.server_redis_user, funcname)

class DACloudStorage(DAObject):
    """Returns an object that can be used to interface with S3 or Azure."""
    def init(self, *pargs, **kwargs):
        if 'provider' in kwargs and 'config' in kwargs:
            self.custom = True
            self.provider = kwargs['provider']
            self.config = kwargs['config']
            del kwargs['provider']
            del kwargs['config']
            server.cloud_custom(self.provider, self.config)
        else:
            self.custom = False
        return super(DACloudStorage, self).init(*pargs, **kwargs)
    @property
    def conn(self):
        """This property returns a boto3.resource('s3') or BlockBlobService() object."""
        if self.custom:
            return server.cloud_custom(self.provider, self.config).conn
        else:
            return server.cloud.conn
    @property
    def client(self):
        """This property returns a boto3.client('s3') object."""
        if self.custom:
            return server.cloud_custom(self.provider, self.config).client
        else:
            return server.cloud.client
    @property
    def bucket(self):
        """This property returns a boto3 Bucket() object."""
        if self.custom:
            return server.cloud_custom(self.provider, self.config).bucket
        else:
            return server.cloud.bucket
    @property
    def bucket_name(self):
        """This property returns the name of the Amazon S3 bucket."""
        if self.custom:
            return server.cloud_custom(self.provider, self.config).bucket_name
        else:
            return server.cloud.bucket_name
    @property
    def container_name(self):
        """This property returns the name of the Azure Blob Storage container."""
        if self.custom:
            return server.cloud_custom(self.provider, self.config).container
        else:
            return server.cloud.container

class DAGoogleAPI(DAObject):
    def api_credentials(self, scope):
        """Returns an OAuth2 credentials object for the given scope."""
        return server.google_api.google_api_credentials(scope)
    def http(self, scope):
        """Returns a credentialized http object for the given scope."""
        return self.api_credentials(scope).authorize(httplib2.Http())
    def drive_service(self):
        """Returns a Google Drive service object using google-api-python-client."""
        return apiclient.discovery.build('drive', 'v3', http=self.http('https://www.googleapis.com/auth/drive'))
    def cloud_credentials(self, scope):
        """Returns a google.oauth2.service_account credentials object for the given scope."""
        return server.google_api.google_cloud_credentials(scope)
    def project_id(self):
        """Returns the ID of the project referenced in the google service account credentials in the Configuration."""
        return server.google_api.project_id()
    def google_cloud_storage_client(self, scope=None):
        """Returns a google.cloud.storage.Client object."""
        return server.google_api.google_cloud_storage_client(scope)

def run_python_module(module, arguments=None):
    """Runs a python module, as though from the command line, and returns the output."""
    if re.search(r'\.py$', module):
        module = this_thread.current_package + '.' + re.sub(r'\.py$', '', module)
    elif re.search(r'^\.', module):
        module = this_thread.current_package + module
    if PY2:
        commands = [re.sub(r'/lib/python.*', '/bin/python', docassemble.base.ocr.__file__), '-m', module]
    else:
        commands = [re.sub(r'/lib/python.*', '/bin/python3', docassemble.base.ocr.__file__), '-m', module]
    if arguments:
        if not isinstance(arguments, list):
            raise DAError("run_python_module: the arguments parameter must be in the form of a list")
        commands.extend(arguments)
    output = ''
    try:
        output = subprocess.check_output(commands, stderr=subprocess.STDOUT).decode()
        return_code = 0
    except subprocess.CalledProcessError as err:
        output = err.output.decode()
        return_code = err.returncode
    return output, return_code

def today(timezone=None, format=None):
    """Returns today's date at midnight as a DADateTime object."""
    ensure_definition(timezone, format)
    if timezone is None:
        timezone = get_default_timezone()
    val = pytz.utc.localize(datetime.datetime.utcnow()).astimezone(pytz.timezone(timezone))
    if format is not None:
        return dd(val.replace(hour=0, minute=0, second=0, microsecond=0)).format_date(format)
    else:
        return dd(val.replace(hour=0, minute=0, second=0, microsecond=0))

def babel_language(language):
    if 'babel dates map' not in server.daconfig:
        return language
    return server.daconfig['babel dates map'].get(language, language)

def month_of(the_date, as_word=False, language=None):
    """Interprets the_date as a date and returns the month.
    Set as_word to True if you want the month as a word."""
    ensure_definition(the_date, as_word, language)
    if language is None:
        language = get_language()
    try:
        if isinstance(the_date, datetime.datetime) or isinstance(the_date, datetime.date):
            date = the_date
        else:
            date = dateutil.parser.parse(the_date)
        if as_word:
            return(babel.dates.format_date(date, format='MMMM', locale=babel_language(language)))
        return(int(date.strftime('%m')))
    except:
        return word("Bad date")

def day_of(the_date, language=None):
    """Interprets the_date as a date and returns the day of month."""
    ensure_definition(the_date, language)
    try:
        if isinstance(the_date, datetime.datetime) or isinstance(the_date, datetime.date):
            date = the_date
        else:
            date = dateutil.parser.parse(the_date)
        return(int(date.strftime('%d')))
    except:
        return word("Bad date")

def dow_of(the_date, as_word=False, language=None):
    """Interprets the_date as a date and returns the day of week as a number from 1 to 7 for Sunday through Saturday.  Set as_word to True if you want the day of week as a word."""
    ensure_definition(the_date, as_word, language)
    if language is None:
        language = get_language()
    try:
        if isinstance(the_date, datetime.datetime) or isinstance(the_date, datetime.date):
            date = the_date
        else:
            date = dateutil.parser.parse(the_date)
        if as_word:
            return(babel.dates.format_date(date, format='EEEE', locale=babel_language(language)))
        else:
            return(int(date.strftime('%u')))
    except:
        return word("Bad date")

def year_of(the_date, language=None):
    """Interprets the_date as a date and returns the year."""
    ensure_definition(the_date, language)
    try:
        if isinstance(the_date, datetime.datetime) or isinstance(the_date, datetime.date):
            date = the_date
        else:
            date = dateutil.parser.parse(the_date)
        return(int(date.strftime('%Y')))
    except:
        return word("Bad date")

def format_date(the_date, format='long', language=None):
    """Interprets the_date as a date and returns the date formatted for the current locale."""
    ensure_definition(the_date, format, language)
    if language is None:
        language = get_language()
    if isinstance(the_date, DAEmpty):
        return ""
    try:
        if isinstance(the_date, datetime.datetime) or isinstance(the_date, datetime.date):
            date = the_date
        else:
            date = dateutil.parser.parse(the_date)
        return babel.dates.format_date(date, format=format, locale=babel_language(language))
    except:
        return word("Bad date")

def format_datetime(the_date, format='long', language=None):
    """Interprets the_date as a date/time and returns the date/time formatted for the current locale."""
    ensure_definition(the_date, format, language)
    if language is None:
        language = get_language()
    if isinstance(the_date, DAEmpty):
        return ""
    try:
        if isinstance(the_date, datetime.datetime) or isinstance(the_date, datetime.date):
            date = the_date
        else:
            date = dateutil.parser.parse(the_date)
        return babel.dates.format_datetime(date, format=format, locale=babel_language(language))
    except:
        return word("Bad date")

def format_time(the_time, format='short', language=None):
    """Interprets the_time as a date/time and returns the time formatted for the current locale."""
    ensure_definition(the_time, format, language)
    if language is None:
        language = get_language()
    if isinstance(the_time, DAEmpty):
        return ""
    try:
        if isinstance(the_time, datetime.datetime) or isinstance(the_time, datetime.date) or isinstance(the_time, datetime.time):
            time = the_time
        else:
            time = dateutil.parser.parse(the_time)
        return babel.dates.format_time(time, format=format, locale=babel_language(language))
    except Exception as errmess:
        return word("Bad date: " + text_type(errmess))

class DateTimeDelta(object):
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return text_type(self.describe())
    def describe(self, **kwargs):
        specificity = kwargs.get('specificity', None)
        output = list()
        diff = dateutil.relativedelta.relativedelta(self.end, self.start)
        if diff.years != 0:
            output.append((abs(diff.years), noun_plural(word('year'), abs(diff.years))))
        if diff.months != 0 and specificity != 'year':
            output.append((abs(diff.months), noun_plural(word('month'), abs(diff.months))))
        if diff.days != 0 and specificity not in ('year', 'month'):
            output.append((abs(diff.days), noun_plural(word('day'), abs(diff.days))))
        if kwargs.get('nice', True):
            return_value = comma_and_list(["%s %s" % (nice_number(y[0]), y[1]) for y in output])
            if kwargs.get('capitalize', False):
                return capitalize(return_value)
            else:
                return return_value
        else:
            return comma_and_list(["%d %s" % y for y in output])

class DADateTime(datetime.datetime):
    def format(self, format='long', language=None):
        return format_date(self, format=format, language=language)
    def format_date(self, format='long', language=None):
        return format_date(self, format=format, language=language)
    def format_datetime(self, format='long', language=None):
        return format_datetime(self, format=format, language=language)
    def format_time(self, format='short', language=None):
        return format_time(self, format=format, language=language)
    def replace_time(self, time):
        return self.replace(hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)
    @property
    def nanosecond(self):
        return 0
    @property
    def dow(self):
        return self.isocalendar()[2]
    @property
    def week(self):
        return self.isocalendar()[1]
    def plus(self, **kwargs):
        return dd(dt(self) + date_interval(**kwargs))
    def minus(self, **kwargs):
        return dd(dt(self) - date_interval(**kwargs))
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return text_type(format_date(self))
    def __add__(self, other):
        if isinstance(other, string_types):
            return text_type(self) + other
        val = dt(self) + other
        if isinstance(val, datetime.date):
            return dd(val)
        return val
    def __radd__(self, other):
        if isinstance(other, string_types):
            return other + text_type(self)
        return dd(dt(self) + other)
    def __sub__(self, other):
        val = dt(self) - other
        if isinstance(val, datetime.date):
            return dd(val)
        return val
    def __rsub__(self, other):
        val = other - dt(self)
        if isinstance(val, datetime.date):
            return dd(val)
        return val

def current_datetime(timezone=None):
    """Returns the current time.  Uses the default timezone unless another
    timezone is explicitly provided.

    """
    ensure_definition(timezone)
    if timezone is None:
        timezone = get_default_timezone()
    return dd(pytz.utc.localize(datetime.datetime.utcnow()).astimezone(pytz.timezone(timezone)))

def as_datetime(the_date, timezone=None):
    """Converts the_date to a DADateTime object with a timezone.  Uses the
    default timezone unless another timezone is explicitly provided."""
    ensure_definition(the_date, timezone)
    if timezone is None:
        timezone = get_default_timezone()
    if isinstance(the_date, datetime.date) and not isinstance(the_date, datetime.datetime):
        the_date = datetime.datetime.combine(the_date, datetime.datetime.min.time())
    if isinstance(the_date, datetime.datetime):
        new_datetime = the_date
    else:
        new_datetime = dateutil.parser.parse(the_date)
    if new_datetime.tzinfo:
        new_datetime = new_datetime.astimezone(pytz.timezone(timezone))
    else:
        new_datetime = pytz.timezone(timezone).localize(new_datetime)
    return dd(new_datetime)

def dd(obj):
    if isinstance(obj, DADateTime):
        return obj
    return DADateTime(obj.year, month=obj.month, day=obj.day, hour=obj.hour, minute=obj.minute, second=obj.second, microsecond=obj.microsecond, tzinfo=obj.tzinfo)

def dt(obj):
    return datetime.datetime(obj.year, obj.month, obj.day, obj.hour, obj.minute, obj.second, obj.microsecond, obj.tzinfo)

def date_interval(**kwargs):
    """Expresses a date and time interval.  Passes through all arguments
    to dateutil.relativedelta.relativedelta."""
    ensure_definition(**kwargs)
    return dateutil.relativedelta.relativedelta(**kwargs)

def date_difference(starting=None, ending=None, timezone=None):
    """Calculates the difference between the date indicated by "starting"
    and the date indicated by "ending."  Returns an object with attributes weeks,
    days, hours, minutes, seconds, and delta."""
    ensure_definition(starting, ending, timezone)
    if starting is None:
        starting = current_datetime()
    if ending is None:
        ending = current_datetime()
    if timezone is None:
        timezone = get_default_timezone()
    if isinstance(starting, datetime.date) and not isinstance(starting, datetime.datetime):
        starting = datetime.datetime.combine(starting, datetime.datetime.min.time())
    if isinstance(ending, datetime.date) and not isinstance(ending, datetime.datetime):
        ending = datetime.datetime.combine(ending, datetime.datetime.min.time())
    if not isinstance(starting, datetime.datetime):
        starting = dateutil.parser.parse(starting)
    if not isinstance(ending, datetime.datetime):
        ending = dateutil.parser.parse(ending)
    if starting.tzinfo:
        starting = starting.astimezone(pytz.timezone(timezone))
    else:
        starting = pytz.timezone(timezone).localize(starting)
    if ending.tzinfo:
        ending = ending.astimezone(pytz.timezone(timezone))
    else:
        ending = pytz.timezone(timezone).localize(ending)
    delta = ending - starting
    output = DateTimeDelta()
    output.start = starting
    output.end = ending
    output.weeks = (delta.days / 7.0) + (delta.seconds / 604800.0)
    output.days = delta.days + (delta.seconds / 86400.0)
    output.hours = (delta.days * 24.0) + (delta.seconds / 3600.0)
    output.minutes = (delta.days * 1440.0) + (delta.seconds / 60.0)
    output.seconds = (delta.days * 86400) + delta.seconds
    output.years = (delta.days + delta.seconds / 86400.0) / 365.2425
    return output

def fax_string(person, country=None):
    if person is None:
        return None
    fax_number = None
    if isinstance(person, Person):
        fax_number = person.facsimile_number(country=country)
    elif isinstance(person, phonenumbers.PhoneNumber):
        fax_number = phonenumbers.format_number(person, phonenumbers.PhoneNumberFormat.E164)
    else:
        fax_number = phone_number_in_e164(person, country=country)
    return fax_number

def phone_string(person, country=None):
    if person is None:
        return None
    phone_number = None
    if isinstance(person, Person):
        phone_number = person.sms_number()
    elif isinstance(person, phonenumbers.PhoneNumber):
        phone_number = phonenumbers.format_number(person, phonenumbers.PhoneNumberFormat.E164)
    else:
        phone_number = phone_number_in_e164(person, country=country)
    return phone_number

def email_string(persons, include_name=None, first=False):
    if persons is None:
        return None
    if not (isinstance(persons, (DAList, DASet, abc.Iterable)) and not isinstance(persons, string_types)):
        persons = [persons]
    result = []
    for person in persons:
        if isinstance(person, Person) or isinstance(person, DAEmailRecipient):
            result.append(person.email_address(include_name=include_name))
        else:
            result.append(text_type(person))
    result = [x for x in result if x is not None and x != '']
    if first:
        if len(result):
            return result[0]
        return None
    return result

def email_stringer(variable, first=False, include_name=False):
    return email_string(variable, include_name=include_name, first=first)

def valid_datetime(the_datetime):
    """Returns True if the provided text represents a valid date or time."""
    ensure_definition(the_datetime)
    if isinstance(the_datetime, datetime.date) or isinstance(the_datetime, datetime.time):
        return True
    try:
        dateutil.parser.parse(the_datetime)
        return True
    except:
        return False

def timezone_list():
    """Returns a list of timezone choices, expressed as text."""
    return sorted([tz for tz in pytz.all_timezones])

def returning_user(minutes=None, hours=None, days=None):
    """Returns True if the user is returning to the interview after six
    hours of inactivity, or other time indicated by the optional
    keyword arguments minutes, hours, or days.

    """
    if this_thread.current_info['method'] != 'GET':
        return False
    if minutes is not None and last_access_minutes() > minutes:
        return True
    if hours is not None and last_access_hours() > hours:
        return True
    if days is not None and last_access_days() > days:
        return True
    if last_access_hours() > 6.0:
        return True
    return False

def last_access_delta(*pargs, **kwargs):
    """Returns a datetime.timedelta object expressing the length of
    time that has passed since the last time the interview was accessed."""
    last_time = last_access_time(*pargs, **kwargs)
    if last_time is None:
        return datetime.timedelta(0)
    return current_datetime() - last_time

def last_access_days(*pargs, **kwargs):
    """Returns the number of days since the last time the interview
    was accessed."""
    delta = last_access_delta(*pargs, **kwargs)
    return delta.days + (delta.seconds / 86400.0)

def last_access_hours(*pargs, **kwargs):
    """Returns the number of hours since the last time the interview
    was accessed."""
    delta = last_access_delta(*pargs, **kwargs)
    return (delta.days * 24.0) + (delta.seconds / 3600.0)

def last_access_minutes(*pargs, **kwargs):
    """Returns the number of minutes since the last time the interview
    was accessed."""
    delta = last_access_delta(*pargs, **kwargs)
    return (delta.days * 1440.0) + (delta.seconds / 60.0)

def last_access_time(include_privileges=None, exclude_privileges=None, include_cron=False, timezone=None):
    """Returns the last time the interview was accessed, as a DADateTime object."""
    max_time = None
    if include_privileges is not None:
        if not isinstance(include_privileges, (list, tuple, dict)):
            if isinstance(include_privileges, DAObject) and hasattr(include_privileges, 'elements'):
                include_privileges = include_privileges.elements
            else:
                include_privileges = [include_privileges]
        if 'cron' in include_privileges:
            include_cron = True
    if exclude_privileges is not None:
        if not isinstance(exclude_privileges, (list, tuple, dict)):
            if isinstance(exclude_privileges, DAObject) and hasattr(exclude_privileges, 'elements'):
                exclude_privileges = exclude_privileges.elements
            else:
                exclude_privileges = [exclude_privileges]
    else:
        exclude_privileges = list()
    for user_id, access_time in this_thread.internal['accesstime'].items():
        if user_id == -1:
            if 'anonymous' in exclude_privileges:
                continue
            if include_privileges is None or 'anonymous' in include_privileges:
                if max_time is None or max_time < access_time:
                    max_time = access_time
                    break
        else:
            user_object = server.get_user_object(user_id)
            if user_object is not None and hasattr(user_object, 'roles'):
                if len(user_object.roles) == 0:
                    if 'user' in exclude_privileges:
                        continue
                    if include_privileges is None or 'user' in include_privileges:
                        if max_time is None or max_time < access_time:
                            max_time = access_time
                            break
                else:
                    for role in user_object.roles:
                        if (include_cron is False and role.name == 'cron') or role.name in exclude_privileges:
                            continue
                        if include_privileges is None or role.name in include_privileges:
                            if max_time is None or max_time < access_time:
                                max_time = access_time
                                break
    if max_time is None:
        return None
    if timezone is not None:
        return dd(pytz.utc.localize(max_time).astimezone(pytz.timezone(timezone)))
    else:
        return dd(pytz.utc.localize(max_time).astimezone(pytz.utc))

def start_time(timezone=None):
    """Returns the time the interview was started, as a DADateTime object."""
    if timezone is not None:
        return dd(pytz.utc.localize(this_thread.internal['starttime']).astimezone(pytz.timezone(timezone)))
    else:
        return dd(pytz.utc.localize(this_thread.internal['starttime']).astimezone(pytz.utc))

class LatitudeLongitude(DAObject):
    """Represents a GPS location."""
    def init(self, *pargs, **kwargs):
        self.gathered = False
        self.known = False
        # self.description = ""
        return super(LatitudeLongitude, self).init(*pargs, **kwargs)
    def status(self):
        """Returns True or False depending on whether an attempt has yet been made
        to gather the latitude and longitude."""
        #logmessage("got to status")
        if self.gathered:
            #logmessage("gathered is true")
            return False
        else:
            if location_returned():
                #logmessage("returned is true")
                self._set_to_current()
                return False
            else:
                return True
    def _set_to_current(self):
        #logmessage("set to current")
        if 'user' in this_thread.current_info and 'location' in this_thread.current_info['user'] and isinstance(this_thread.current_info['user']['location'], dict):
            if 'latitude' in this_thread.current_info['user']['location'] and 'longitude' in this_thread.current_info['user']['location']:
                self.latitude = this_thread.current_info['user']['location']['latitude']
                self.longitude = this_thread.current_info['user']['location']['longitude']
                self.known = True
                #logmessage("known is true")
            elif 'error' in this_thread.current_info['user']['location']:
                self.error = this_thread.current_info['user']['location']['error']
                self.known = False
                #logmessage("known is false")
            self.gathered = True
            self.description = text_type(self)
        return
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        if hasattr(self, 'latitude') and hasattr(self, 'longitude'):
            return text_type(self.latitude) + ', ' + text_type(self.longitude)
        elif hasattr(self, 'error'):
            return text_type(self.error)
        return u'Unknown'

class RoleChangeTracker(DAObject):
    """Used within an interview to facilitate changes in the active role
    required for filling in interview information.  Ensures that participants
    do not receive multiple e-mails needlessly."""
    def init(self, *pargs, **kwargs):
        self.last_role = None
        return
    # def should_send_email(self):
    #     """Returns True or False depending on whether an e-mail will be sent on
    #     role change"""
    #     return True
    def _update(self, target_role):
        """When a notification is delivered about a necessary change in the
        active role of the interviewee, this function is called with
        the name of the new role.  This prevents the send_email()
        function from sending duplicative notifications."""
        self.last_role = target_role
        return
    def send_email(self, roles_needed, **kwargs):
        """Sends a notification e-mail if necessary because of a change in the
        active of the interviewee.  Returns True if an e-mail was
        successfully sent.  Otherwise, returns False.  False could
        mean that it was not necessary to send an e-mail."""
        #logmessage("Current role is " + str(this_thread.global_vars.role))
        for role_option in kwargs:
            if 'to' in kwargs[role_option]:
                need(kwargs[role_option]['to'].email)
        for role_needed in roles_needed:
            #logmessage("One role needed is " + str(role_needed))
            if role_needed == self.last_role:
                #logmessage("Already notified new role " + str(role_needed))
                return False
            if role_needed in kwargs:
                #logmessage("I have info on " + str(role_needed))
                email_info = kwargs[role_needed]
                if 'to' in email_info and 'email' in email_info:
                    #logmessage("I have email info on " + str(role_needed))
                    try:
                        result = send_email(to=email_info['to'], html=email_info['email'].content, subject=email_info['email'].subject)
                    except DAError:
                        result = False
                    if result:
                        self._update(role_needed)
                    return result
        return False

class Name(DAObject):
    """Base class for an object's name."""
    def full(self):
        """Returns the full name."""
        return(self.text)
    def firstlast(self):
        """This method is included for compatibility with other types of names."""
        return(self.text)
    def lastfirst(self):
        """This method is included for compatibility with other types of names."""
        return(self.text)
    def defined(self):
        """Returns True if the name has been defined.  Otherwise, returns False."""
        return hasattr(self, 'text')
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return(text_type(self.full()))
#    def __repr__(self):
#        return(repr(self.full()))

class IndividualName(Name):
    """The name of an Individual."""
    def init(self, *pargs, **kwargs):
        if 'uses_parts' not in kwargs:
            self.uses_parts = True
        return super(IndividualName, self).init(*pargs, **kwargs)
    def defined(self):
        """Returns True if the name has been defined.  Otherwise, returns False."""
        if not self.uses_parts:
            return super(IndividualName, self).defined()
        return hasattr(self, 'first')
    def full(self, middle='initial', use_suffix=True):
        """Returns the full name.  Has optional keyword arguments middle
        and use_suffix."""
        if not self.uses_parts:
            return super(IndividualName, self).full()
        names = [self.first]
        if hasattr(self, 'middle') and len(self.middle):
            if middle is False or middle is None:
                pass
            elif middle == 'initial':
                names.append(self.middle[0] + '.')
            else:
                names.append(self.middle)
        if hasattr(self, 'last') and len(self.last):
            names.append(self.last)
        else:
            if hasattr(self, 'paternal_surname'):
                names.append(self.paternal_surname)
            if hasattr(self, 'maternal_surname'):
                names.append(self.maternal_surname)
        if hasattr(self, 'suffix') and use_suffix and len(self.suffix):
            names.append(self.suffix)
        return(" ".join(names))
    def firstlast(self):
        """Returns the first name followed by the last name."""
        if not self.uses_parts:
            return super(IndividualName, self).firstlast()
        return(self.first + " " + self.last)
    def lastfirst(self):
        """Returns the last name followed by a comma, followed by the
        last name, followed by the suffix (if a suffix exists)."""
        if not self.uses_parts:
            return super(IndividualName, self).lastfirst()
        output = self.last
        if hasattr(self, 'suffix') and self.suffix:
            output += " " + self.suffix
        output += ", " + self.first
        if hasattr(self, 'middle') and self.middle:
            output += " " + self.middle[0] + '.'
        return output

class Address(DAObject):
    """A geographic address."""
    def init(self, *pargs, **kwargs):
        if 'location' not in kwargs:
            self.initializeAttribute('location', LatitudeLongitude)
        if 'geolocated' not in kwargs:
            self.geolocated = False
        if not hasattr(self, 'city_only'):
            self.city_only = False
        return super(Address, self).init(*pargs, **kwargs)
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return(text_type(self.block()))
    def on_one_line(self, include_unit=False, omit_default_country=True, language=None):
        """Returns a one-line address.  Primarily used internally for geolocation."""
        output = ""
        if self.city_only is False:
            if (not hasattr(self, 'address')) and hasattr(self, 'street_number') and hasattr(self, 'street'):
                output += text_type(self.street_number) + " " + text_type(self.street)
            else:
                output += text_type(self.address)
            if include_unit:
                the_unit = self.formatted_unit(language=language)
                if the_unit != '':
                    output += ", " + the_unit
            output += ", "
        #if hasattr(self, 'sublocality') and self.sublocality:
        #    output += text_type(self.sublocality) + ", "
        if hasattr(self, 'sublocality_level_1') and self.sublocality_level_1:
            if not (hasattr(self, 'street_number') and self.street_number == self.sublocality_level_1):
                output += text_type(self.sublocality_level_1) + ", "
        output += text_type(self.city)
        if hasattr(self, 'state') and self.state:
            output += ", " + text_type(self.state)
        if hasattr(self, 'zip') and self.zip:
            output += " " + text_type(self.zip)
        elif hasattr(self, 'postal_code') and self.postal_code:
            output += " " + text_type(self.postal_code)
        if hasattr(self, 'country') and self.country:
            if (not omit_default_country) or get_country() != self.country:
                output += ", " + country_name(self.country)
        elif omit_default_country is False:
            output += ", " + country_name(get_country())
        return output
    def _map_info(self):
        if (self.location.gathered and self.location.known) or self.geolocate():
            if hasattr(self.location, 'description'):
                the_info = self.location.description
            else:
                the_info = ''
            result = {'latitude': self.location.latitude, 'longitude': self.location.longitude, 'info': the_info}
            if hasattr(self, 'icon'):
                result['icon'] = self.icon
            return [result]
        return None
    def geolocate(self, address=None):
        """Determines the latitude and longitude of the location from its components.  If an address is supplied, the address fields that are not already populated will be populated with the result of the geolocation of the selected address."""
        if address is None:
            if self.geolocated:
                return self.geolocate_success
            the_address = self.on_one_line(include_unit=True, omit_default_country=False)
        else:
            the_address = address
        #logmessage("geolocate: trying to geolocate " + str(the_address))
        from geopy.geocoders import GoogleV3
        if 'google' in server.daconfig and 'api key' in server.daconfig['google'] and server.daconfig['google']['api key']:
            my_geocoder = GoogleV3(api_key=server.daconfig['google']['api key'])
        else:
            my_geocoder = GoogleV3()
        try_number = 0
        success = False
        results = None
        while not success and try_number < 2:
            try:
                results = my_geocoder.geocode(the_address)
                success = True
            except Exception as the_err:
                logmessage(text_type(the_err))
                try_number += 1
                time.sleep(try_number)
        self.geolocated = True
        if results:
            self.geolocate_success = True
            self.location.gathered = True
            self.location.known = True
            self.location.latitude = results.latitude
            self.location.longitude = results.longitude
            self.geolocate_response = results.raw
            if hasattr(self, 'norm'):
                delattr(self, 'norm')
            if hasattr(self, 'norm_long'):
                delattr(self, 'norm_long')
            self.initializeAttribute('norm', self.__class__)
            self.initializeAttribute('norm_long', self.__class__)
            if 'formatted_address' in results.raw:
                self.one_line = results.raw['formatted_address']
                self.norm.one_line = results.raw['formatted_address']
                self.norm_long.one_line = results.raw['formatted_address']
            if 'address_components' in results.raw:
                geo_types = {
                    'administrative_area_level_1': ('state', 'short_name'),
                    'administrative_area_level_2': ('county', 'long_name'),
                    'administrative_area_level_3': ('administrative_area_level_3', 'long_name'),
                    'administrative_area_level_4': ('administrative_area_level_4', 'long_name'),
                    'administrative_area_level_5': ('administrative_area_level_5', 'long_name'),
                    'colloquial_area': ('colloquial_area', 'long_name'),
                    'country': ('country', 'short_name'),
                    'floor': ('floor', 'long_name'),
                    'intersection': ('intersection', 'long_name'),
                    'locality': ('city', 'long_name'),
                    'neighborhood': ('neighborhood', 'long_name'),
                    'post_box': ('post_box', 'long_name'),
                    'postal_code': ('zip', 'long_name'),
                    'postal_code_prefix': ('postal_code_prefix', 'long_name'),
                    'postal_code_suffix': ('postal_code_suffix', 'long_name'),
                    'postal_town': ('postal_town', 'long_name'),
                    'premise': ('premise', 'long_name'),
                    'room': ('room', 'long_name'),
                    'route': ('street', 'short_name'),
                    'street_number': ('street_number', 'short_name'),
                    'sublocality': ('sublocality', 'long_name'),
                    'sublocality_level_1': ('sublocality_level_1', 'long_name'),
                    'sublocality_level_2': ('sublocality_level_2', 'long_name'),
                    'sublocality_level_3': ('sublocality_level_3', 'long_name'),
                    'sublocality_level_4': ('sublocality_level_4', 'long_name'),
                    'sublocality_level_5': ('sublocality_level_5', 'long_name'),
#                    'subpremise': ('unit', 'long_name'),
                }
                for component in results.raw['address_components']:
                    if 'types' in component and 'long_name' in component:
                        for geo_type, addr_type in geo_types.items():
                            if geo_type in component['types'] and ((not hasattr(self, addr_type[0])) or getattr(self, addr_type[0]) == '' or getattr(self, addr_type[0]) is None):
                                setattr(self, addr_type[0], component[addr_type[1]])
                        if (not hasattr(self, geo_type)) or getattr(self, geo_type) == '' or getattr(self, geo_type) is None:
                            setattr(self, geo_type, component['long_name'])
                geo_types = {
                    'administrative_area_level_1': 'state',
                    'administrative_area_level_2': 'county',
                    'administrative_area_level_3': 'administrative_area_level_3',
                    'administrative_area_level_4': 'administrative_area_level_4',
                    'administrative_area_level_5': 'administrative_area_level_5',
                    'colloquial_area': 'colloquial_area',
                    'country': 'country',
                    'floor': 'floor',
                    'intersection': 'intersection',
                    'locality': 'city',
                    'neighborhood': 'neighborhood',
                    'post_box': 'post_box',
                    'postal_code': 'zip',
                    'postal_code_prefix': 'postal_code_prefix',
                    'postal_code_suffix': 'postal_code_suffix',
                    'postal_town': 'postal_town',
                    'premise': 'premise',
                    'room': 'room',
                    'route': 'street',
                    'street_number': 'street_number',
                    'sublocality': 'sublocality',
                    'sublocality_level_1': 'sublocality_level_1',
                    'sublocality_level_2': 'sublocality_level_2',
                    'sublocality_level_3': 'sublocality_level_3',
                    'sublocality_level_4': 'sublocality_level_4',
                    'sublocality_level_5': 'sublocality_level_5',
#                    'subpremise': 'unit'
                }
                for component in results.raw['address_components']:
                    if 'types' in component:
                        for geo_type, addr_type in geo_types.items():
                            if geo_type in component['types']:
                                if 'short_name' in component:
                                    setattr(self.norm, addr_type, component['short_name'])
                                    if addr_type != geo_type:
                                        setattr(self.norm, geo_type, component['short_name'])
                                if 'long_name' in component:
                                    setattr(self.norm_long, addr_type, component['long_name'])
                                    if addr_type != geo_type:
                                        setattr(self.norm_long, geo_type, component['long_name'])
                if hasattr(self.norm, 'unit'):
                    self.norm.unit = '#' + text_type(self.norm.unit)
                if hasattr(self.norm_long, 'unit'):
                    self.norm_long.unit = '#' + text_type(self.norm_long.unit)
                if hasattr(self.norm, 'street_number') and hasattr(self.norm, 'street'):
                    self.norm.address = self.norm.street_number + " " + self.norm.street
                if hasattr(self.norm_long, 'street_number') and hasattr(self.norm_long, 'street'):
                    self.norm_long.address = self.norm_long.street_number + " " + self.norm_long.street
                if (not hasattr(self.norm, 'city')) and hasattr(self.norm, 'administrative_area_level_3'):
                    self.norm.city = self.norm.administrative_area_level_3
                if (not hasattr(self.norm_long, 'city')) and hasattr(self.norm_long, 'administrative_area_level_3'):
                    self.norm_long.city = self.norm_long.administrative_area_level_3
                if (not hasattr(self.norm, 'city')) and hasattr(self.norm, 'neighborhood'):
                    self.norm.city = self.norm.neighborhood
                if (not hasattr(self.norm_long, 'city')) and hasattr(self.norm_long, 'neighborhood'):
                    self.norm_long.city = self.norm_long.neighborhood
            self.norm.geolocated = True
            self.norm.location.gathered = True
            self.norm.location.known = True
            self.norm.location.latitude = results.latitude
            self.norm.location.longitude = results.longitude
            try:
                self.norm.location.description = self.norm.block()
            except:
                logmessage("Normalized address was incomplete")
                self.geolocate_success = False
            self.norm.geolocate_response = results.raw
            self.norm_long.geolocated = True
            self.norm_long.location.gathered = True
            self.norm_long.location.known = True
            self.norm_long.location.latitude = results.latitude
            self.norm_long.location.longitude = results.longitude
            try:
                self.norm_long.location.description = self.norm_long.block()
            except:
                logmessage("Normalized address was incomplete")
                self.geolocate_success = False
            self.norm_long.geolocate_response = results.raw
            if address is not None:
                self.normalize()
            try:
                self.location.description = self.block()
            except:
                self.location.description = ''
        else:
            logmessage("geolocate: Valid not ok.")
            self.geolocate_success = False
        #logmessage(str(self.__dict__))
        return self.geolocate_success
    def normalize(self, long_format=False):
        if not self.geolocate():
            return False
        the_instance_name = self.instanceName
        the_norm = self.norm
        the_norm_long = self.norm_long
        if long_format:
            target = copy.deepcopy(the_norm_long)
        else:
            target = copy.deepcopy(the_norm)
        for name in target.__dict__:
            setattr(self, name, getattr(target, name))
        self._set_instance_name_recursively(the_instance_name)
        self.norm = the_norm
        self.norm_long = the_norm_long
        return True
    def block(self, language=None):
        """Returns the address formatted as a block, as in a mailing."""
        output = ""
        if this_thread.evaluation_context == 'docx':
            line_breaker = '</w:t><w:br/><w:t xml:space="preserve">'
        else:
            line_breaker = " [NEWLINE] "
        if self.city_only is False:
            if (not hasattr(self, 'address')) and hasattr(self, 'street_number') and hasattr(self, 'street'):
                output += text_type(self.street_number) + " " + text_type(self.street) + line_breaker
            else:
                output += text_type(self.address) + line_breaker
            the_unit = self.formatted_unit(language=language)
            if the_unit != '':
                output += the_unit + line_breaker
        if hasattr(self, 'sublocality_level_1') and self.sublocality_level_1:
            output += text_type(self.sublocality_level_1) + line_breaker
        output += text_type(self.city)
        if hasattr(self, 'state') and self.state:
            output += ", " + text_type(self.state)
        if hasattr(self, 'zip'):
            output += " " + text_type(self.zip)
        elif hasattr(self, 'postal_code') and self.postal_code:
            output += " " + text_type(self.postal_code)
        return(output)
    def formatted_unit(self, language=None, require=False):
        """Returns the unit, formatted appropriately"""
        if not hasattr(self, 'unit') and not hasattr(self, 'floor') and not hasattr(self, 'room'):
            if require:
                self.unit
            else:
                return ''
        if hasattr(self, 'unit') and self.unit != '' and self.unit is not None:
            if not re.search(r'unit|floor|suite|apt|apartment|room|ste|fl', text_type(self.unit), flags=re.IGNORECASE):
                return word("Unit", language=language) + " " + text_type(self.unit)
            else:
                return text_type(self.unit)
        elif hasattr(self, 'floor') and self.floor != '' and self.floor is not None:
            return word("Floor", language=language) + " " + text_type(self.floor)
        elif hasattr(self, 'room') and self.room != '' and self.room is not None:
            return word("Room", language=language) + " " + text_type(self.room)
        return ''
    def line_one(self, language=None):
        """Returns the first line of the address, including the unit
        number if there is one."""
        if self.city_only:
            return ''
        if (not hasattr(self, 'address')) and hasattr(self, 'street_number') and hasattr(self, 'street'):
            output += text_type(self.street_number) + " " + text_type(self.street)
        else:
            output = text_type(self.address)
        the_unit = self.formatted_unit(language=language)
        if the_unit != '':
            output += ", " + the_unit
        return(output)
    def line_two(self, language=None):
        """Returns the second line of the address, including the city,
        state and zip code."""
        output = ""
        #if hasattr(self, 'sublocality') and self.sublocality:
        #    output += text_type(self.sublocality) + ", "
        if hasattr(self, 'sublocality_level_1') and self.sublocality_level_1:
            output += text_type(self.sublocality_level_1) + ", "
        output += text_type(self.city)
        if hasattr(self, 'state') and self.state:
            output += ", " + text_type(self.state)
        if hasattr(self, 'zip') and self.zip:
            output += " " + text_type(self.zip)
        elif hasattr(self, 'postal_code') and self.postal_code:
            output += " " + text_type(self.postal_code)
        return(output)

class City(Address):
    """A geographic address specific only to a city."""
    def init(self, *pargs, **kwargs):
        self.city_only = True
        return super(City, self).init(*pargs, **kwargs)

class Thing(DAObject):
    """Represents something with a name."""
    def init(self, *pargs, **kwargs):
        if not hasattr(self, 'name') and 'name' not in kwargs:
            self.name = Name()
        if 'name' in kwargs and isinstance(kwargs['name'], string_types):
            if not hasattr(self, 'name'):
                self.name = Name()
            self.name.text = kwargs['name']
            del kwargs['name']
        return super(Thing, self).init(*pargs, **kwargs)
    def __setattr__(self, attrname, value):
        if attrname == 'name' and isinstance(value, string_types):
            self.name.text = value
        else:
            return super(Thing, self).__setattr__(attrname, value)
    def __unicode__(self):
        return text_type(self.name.full())
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()

class Event(DAObject):
    """A DAObject with pre-set attributes address, which is a City, and
    location, which is a LatitudeLongitude.

    """
    def init(self, *pargs, **kwargs):
        if 'address' not in kwargs:
            self.address = City()
        if 'location' not in kwargs:
            self.initializeAttribute('location', LatitudeLongitude)
        return super(Event, self).init(*pargs, **kwargs)
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return text_type(self.address)

class Person(DAObject):
    """Represents a legal or natural person."""
    def init(self, *pargs, **kwargs):
        if not hasattr(self, 'name') and 'name' not in kwargs:
            self.name = Name()
        if 'address' not in kwargs:
            self.initializeAttribute('address', Address)
        if 'location' not in kwargs:
            self.initializeAttribute('location', LatitudeLongitude)
        if 'name' in kwargs and isinstance(kwargs['name'], string_types):
            if not hasattr(self, 'name'):
                self.name = Name()
            self.name.text = kwargs['name']
            del kwargs['name']
        # if 'roles' not in kwargs:
        #     self.roles = set()
        return super(Person, self).init(*pargs, **kwargs)
    def _map_info(self):
        if not self.location.known:
            if (self.address.location.gathered and self.address.location.known) or self.address.geolocate():
                self.location = self.address.location
        if self.location.gathered and self.location.known:
            if self.name.defined():
                the_info = self.name.full()
            else:
                the_info = capitalize(self.object_name())
            if hasattr(self.location, 'description') and self.location.description != '':
                the_info += " [NEWLINE] " + self.location.description
            result = {'latitude': self.location.latitude, 'longitude': self.location.longitude, 'info': the_info}
            if hasattr(self, 'icon'):
                result['icon'] = self.icon
            elif self is this_thread.global_vars.user:
                result['icon'] = {'path': 'CIRCLE', 'scale': 5, 'strokeColor': 'blue'}
            return [result]
        return None
    def identified(self):
        """Returns True if the person's name has been set.  Otherwise, returns False."""
        if hasattr(self.name, 'text'):
            return True
        return False
    def __setattr__(self, attrname, value):
        if attrname == 'name' and isinstance(value, string_types):
            self.name.text = value
        else:
            return super(Person, self).__setattr__(attrname, value)
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return text_type(self.name.full())
    def pronoun_objective(self, **kwargs):
        """Returns "it" or "It" depending on the value of the optional
        keyword argument "capitalize." """
        output = word('it', **kwargs)
        if 'capitalize' in kwargs and kwargs['capitalize']:
            return(capitalize(output))
        else:
            return(output)
    def possessive(self, target, **kwargs):
        """Given a word like "fish," returns "your fish" or
        "John Smith's fish," depending on whether the person is the user."""
        if self is this_thread.global_vars.user:
            return your(target, **kwargs)
        else:
            return possessify(self.name, target, **kwargs)
    def object_possessive(self, target, **kwargs):
        """Given a word, returns a phrase indicating possession, but
        uses the variable name rather than the object's actual name."""
        if self is this_thread.global_vars.user:
            return your(target, **kwargs)
        return super(Person, self).object_possessive(target, **kwargs)
    def is_are_you(self, **kwargs):
        """Returns "are you" if the object is the user, otherwise returns
        "is" followed by the object name."""
        if self is this_thread.global_vars.user:
            output = word('are you', **kwargs)
        else:
            output = is_word(self.name.full(), **kwargs)
        if 'capitalize' in kwargs and kwargs['capitalize']:
            return(capitalize(output))
        else:
            return(output)
    def is_user(self):
        """Returns True if the person is the user, otherwise False."""
        return self is this_thread.global_vars.user
    def address_block(self, language=None):
        """Returns the person name address as a block, for use in mailings."""
        if this_thread.evaluation_context == 'docx':
            return(self.name.full() + '</w:t><w:br/><w:t xml:space="preserve">' + self.address.block(language=language))
        else:
            return("[FLUSHLEFT] " + self.name.full() + " [NEWLINE] " + self.address.block(language=language))
    def sms_number(self):
        """Returns the person's mobile_number, if defined, otherwise the phone_number."""
        if hasattr(self, 'mobile_number'):
            the_number = self.mobile_number
            if hasattr(self, 'uses_whatsapp'):
                the_number = 'whatsapp:' + text_type(self.mobile_number)
        else:
            the_number = self.phone_number
        if hasattr(self, 'country'):
            the_country = self.country
        elif hasattr(self, 'address') and hasattr(self.address, 'country'):
            the_country = self.address.country
        else:
            the_country = get_country()
        return phone_number_in_e164(the_number, country=the_country)
    def facsimile_number(self, country=None):
        """Returns the person's fax_number, formatted appropriately."""
        the_number = self.fax_number
        if country is not None:
            the_country = country
        elif hasattr(self, 'country'):
            the_country = self.country
        elif hasattr(self, 'address') and hasattr(self.address, 'country'):
            the_country = self.address.country
        else:
            the_country = get_country()
        return phone_number_in_e164(the_number, country=the_country)
    def email_address(self, include_name=None):
        """Returns an e-mail address for the person."""
        if include_name is True or (include_name is not False and self.name.defined()):
            return('"' + nodoublequote(self.name) + '" <' + str(self.email) + '>')
        return(str(self.email))
    # def age(self):
    #     if (hasattr(self, 'age_in_years')):
    #         return self.age_in_years
    #     today = date.today()
    #     born = self.birthdate
    #     try:
    #         birthday = born.replace(year=today.year)
    #     except ValueError:
    #         birthday = born.replace(year=today.year, month=born.month+1, day=1)
    #     if birthday > today:
    #         return today.year - born.year - 1
    #     else:
    #         return today.year - born.year
    def do_question(self, the_verb, **kwargs):
        """Given a verb like "eat," returns "do you eat" or "does John Smith eat,"
        depending on whether the person is the user."""
        if self == this_thread.global_vars.user:
            return(do_you(the_verb, **kwargs))
        else:
            return(does_a_b(self.name, the_verb, **kwargs))
    def did_question(self, the_verb, **kwargs):
        """Given a verb like "eat," returns "did you eat" or "did John Smith eat,"
        depending on whether the person is the user."""
        if self == this_thread.global_vars.user:
            return did_you(the_verb, **kwargs)
        else:
            return did_a_b(self.name, the_verb, **kwargs)
    def were_question(self, the_target, **kwargs):
        """Given a target like "married", returns "were you married" or "was
        John Smith married," depending on whether the person is the
        user."""
        if self == this_thread.global_vars.user:
            return were_you(the_target, **kwargs)
        else:
            return was_a_b(self.name, the_target, **kwargs)
    def have_question(self, the_target, **kwargs):
        """Given a target like "", returns "have you married" or "has
        John Smith married," depending on whether the person is the
        user."""
        if self == this_thread.global_vars.user:
            return have_you(the_target, **kwargs)
        else:
            return has_a_b(self.name, the_target, **kwargs)
    def does_verb(self, the_verb, **kwargs):
        """Given a verb like "eat," returns "eat" or "eats"
        depending on whether the person is the user."""
        if self == this_thread.global_vars.user:
            tense = '1sg'
        else:
            tense = '3sg'
        if ('past' in kwargs and kwargs['past'] == True) or ('present' in kwargs and kwargs['present'] == False):
            return verb_past(the_verb, tense, **kwargs)
        else:
            return verb_present(the_verb, tense, **kwargs)
    def did_verb(self, the_verb, **kwargs):
        """Like does_verb(), except uses the past tense of the verb."""
        if self == this_thread.global_vars.user:
            tense = "2sgp"
        else:
            tense = "3sgp"
        #logmessage(the_verb + " " + tense)
        output = verb_past(the_verb, tense, **kwargs)
    def subject(self, **kwargs):
        """Returns "you" or the person's name, depending on whether the
        person is the user."""
        if self == this_thread.global_vars.user:
            output = word('you', **kwargs)
        else:
            output = text_type(self)
        if 'capitalize' in kwargs and kwargs['capitalize']:
            return(capitalize(output))
        else:
            return(output)

class Individual(Person):
    """Represents a natural person."""
    def init(self, *pargs, **kwargs):
        if 'name' not in kwargs and not hasattr(self, 'name'):
            self.name = IndividualName()
        # if 'child' not in kwargs and not hasattr(self, 'child'):
        #     self.child = ChildList()
        # if 'income' not in kwargs and not hasattr(self, 'income'):
        #     self.income = Income()
        # if 'asset' not in kwargs and not hasattr(self, 'asset'):
        #     self.asset = Asset()
        # if 'expense' not in kwargs and not hasattr(self, 'expense'):
        #     self.expense = Expense()
        if (not hasattr(self, 'name')) and 'name' in kwargs and isinstance(kwargs['name'], string_types):
            self.name = IndividualName()
            self.name.uses_parts = False
            self.name.text = kwargs['name']
        return super(Individual, self).init(*pargs, **kwargs)
    def get_parents(self, tree, create=False):
        return self.get_relation('child', tree, create=create)
    def get_spouse(self, tree, create=False):
        return self.get_peer_relation('spouse', tree, create=create)
    def set_spouse(self, target, tree):
        return self.set_peer_relationship(self, target, "spouse", tree, replace=True)
    def is_spouse_of(self, target, tree):
        return self.is_peer_relation(target, 'spouse', tree)
    def gather_family(self, tree, up=1, down=1):
        pass
    def identified(self):
        """Returns True if the individual's name has been set.  Otherwise, returns False."""
        if hasattr(self.name, 'first'):
            return True
        return False
    def age_in_years(self, decimals=False, as_of=None):
        """Returns the individual's age in years, based on self.birthdate."""
        if hasattr(self, 'age'):
            if decimals:
                return float(self.age)
            else:
                return int(self.age)
        if as_of is None:
            comparator = current_datetime()
        else:
            comparator = as_datetime(as_of)
        birth_date = as_datetime(self.birthdate)
        rd = dateutil.relativedelta.relativedelta(comparator, birth_date)
        if decimals:
            return float(rd.years)
        else:
            return int(rd.years)
    def first_name_hint(self):
        """If the individual is the user and the user is logged in and
        the user has set up a name in the user profile, this returns
        the user's first name.  Otherwise, returns a blank string."""
        if self is this_thread.global_vars.user and this_thread.current_info['user']['is_authenticated'] and 'firstname' in this_thread.current_info['user'] and this_thread.current_info['user']['firstname']:
            return this_thread.current_info['user']['firstname'];
        return ''
    def last_name_hint(self):
        """If the individual is the user and the user is logged in and
        the user has set up a name in the user profile, this returns
        the user's last name.  Otherwise, returns a blank string."""
        if self is this_thread.global_vars.user and this_thread.current_info['user']['is_authenticated'] and 'lastname' in this_thread.current_info['user'] and this_thread.current_info['user']['lastname']:
            return this_thread.current_info['user']['lastname'];
        return ''
    def salutation(self, **kwargs):
        """Returns "Mr.", "Ms.", etc."""
        return salutation(self, **kwargs)
    def pronoun_possessive(self, target, **kwargs):
        """Given a word like "fish," returns "her fish" or "his fish," as appropriate."""
        if self == this_thread.global_vars.user and ('thirdperson' not in kwargs or not kwargs['thirdperson']):
            output = your(target, **kwargs)
        elif self.gender == 'female':
            output = her(target, **kwargs)
        elif self.gender == 'other':
            output = their(target, **kwargs)
        else:
            output = his(target, **kwargs)
        if 'capitalize' in kwargs and kwargs['capitalize']:
            return(capitalize(output))
        else:
            return(output)
    def pronoun(self, **kwargs):
        """Returns a pronoun like "you," "her," or "him," as appropriate."""
        if self == this_thread.global_vars.user:
            output = word('you', **kwargs)
        if self.gender == 'female':
            output = word('her', **kwargs)
        elif self.gender == 'other':
            output = word('them', **kwargs)
        else:
            output = word('him', **kwargs)
        if 'capitalize' in kwargs and kwargs['capitalize']:
            return(capitalize(output))
        else:
            return(output)
    def pronoun_objective(self, **kwargs):
        """Same as pronoun()."""
        return self.pronoun(**kwargs)
    def pronoun_subjective(self, **kwargs):
        """Returns a pronoun like "you," "she," or "he," as appropriate."""
        if self == this_thread.global_vars.user and ('thirdperson' not in kwargs or not kwargs['thirdperson']):
            output = word('you', **kwargs)
        elif self.gender == 'female':
            output = word('she', **kwargs)
        elif self.gender == 'other':
            output = word('they', **kwargs)
        else:
            output = word('he', **kwargs)
        if 'capitalize' in kwargs and kwargs['capitalize']:
            return(capitalize(output))
        else:
            return(output)
    def yourself_or_name(self, **kwargs):
        """Returns a "yourself" if the individual is the user, otherwise
        returns the individual's name."""
        if self == this_thread.global_vars.user:
            output = word('yourself', **kwargs)
        else:
            output = self.name.full()
        if 'capitalize' in kwargs and kwargs['capitalize']:
            return(capitalize(output))
        else:
            return(output)
    def __setattr__(self, attrname, value):
        if attrname == 'name' and isinstance(value, string_types):
            if isinstance(self.name, IndividualName):
                self.name.uses_parts = False
            self.name.text = value
        else:
            return super(Individual, self).__setattr__(attrname, value)

class ChildList(DAList):
    """Represents a list of children."""
    def init(self, *pargs, **kwargs):
        self.object_type = Individual
        return super(ChildList, self).init(*pargs, **kwargs)

class FinancialList(DADict):
    """Represents a set of currency amounts."""
    def init(self, *pargs, **kwargs):
        self.object_type = Value
        return super(FinancialList, self).init(*pargs, **kwargs)
    def total(self):
        """Returns the total value in the list, gathering the list items if necessary."""
        self._trigger_gather()
        result = 0
        for item in sorted(self.elements.keys()):
            if self[item].exists:
                result += Decimal(self[item].value)
        return(result)
    def existing_items(self):
        """Returns a list of types of amounts that exist within the financial list."""
        self._trigger_gather()
        return [key for key in sorted(self.elements.keys()) if self[key].exists]
    def _new_item_init_callback(self):
        self.elements[self.new_item_name].exists = True
        if hasattr(self, 'new_item_value'):
            self.elements[self.new_item_name].value = self.new_item_value
            del self.new_item_value
        return super(FinancialList, self)._new_item_init_callback()
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return text_type(self.total())

class PeriodicFinancialList(FinancialList):
    """Represents a set of currency items, each of which has an associated period."""
    def init(self, *pargs, **kwargs):
        self.object_type = PeriodicValue
        return super(FinancialList, self).init(*pargs, **kwargs)
    def total(self, period_to_use=1):
        """Returns the total periodic value in the list, gathering the list items if necessary."""
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        for item in sorted(self.elements.keys()):
            if self.elements[item].exists:
                result += Decimal(self.elements[item].value) * Decimal(self.elements[item].period)
        return(result/Decimal(period_to_use))
    def _new_item_init_callback(self):
        if hasattr(self, 'new_item_period'):
            self.elements[self.new_item_name].period = self.new_item_period
            del self.new_item_period
        return super(PeriodicFinancialList, self)._new_item_init_callback()

class Income(PeriodicFinancialList):
    """A PeriodicFinancialList representing a person's income."""
    pass

class Asset(FinancialList):
    """A FinancialList representing a person's assets."""
    pass

class Expense(PeriodicFinancialList):
    """A PeriodicFinancialList representing a person's expenses."""
    pass

class Value(DAObject):
    """Represents a value in a FinancialList."""
    def amount(self):
        """Returns the value's amount, or 0 if the value does not exist."""
        if not self.exists:
            return 0
        return (Decimal(self.value))
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return text_type(self.amount())
    def __float__(self):
        return float(self.amount())
    def __int__(self):
        return int(self.__float__())
    def __long__(self):
        return long(self.__float__())
    def __le__(self, other):
        return self.value <= (other.value if isinstance(other, Value) else other)
    def __ge__(self, other):
        return self.value >= (other.value if isinstance(other, Value) else other)
    def __gt__(self, other):
        return self.value > (other.value if isinstance(other, Value) else other)
    def __lt__(self, other):
        return self.value < (other.value if isinstance(other, Value) else other)
    def __eq__(self, other):
        return self.value == (other.value if isinstance(other, Value) else other)
    def __ne__(self, other):
        return self.value != (other.value if isinstance(other, Value) else other)
    def __hash__(self):
        return hash((self.instanceName,))

class PeriodicValue(Value):
    """Represents a value in a PeriodicFinancialList."""
    def amount(self, period_to_use=1):
        """Returns the periodic value's amount for a full period,
        or 0 if the value does not exist."""
        if not self.exists:
            return 0
        ensure_definition(period_to_use)
        return (Decimal(self.value) * Decimal(self.period)) / Decimal(period_to_use)

class OfficeList(DAList):
    """Represents a list of offices of a company or organization."""
    def init(self, *pargs, **kwargs):
        self.object_type = Address
        return super(OfficeList, self).init(*pargs, **kwargs)

class Organization(Person):
    """Represents a company or organization."""
    def init(self, *pargs, **kwargs):
        if 'offices' in kwargs:
            self.initializeAttribute('office', OfficeList)
            if type(kwargs['offices']) is list:
                for office in kwargs['offices']:
                    if type(office) is dict:
                        new_office = self.office.appendObject(Address, **office)
                        new_office.geolocate()
            del kwargs['offices']
        return super(Organization, self).init(*pargs, **kwargs)
    def will_handle(self, problem=None, county=None):
        """Returns True or False depending on whether the organization
        serves the given county and/or handles the given problem."""
        ensure_definition(problem, county)
        if problem:
            if not (hasattr(self, 'handles') and problem in self.handles):
                return False
        if county:
            if not (hasattr(self, 'serves') and county in self.serves):
                return False
        return True
    def _map_info(self):
        the_response = list()
        if hasattr(self.office):
            for office in self.office:
                if (office.location.gathered and office.location.known) or office.geolocate():
                    if self.name.defined():
                        the_info = self.name.full()
                    else:
                        the_info = capitalize(self.object_name())
                    if hasattr(office.location, 'description') and office.location.description != '':
                        the_info += " [NEWLINE] " + office.location.description
                    this_response = {'latitude': office.location.latitude, 'longitude': office.location.longitude, 'info': the_info}
                    if hasattr(office, 'icon'):
                        this_response['icon'] = office.icon
                    elif hasattr(self, 'icon'):
                        this_response['icon'] = self.icon
                    the_response.append(this_response)
        if len(the_response):
            return the_response
        return None

# twilio_config = None

# def set_twilio_config(the_config):
#     global twilio_config
#     twilio_config = the_config

def get_sms_session(phone_number, config='default'):
    """Returns the SMS session information for a phone number, or None if no session exists."""
    result = server.get_sms_session(phone_number, config=config)
    for key in ['number', 'tempuser', 'user_id']:
        if key in result:
            del result[key]
    return result

def initiate_sms_session(phone_number, yaml_filename=None, email=None, new=False, send=True, config='default'):
    """Initiates a new SMS session for a phone number, overwriting any that is currently active."""
    server.initiate_sms_session(phone_number, yaml_filename=yaml_filename, email=email, new=new, config=config)
    if send:
        send_sms_invite(to=phone_number, config=config)
    return True

def terminate_sms_session(phone_number, config='default'):
    """Terminates an SMS session for a phone number, whether the session exists or not."""
    return server.terminate_sms_session(phone_number, config=config)

def send_sms_invite(to=None, body='question', config='default'):
    """Sends an SMS message to a phone number, where the message is the
    current interview question the recipient would see if he or she
    texted 'question' to the system.
    """
    if to is None:
        raise DAError("send_sms_invite: no phone number provided")
    phone_number = docassemble.base.functions.phone_number_in_e164(to)
    if phone_number is None:
        raise DAError("send_sms_invite: phone number is invalid")
    message = server.sms_body(phone_number, body=body, config=config)
    #logmessage("Sending message " + str(message) + " to " + str(phone_number))
    send_sms(to=phone_number, body=message, config=config)

def send_sms(to=None, body=None, template=None, task=None, attachments=None, config='default'):
    """Sends a text message and returns whether sending the text was successful."""
    if server.twilio_config is None:
        logmessage("send_sms: ignoring because Twilio not enabled")
        return False
    if config not in server.twilio_config['name']:
        logmessage("send_sms: ignoring because requested configuration does not exist")
        return False
    tconfig = server.twilio_config['name'][config]
    if 'sms' not in tconfig or tconfig['sms'] in [False, None]:
        logmessage("send_sms: ignoring because SMS not enabled")
        return False
    if attachments is None:
        attachments = []
    elif attachments is not list:
        attachments = [attachments]
    if type(to) is not list:
        to = [to]
    if len(to) == 0:
        logmessage("send_sms: no recipients identified")
        return False
    if template is not None and body is None:
        body_html = '<html><body>'
        if template.subject is not None:
            body_html += markdown_to_html(template.subject)
        body_html += markdown_to_html(template.content) + '</body></html>'
        body = BeautifulSoup(body_html, "html.parser").get_text('\n')
    if body is None:
        body = word("blank message")
    success = True
    media = list()
    for attachment in attachments:
        attachment_list = list()
        if isinstance(attachment, DAFileCollection):
            subattachment = getattr(attachment, 'pdf', None)
            if subattachment is None:
                subattachment = getattr(attachment, 'docx', None)
            if subattachment is None:
                subattachment = getattr(attachment, 'rtf', None)
            if subattachment is None:
                subattachment = getattr(attachment, 'tex', None)
            if subattachment is not None:
                attachment_list.append(subattachment)
            else:
                logmessage("send_sms: could not find file to attach in DAFileCollection.")
                success = False
        elif isinstance(attachment, DAFile):
            attachment_list.append(attachment)
        elif isinstance(attachment, DAStaticFile):
            attachment_list.append(attachment)
        elif isinstance(attachment, DAFileList):
            attachment_list.extend(attachment.elements)
        elif isinstance(attachment, string_types) and re.search(r'^https?://', attachment):
            attachment_list.append(attachment)
        else:
            logmessage("send_sms: attachment " + repr(attachment) + " is not valid.")
            success = False
        if success:
            for the_attachment in attachment_list:
                if type(the_attachment) is DAFile and the_attachment.ok:
                    #url = url_start + server.url_for('serve_stored_file', uid=this_thread.current_info['session'], number=the_attachment.number, filename=the_attachment.filename, extension=the_attachment.extension)
                    media.append(the_attachment.url_for(_external=True))
                if type(the_attachment) is DAStaticFile:
                    media.append(the_attachment.url_for(_external=True))
                elif isinstance(the_attachment, string_types):
                    media.append(the_attachment)
    if len(media) > 10:
        logmessage("send_sms: more than 10 attachments were provided; not sending message")
        success = False
    if success:
        twilio_client = TwilioRestClient(tconfig['account sid'], tconfig['auth token'])
        for recipient in to:
            phone_number = phone_string(recipient)
            if phone_number is not None:
                if phone_number.startswith('whatsapp:'):
                    from_number = 'whatsapp:' + tconfig.get('whatsapp number', tconfig['number'])
                else:
                    from_number = tconfig['number']
                try:
                    if len(media):
                        message = twilio_client.messages.create(to=phone_number, from_=from_number, body=body, media_url=media)
                    else:
                        message = twilio_client.messages.create(to=phone_number, from_=from_number, body=body)
                except Exception as errstr:
                    logmessage("send_sms: failed to send message from " + from_number + " to " + phone_number + ": " + text_type(errstr))
                    return False
    if success and task is not None:
        mark_task_as_performed(task)
    return True


class FaxStatus(object):
    def __init__(self, sid):
        self.sid = sid
    def status(self):
        if self.sid is None:
            return 'not-configured'
        the_json = server.server_redis.get('da:faxcallback:sid:' + self.sid)
        if the_json is None:
            return 'no-information'
        info = json.loads(the_json)
        return info['FaxStatus']
    def info(self):
        if self.sid is None:
            return dict(FaxStatus='not-configured')
        the_json = server.server_redis.get('da:faxcallback:sid:' + self.sid)
        if the_json is None:
            return dict(FaxStatus='no-information')
        info_dict = json.loads(the_json)
        return info_dict
    def received(self):
        the_status = self.status()
        if the_status in ('no-information', 'not-configured'):
            return None
        if the_status == 'received':
            return True
        else:
            return False

def send_fax(fax_number, file_object, config='default', country=None):
    if server.twilio_config is None:
        logmessage("send_fax: ignoring because Twilio not enabled")
        return FaxStatus(None)
    if config not in server.twilio_config['name']:
        logmessage("send_fax: ignoring because requested configuration does not exist")
        return FaxStatus(None)
    tconfig = server.twilio_config['name'][config]
    if 'fax' not in tconfig or tconfig['fax'] in [False, None]:
        logmessage("send_fax: ignoring because fax not enabled")
        return FaxStatus(None)
    return FaxStatus(server.send_fax(fax_string(fax_number, country=country), file_object, config))

def send_email(to=None, sender=None, cc=None, bcc=None, body=None, html=None, subject="", template=None, task=None, attachments=None):
    """Sends an e-mail and returns whether sending the e-mail was successful."""
    if attachments is None:
        attachments = []
    if not isinstance(attachments, (list, DAList, set, DASet, tuple)):
        attachments = [attachments]
    from flask_mail import Message
    if type(to) is not list:
        to = [to]
    if len(to) == 0:
        return False
    if template is not None:
        if subject is None or subject == '':
            subject = template.subject
        body_html = '<html><body>' + markdown_to_html(template.content) + '</body></html>'
        if body is None:
            body = BeautifulSoup(body_html, "html.parser").get_text('\n')
        if html is None:
            html = body_html
    if body is None and html is None:
        body = ""
    subject = re.sub(r'[\n\r]+', ' ', subject)
    sender_string = email_stringer(sender, first=True, include_name=True)
    to_string = email_stringer(to)
    cc_string = email_stringer(cc)
    bcc_string = email_stringer(bcc)
    #logmessage("Sending mail to: " + repr(dict(subject=subject, recipients=to_string, sender=sender_string, cc=cc_string, bcc=bcc_string, body=body, html=html)))
    msg = Message(subject, sender=sender_string, recipients=to_string, cc=cc_string, bcc=bcc_string, body=body, html=html)
    filenames_used = set()
    success = True
    for attachment in attachments:
        attachment_list = list()
        if isinstance(attachment, DAFileCollection):
            subattachment = getattr(attachment, 'pdf', None)
            if subattachment is None:
                subattachment = getattr(attachment, 'docx', None)
            if subattachment is None:
                subattachment = getattr(attachment, 'rtf', None)
            if subattachment is None:
                subattachment = getattr(attachment, 'tex', None)
            if subattachment is not None:
                attachment_list.append(subattachment)
            else:
                success = False
        elif isinstance(attachment, DAFile):
            attachment_list.append(attachment)
        elif isinstance(attachment, DAStaticFile):
            attachment_list.append(attachment)
        elif isinstance(attachment, DAFileList):
            attachment_list.extend(attachment.elements)
        elif isinstance(attachment, string_types):
            file_info = server.file_finder(attachment)
            if 'fullpath' in file_info:
                failed = True
                with open(file_info['fullpath'], 'rb') as fp:
                    msg.attach(attachment_name(file_info['filename'], filenames_used), file_info['mimetype'], fp.read())
                    failed = False
                if failed:
                    success = False
            else:
                success = False
            continue
        else:
            success = False
        if success:
            for the_attachment in attachment_list:
                if isinstance(the_attachment, DAStaticFile):
                    the_path = the_attachment.path()
                    with open(the_path, 'rb') as fp:
                        the_basename = os.path.basename(the_path)
                        extension, mimetype = server.get_ext_and_mimetype(the_basename)
                        msg.attach(attachment_name(the_basename, filenames_used), mimetype, fp.read())
                    continue
                if the_attachment.ok:
                    if the_attachment.has_specific_filename:
                        file_info = server.file_finder(str(the_attachment.number), filename=the_attachment.filename)
                    else:
                        file_info = server.file_finder(str(the_attachment.number))
                    if 'fullpath' in file_info:
                        failed = True
                        with open(file_info['fullpath'], 'rb') as fp:
                            msg.attach(attachment_name(the_attachment.filename, filenames_used), file_info['mimetype'], fp.read())
                            failed = False
                        if failed:
                            success = False
                    else:
                        success = False
    if success:
        try:
            logmessage("send_email: starting to send")
            server.send_mail(msg)
            logmessage("send_email: finished sending")
        except Exception as errmess:
            logmessage("send_email: sending mail failed with error of " + " type " + str(errmess.__class__.__name__) + ": " + text_type(errmess))
            success = False
    if success and task is not None:
        mark_task_as_performed(task)
    return(success)

def attachment_name(filename, filenames):
    if filename not in filenames:
        filenames.add(filename)
        return filename
    indexno = 1
    parts = os.path.splitext(filename)
    while True:
        new_filename = '%s_%03d%s' % (parts[0], indexno, parts[1])
        if new_filename not in filenames:
            filenames.add(new_filename)
            return new_filename
        indexno += 1

def map_of(*pargs, **kwargs):
    """Inserts into markup a Google Map representing the objects passed as arguments."""
    the_map = {'markers': list()}
    all_args = list()
    for arg in pargs:
        if isinstance(arg, list):
            all_args.extend(arg)
        else:
            all_args.append(arg)
    for arg in all_args:
        if isinstance(arg, DAObject):
            markers = arg._map_info()
            if markers:
                for marker in markers:
                    if 'icon' in marker and not isinstance(marker['icon'], dict):
                        marker['icon'] = {'url': server.url_finder(marker['icon'])}
                    if 'info' in marker and marker['info']:
                        marker['info'] = markdown_to_html(marker['info'], trim=True)
                    the_map['markers'].append(marker)
    if 'center' in kwargs:
        the_center = kwargs['center']
        if callable(getattr(the_center, '_map_info', None)):
            markers = the_center._map_info()
            if markers:
                the_map['center'] = markers[0]
    if 'center' not in the_map and len(the_map['markers']):
        the_map['center'] = the_map['markers'][0]
    if len(the_map['markers']) or 'center' in the_map:
        return '[MAP ' + re.sub(r'\n', '', codecs.encode(json.dumps(the_map).encode('utf-8'), 'base64').decode()) + ']'
    return word('(Unable to display map)')

def ocr_file_in_background(*pargs, **kwargs):
    """Starts optical character recognition on one or more image files or PDF
    files and returns an object representing the background task created."""
    language = kwargs.get('language', None)
    psm = kwargs.get('psm', 6)
    x = kwargs.get('x', None)
    y = kwargs.get('y', None)
    W = kwargs.get('W', None)
    H = kwargs.get('H', None)
    message = kwargs.get('message', None)
    image_file = pargs[0]
    if len(pargs) > 1:
        ui_notification = pargs[1]
    else:
        ui_notification = None
    args = dict(yaml_filename=this_thread.current_info['yaml_filename'], user=this_thread.current_info['user'], user_code=this_thread.current_info['session'], secret=this_thread.current_info['secret'], url=this_thread.current_info['url'], url_root=this_thread.current_info['url_root'], language=language, psm=psm, x=x, y=y, W=W, H=H, extra=ui_notification, message=message)
    collector = server.ocr_finalize.s(**args)
    todo = list()
    for item in docassemble.base.ocr.ocr_page_tasks(image_file, **args):
        todo.append(server.ocr_page.s(**item))
    the_chord = server.chord(todo)(collector)
    if ui_notification is not None:
        worker_key = 'da:worker:uid:' + str(this_thread.current_info['session']) + ':i:' + str(this_thread.current_info['yaml_filename']) + ':userid:' + str(this_thread.current_info['user']['the_user_id'])
        #sys.stderr.write("worker_caller: id is " + str(result.obj.id) + " and key is " + worker_key + "\n")
        server.server_redis.rpush(worker_key, the_chord.id)
    #sys.stderr.write("ocr_file_in_background finished\n")
    return the_chord

# def ocr_file_in_background(image_file, ui_notification=None, language=None, psm=6, x=None, y=None, W=None, H=None):
#     """Starts optical character recognition on one or more image files or PDF
#     files and returns an object representing the background task created."""
#     sys.stderr.write("ocr_file_in_background: started\n")
#     return server.async_ocr(image_file, ui_notification=ui_notification, language=language, psm=psm, x=x, y=y, W=W, H=H, user_code=this_thread.current_info.get('session', None))

def ocr_file(image_file, language=None, psm=6, f=None, l=None, x=None, y=None, W=None, H=None):
    """Runs optical character recognition on one or more image files or PDF
    files and returns the recognized text."""
    if not (isinstance(image_file, DAFile) or isinstance(image_file, DAFileList)):
        return word("(Not a DAFile or DAFileList object)")
    pdf_to_ppm = get_config("pdftoppm")
    if pdf_to_ppm is None:
        pdf_to_ppm = 'pdftoppm'
    ocr_resolution = get_config("ocr dpi")
    if ocr_resolution is None:
        ocr_resolution = '300'
    langs = docassemble.base.ocr.get_available_languages()
    if language is None:
        language = get_language()
    ocr_langs = get_config("ocr languages")
    if ocr_langs is None:
        ocr_langs = dict()
    if language in langs:
        lang = language
    else:
        if language in ocr_langs and ocr_langs[language] in langs:
            lang = ocr_langs[language]
        else:
            try:
                pc_lang = pycountry.languages.get(alpha_2=language)
                lang_three_letter = pc_lang.alpha_3
                if lang_three_letter in langs:
                    lang = lang_three_letter
                else:
                    if 'eng' in langs:
                        lang = 'eng'
                    else:
                        lang = langs[0]
                    logmessage("ocr_file: could not get OCR language for language " + str(language) + "; using language " + str(lang))
            except Exception as the_error:
                if 'eng' in langs:
                    lang = 'eng'
                else:
                    lang = langs[0]
                logmessage("ocr_file: could not get OCR language for language " + str(language) + "; using language " + str(lang) + "; error was " + str(the_error))
    if isinstance(image_file, DAFile):
        image_file = [image_file]
    temp_directory_list = list()
    file_list = list()
    for doc in image_file:
        if hasattr(doc, 'extension'):
            if doc.extension not in ['pdf', 'png', 'jpg', 'gif']:
                return word("(Not a readable image file)")
            path = doc.path()
            if doc.extension == 'pdf':
                directory = tempfile.mkdtemp()
                temp_directory_list.append(directory)
                prefix = os.path.join(directory, 'page')
                args = [pdf_to_ppm, '-r', str(ocr_resolution)]
                if f is not None:
                    args.extend(['-f', str(f)])
                if l is not None:
                    args.extend(['-l', str(l)])
                if x is not None:
                    args.extend(['-x', str(x)])
                if y is not None:
                    args.extend(['-y', str(y)])
                if W is not None:
                    args.extend(['-W', str(W)])
                if H is not None:
                    args.extend(['-H', str(H)])
                args.extend(['-png', path, prefix])
                result = subprocess.call(args)
                if result > 0:
                    return word("(Unable to extract images from PDF file)")
                file_list.extend(sorted([os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]))
                continue
            file_list.append(path)
    page_text = list()
    for page in file_list:
        image = Image.open(page)
        color = ImageEnhance.Color(image)
        bw = color.enhance(0.0)
        bright = ImageEnhance.Brightness(bw)
        brightened = bright.enhance(1.5)
        contrast = ImageEnhance.Contrast(brightened)
        final_image = contrast.enhance(2.0)
        file_to_read = tempfile.TemporaryFile()
        final_image.save(file_to_read, "PNG")
        file_to_read.seek(0)
        try:
            text = subprocess.check_output(['tesseract', 'stdin', 'stdout', '-l', str(lang), '--psm', str(psm)], stdin=file_to_read).decode('utf-8', 'ignore')
        except subprocess.CalledProcessError as err:
            raise Exception("ocr_file: failed to list available languages: " + str(err) + " " + str(err.output.decode()))
        page_text.append(text)
    for directory in temp_directory_list:
        shutil.rmtree(directory)
    return "\f".join(page_text)

def read_qr(image_file, f=None, l=None, x=None, y=None, W=None, H=None):
    """Reads QR codes from a file or files and returns a list of codes found."""
    if not (isinstance(image_file, DAFile) or isinstance(image_file, DAFileList)):
        return word("(Not a DAFile or DAFileList object)")
    if isinstance(image_file, DAFile):
        image_file = [image_file]
    pdf_to_ppm = get_config("pdftoppm")
    if pdf_to_ppm is None:
        pdf_to_ppm = 'pdftoppm'
    ocr_resolution = get_config("ocr dpi")
    if ocr_resolution is None:
        ocr_resolution = '300'
    file_list = list()
    temp_directory_list = list()
    for doc in image_file:
        if hasattr(doc, 'extension'):
            if doc.extension not in ['pdf', 'png', 'jpg', 'gif']:
                return word("(Not a readable image file)")
            path = doc.path()
            if doc.extension == 'pdf':
                directory = tempfile.mkdtemp()
                temp_directory_list.append(directory)
                prefix = os.path.join(directory, 'page')
                args = [pdf_to_ppm, '-r', str(ocr_resolution)]
                if f is not None:
                    args.extend(['-f', str(f)])
                if l is not None:
                    args.extend(['-l', str(l)])
                if x is not None:
                    args.extend(['-x', str(x)])
                if y is not None:
                    args.extend(['-y', str(y)])
                if W is not None:
                    args.extend(['-W', str(W)])
                if H is not None:
                    args.extend(['-H', str(H)])
                args.extend(['-png', path, prefix])
                result = subprocess.call(args)
                if result > 0:
                    return word("(Unable to extract images from PDF file)")
                file_list.extend(sorted([os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]))
                continue
            file_list.append(path)
    codes = list()
    for page in file_list:
        if PY2:
            raise Exception("QR reading is not supported in the Python 2.7 version of docassemble.")
        else:
            from pyzbar.pyzbar import decode
            for result in decode(Image.open(page)):
                codes.append(result.data.decode())
    return codes

def path_and_mimetype(file_ref):
    """Returns a path and the MIME type of a file"""
    if isinstance(file_ref, DAFileList) and len(file_ref.elements) > 0:
        file_ref = file_ref.elements[0]
    elif isinstance(file_ref, DAFileCollection):
        file_ref = file_ref._first_file()
    elif isinstance(file_ref, DAStaticFile):
        path = file_ref.path()
        extension, mimetype = server.get_ext_and_mimetype(file_ref.filename)
        return path, mimetype
    if isinstance(file_ref, DAFile):
        if hasattr(file_ref, 'mimetype'):
            mime_type = file_ref.mimetype
        else:
            mime_type = None
        return file_ref.path(), mime_type
    file_info = server.file_finder(file_ref)
    return file_info.get('fullpath', None), file_info.get('mimetype', None)

class DummyObject(object):
    def __init__(self, *pargs, **kwargs):
        pass

SimpleTextMachineLearner = DummyObject

def set_knn_machine_learner(target):
    global SimpleTextMachineLearner
    SimpleTextMachineLearner = target

SVMMachineLearner = DummyObject

def set_svm_machine_learner(target):
    global SVMMachineLearner
    SVMMachineLearner = target

RandomForestMachineLearner = DummyObject

def set_random_forest_machine_learner(target):
    global RandomForestMachineLearner
    RandomForestMachineLearner = target

MachineLearningEntry = DummyObject

def set_machine_learning_entry(target):
    global MachineLearningEntry
    MachineLearningEntry = target

class DAModel(DAObject):
    """Applies natural language processing to user input and returns a prediction."""
    def init(self, *pargs, **kwargs):
        if 'store' in kwargs:
            self.store = kwargs['store']
        else:
            self.store = '_global'
        if 'group_id' in kwargs:
            self.group_id = kwargs['group_id']
            parts = self.group_id.split(':')
            if len(parts) == 3 and parts[0].startswith('docassemble.') and re.match(r'data/sources/.*\.json', parts[1]):
                self.store = parts[0] + ':' + parts[1]
                self.group_id = parts[2]
            elif len(parts) == 2 and parts[0] == 'global':
                self.store = '_global'
                self.group_id = parts[1]
            elif len(parts) == 2 and (re.match(r'data/sources/.*\.json', parts[0]) or re.match(r'[^/]+\.json', parts[0])):
                self.store = re.sub(r':.*', ':data/sources/' + re.sub(r'^data/sources/', '', parts[0]), self.store)
                self.group_id = parts[1]
            elif len(parts) != 1:
                self.store = '_global'
        else:
            self.group_id = self.instanceName
        if self.store != '_global':
            self.group_id = self.store + ':' + self.group_id
        self.key = kwargs.get('key', None)
        self.use_for_training = kwargs.get('use_for_training', True)
        self.learner = SimpleTextMachineLearner(group_id=self.group_id)
        if 'text' in kwargs:
            self.text = kwargs['text']
            self.predict()
        return super(DAModel, self).init(*pargs, **kwargs)
    def __str__(self):
        return self.__unicode__().encode('utf-8') if PY2 else self.__unicode__()
    def __unicode__(self):
        return text_type(self.prediction)
    def predict(self):
        if self.use_for_training:
            self.entry_id = self.learner.save_for_classification(self.text, key=self.key)
        self.predictions = self.learner.predict(self.text, probabilities=True)
        if len(self.predictions):
            self.prediction = self.predictions[0][0]
            self.probability = self.predictions[0][1]
        else:
            self.prediction = None
            self.probability = 1.0

def pdf_concatenate(*pargs, **kwargs):
    """Concatenates PDF files together and returns a DAFile representing
    the new PDF.

    """
    paths = list()
    get_pdf_paths([x for x in pargs], paths)
    if len(paths) == 0:
        raise DAError("pdf_concatenate: no valid files to concatenate")
    pdf_path = docassemble.base.pandoc.concatenate_files(paths, pdfa=kwargs.get('pdfa', False), password=kwargs.get('password', None))
    pdf_file = DAFile()._set_instance_name_for_function()
    pdf_file.initialize(filename=kwargs.get('filename', 'file.pdf'))
    pdf_file.copy_into(pdf_path)
    pdf_file.retrieve()
    pdf_file.commit()
    return pdf_file

def get_pdf_paths(target, paths):
    if isinstance(target, DAFileCollection) and hasattr(target, 'pdf'):
        paths.append(target.pdf.path())
    elif isinstance(target, DAFileList) or isinstance(target, list):
        for the_file in target:
            get_pdf_paths(the_file, paths)
    elif isinstance(target, DAFile) or isinstance(target, DAStaticFile):
        paths.append(target.path())

def recurse_zip_params(param, root, files):
    if isinstance(param, dict):
        for key, val in param.items():
            recurse_zip_params(val, root + key + '/', files=files)
    elif isinstance(param, (list, tuple, DAFileList)):
        for val in param:
            recurse_zip_params(val, root, files=files)
    elif isinstance(param, DAFileCollection):
        the_file = getattr(param, 'pdf', None)
        if the_file is None:
            the_file = getattr(param, 'docx', None)
            if the_file is None:
                the_file = getattr(param, 'rtf', None)
            if the_file is None:
                the_file = getattr(param, 'tex', None)
        if the_file is not None:
            recurse_zip_params(the_file, root, files=files)
    elif isinstance(param, DAStaticFile) or isinstance(param, DAFile):
        files.append((root + param.filename, param.path()))
    else:
        file_info = server.file_finder(param)
        files.append((root + file_info['filename'], file_info['fullpath']))
    return files

def zip_file(*pargs, **kwargs):
    """Returns a ZIP file as a DAFile containing the files provided as arguments."""
    files = list()
    timezone = get_default_timezone()
    recurse_zip_params(pargs, '', files)
    zip_file = DAFile()._set_instance_name_for_function()
    zip_file.initialize(filename=kwargs.get('filename', 'file.zip'))
    zf = zipfile.ZipFile(zip_file.path(), mode='w')
    for zip_path, path in files:
        info = zipfile.ZipInfo(zip_path)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        info.date_time = datetime.datetime.utcfromtimestamp(os.path.getmtime(path)).replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone)).timetuple()
        with open(path, 'rb') as fp:
            zf.writestr(info, fp.read())
    zf.close()
    zip_file.retrieve()
    zip_file.commit()
    return zip_file

def validation_error(message):
    """Raises a validation error with a given message"""
    raise DAValidationError(message)

def invalid_variable_name(varname):
    if not isinstance(varname, string_types):
        return True
    if re.search(r'[\n\r\(\)\{\}\*\^\#]', varname):
        return True
    varname = re.sub(r'[\.\[].*', '', varname)
    if not valid_variable_match.match(varname):
        return True
    return False

contains_volatile = re.compile('^(x\.|x\[|.*\[[ijklmn]\])')

def url_ask(data):
    """Like url_action, but accepts a data structure containing a sequence of variables to be sought."""
    if not isinstance(data, list):
        data = [data]
    variables = []
    for the_saveas in data:
        if isinstance(the_saveas, dict) and len(the_saveas) == 1 and ('undefine' in the_saveas or 'recompute' in the_saveas or 'set' in the_saveas or 'follow up' in the_saveas):
            if 'set' in the_saveas:
                if not isinstance(the_saveas['set'], list):
                    raise DAError("url_ask: the set statement must refer to a list.  " + repr(data))
                clean_list = []
                for the_dict in the_saveas['set']:
                    if not isinstance(the_dict, dict):
                        raise DAError("url_ask: a set command must refer to a list of dicts.  " + repr(data))
                    for the_var, the_val in the_dict.items():
                        if not isinstance(the_var, string_types):
                            raise DAError("url_ask: a set command must refer to a list of dicts with keys as variable names.  " + repr(data))
                        the_var_stripped = the_var.strip()
                    if invalid_variable_name(the_var_stripped):
                        raise DAError("url_ask: missing or invalid variable name " + repr(the_var) + " .  " + repr(data))
                    if contains_volatile.search(the_var_stripped):
                        raise DAError("url_ask cannot be used with a generic object or a variable iterator")
                    clean_list.append([the_var_stripped, the_val])
                variables.append(dict(action='_da_set', arguments=dict(variables=clean_list)))
            if 'follow up' in the_saveas:
                if not isinstance(the_saveas['follow up'], list):
                    raise DAError("url_ask: the follow up statement must refer to a list.  " + repr(data))
                for var in the_saveas['follow up']:
                    if not isinstance(var, string_types):
                        raise DAError("url_ask: invalid variable name in follow up " + command + ".  " + repr(data))
                    var_saveas = var.strip()
                    if invalid_variable_name(var_saveas):
                        raise DAError("url_ask: missing or invalid variable name " + repr(var_saveas) + " .  " + repr(data))
                    if contains_volatile.search(var):
                        raise DAError("url_ask cannot be used with a generic object or a variable iterator")
                    variables.append(dict(action=var, arguments=dict()))
            for command in ('undefine', 'recompute'):
                if command not in the_saveas:
                    continue
                if not isinstance(the_saveas[command], list):
                    raise DAError("url_ask: the " + command + " statement must refer to a list.  " + repr(data))
                clean_list = []
                for undef_var in the_saveas[command]:
                    if not isinstance(undef_var, string_types):
                        raise DAError("url_ask: invalid variable name " + repr(undef_var) + " in " + command + ".  " + repr(data))
                    undef_saveas = undef_var.strip()
                    if invalid_variable_name(undef_saveas):
                        raise DAError("url_ask: missing or invalid variable name " + repr(undef_saveas) + " .  " + repr(data))
                    if contains_volatile.search(undef_saveas):
                        raise DAError("url_ask cannot be used with a generic object or a variable iterator")
                    clean_list.append(undef_saveas)
                variables.append(dict(action='_da_undefine', arguments=dict(variables=clean_list)))
                if command == 'recompute':
                    variables.append(dict(action='_da_compute', arguments=dict(variables=clean_list)))
            continue
        if isinstance(the_saveas, dict) and len(the_saveas) == 2 and 'action' in the_saveas and 'arguments' in the_saveas:
            if not isinstance(the_saveas['arguments'], dict):
                raise DAError("url_ask: an arguments directive must refer to a dictionary.  " + repr(data))
            if contains_volatile.search(the_saveas['action']):
                raise DAError("url_ask cannot be used with a generic object or a variable iterator")
            variables.append(dict(action=the_saveas['action'], arguments=the_saveas['arguments']))
        if not isinstance(the_saveas, string_types):
            raise DAError("url_ask: invalid variable name " + repr(the_saveas) + ".  " + repr(data))
        the_saveas = the_saveas.strip()
        if invalid_variable_name(the_saveas):
            raise DAError("url_ask: missing or invalid variable name " + repr(the_saveas) + " .  " + repr(data))
        if the_saveas not in variables:
            variables.append(the_saveas)
        if contains_volatile.search(the_saveas):
            raise DAError("url_ask cannot be used with a generic object or a variable iterator")
    return url_action('_da_force_ask', variables=variables)

def action_button_html(url, icon=None, color='success', size='sm', block=False, label='Edit', classname=None, new_window=True, id_tag=None):
    """Returns HTML for a button that visits a particular URL."""
    if not isinstance(label, string_types):
        label = 'Edit'
    if color not in ('primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark', 'link'):
        color = 'dark'
    if size not in ('sm', 'md', 'lg'):
        size = 'sm'
    if size == 'md':
        size = ''
    else:
        size = " btn-" + size
    if block:
        block = ' btn-block'
    else:
        block = ''
    if classname is None:
        classname = ''
    else:
        classname = ' ' + text_type(classname)
    if isinstance(icon, string_types):
        icon = re.sub(r'^(fa[a-z])-fa-', r'\1 fa-', icon)
        if not re.search(r'^fa[a-z] fa-', icon):
            icon = 'fas fa-' + icon
        icon = '<i class="' + icon + '"></i> '
    else:
        icon = ''
    if new_window is True:
        target = ''
    elif new_window is False:
        target = 'target="_self" '
    else:
        target = 'target="' + text_type(new_window) + '" '
    if id_tag is None:
        id_tag = ''
    else:
        id_tag = ' id=' + json.dumps(id_tag)
    return '<a ' + target + 'href="' + url + '"' + id_tag + ' class="btn' + size + block + ' btn-' + color + ' btn-darevisit' + classname + '">' + icon + word(label) + '</a> '

def overlay_pdf(main_pdf, logo_pdf, first_page=None, last_page=None, logo_page=None, only=None):
    """Overlays a page from a PDF file on top of the pages of another PDF file."""
    if isinstance(main_pdf, DAFileCollection):
        main_file = main_pdf.pdf.path()
    elif isinstance(main_pdf, DAFile) or isinstance(main_pdf, DAFileList):
        main_file = main_pdf.path()
    elif isinstance(main_pdf, string_types):
        main_file = main_pdf
    else:
        raise Exception("overlay_pdf: bad main filename")
    if isinstance(logo_pdf, DAFileCollection):
        logo_file = logo_pdf.pdf.path()
    elif isinstance(logo_pdf, DAFile) or isinstance(logo_pdf, DAFileList):
        logo_file = logo_pdf.path()
    elif isinstance(logo_pdf, string_types):
        logo_file = logo_pdf
    else:
        raise Exception("overlay_pdf: bad logo filename")
    outfile = DAFile()
    outfile.set_random_instance_name()
    outfile.initialize(extension='pdf')
    docassemble.base.pdftk.overlay_pdf(main_file, logo_file, outfile.path(), first_page=first_page, last_page=last_page, logo_page=logo_page, only=only)
    outfile.commit()
    outfile.retrieve()
    return outfile

def explain(explanation, category='default'):
    """Add a line to the explanations history."""
    if 'explanations' not in this_thread.internal:
        this_thread.internal['explanations'] = dict()
    if category not in this_thread.internal['explanations']:
        this_thread.internal['explanations'][category] = list()
    if explanation not in this_thread.internal['explanations'][category]:
        this_thread.internal['explanations'][category].append(explanation)

def clear_explanations(category='default'):
    """Erases the history of explanations."""
    if 'explanations' not in this_thread.internal:
        return
    if category == 'all':
        this_thread.internal['explanations'] = dict()
    if category not in this_thread.internal['explanations']:
        return
    this_thread.internal['explanations'][category] = list()

def explanation(category='default'):
    """Returns the list of explanations."""
    if 'explanations' not in this_thread.internal:
        return []
    return this_thread.internal['explanations'].get(category, [])

def set_status(**kwargs):
    """Sets various settings in the interview session."""
    if 'misc' not in this_thread.internal:
        this_thread.internal['misc'] = dict()
    for key, val in kwargs.items():
        this_thread.internal['misc'][key] = val

def get_status(setting):
    """Retrieves a setting of the interview session."""
    if 'misc' not in this_thread.internal:
        return None
    return this_thread.internal['misc'].get(setting, None)

from docassemble.base.oauth import DAOAuth

