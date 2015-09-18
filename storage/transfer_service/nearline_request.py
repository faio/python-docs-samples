# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# [START all]
import argparse
import datetime
import json
import logging

from apiclient import discovery
from oauth2client.client import GoogleCredentials


logging.basicConfig(level=logging.DEBUG)


# [START main]
def main(description, project_id, day, month, year, hours, minutes,
         source_bucket, sink_bucket):
    """Create a transfer from the Google Cloud Storage Standard class to the
    Nearline Storage class."""
    credentials = GoogleCredentials.get_application_default()
    storagetransfer = discovery.build(
        'storagetransfer', 'v1', credentials=credentials)

    # Edit this template with desired parameters.
    # Specify times below using US Pacific Time Zone.
    transfer_job = {
        'description': description,
        'status': 'ENABLED',
        'projectId': project_id,
        'schedule': {
            'scheduleStartDate': {
                'day': day,
                'month': month,
                'year': year
            },
            'startTimeOfDay': {
                'hours': hours,
                'minutes': minutes
            }
        },
        'transferSpec': {
            'gcsDataSource': {
                'bucketName': source_bucket
            },
            'gcsDataSink': {
                'bucketName': sink_bucket
            },
            'objectConditions': {
                'minTimeElapsedSinceLastModification': '2592000s'
            },
            'transferOptions': {
                'deleteObjectsFromSourceAfterTransfer': 'true'
            }
        }
    }

    result = storagetransfer.transferJobs().create(body=transfer_job).execute()
    logging.info('Returned transferJob: %s', json.dumps(result, indent=4))
# [END main]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a transfer from the Google Cloud Storage Standard '
        'class to the Nearline Storage class.')
    parser.add_argument('description', help='Transfer description.')
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('date', help='Date YYYY/MM/DD.')
    parser.add_argument('time', help='Time (24hr) HH:MM.')
    parser.add_argument('source_bucket', help='Source bucket name.')
    parser.add_argument('sink_bucket', help='Sink bucket name.')

    args = parser.parse_args()
    date = datetime.datetime.strptime(args.date, '%Y/%m/%d')
    time = datetime.datetime.strptime(args.time, '%H:%M')

    main(
        args.description,
        args.project_id,
        date.year,
        date.month,
        date.day,
        time.hour,
        time.minute,
        args.source_bucket,
        args.sink_bucket)

# [END all]
