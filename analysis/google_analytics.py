import json
import os

from django.conf import settings
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

from analysis.constants import ALL_METRICS

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/client_secrets.json'

credentials = GoogleCredentials.get_application_default()

analytics_service = build('analytics', 'v3')


def get_ga_report(start_date, end_date):
    # Get a list of all views (profiles) for the first property.
    if not settings.GA_PROFILE_ID:
        profiles = analytics_service.management().profiles().list(
            accountId=settings.GA_ACCOUNT_ID,
            webPropertyId=settings.GA_PROPERTY_ID).execute()

        profile_id = profiles.get('items')[0].get('id')
        settings.GA_PROFILE_ID = profile_id

    result = analytics_service.data().ga().get(
        ids='ga:' + settings.GA_PROFILE_ID,
        start_date=start_date,
        end_date=end_date,
        metrics=ALL_METRICS).execute()

    return result.get('totalsForAllResults')
