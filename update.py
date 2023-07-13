# -*- coding: utf-8 -*-
# Upside Travel, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import boto3
import os
import shutil

import clamav
from common import AV_DEFINITION_PATH
from common import AV_DEFINITION_S3_BUCKET
from common import AV_DEFINITION_S3_PREFIX
from common import CLAMAVLIB_PATH
from common import S3_ENDPOINT
from common import get_timestamp

def lambda_handler(event, context):
    s3 = boto3.resource("s3", endpoint_url=S3_ENDPOINT)
    s3_client = boto3.client("s3", endpoint_url=S3_ENDPOINT)

    print("Script starting at %s\n" % (get_timestamp()))
    # if os.path.exists(AV_DEFINITION_PATH):
    #     shutil.rmtree(AV_DEFINITION_PATH)

    clamav.update_defs_from_freshclam(AV_DEFINITION_PATH, CLAMAVLIB_PATH)
    # If main.cvd gets updated (very rare), we will need to force freshclam
    # to download the compressed version to keep file sizes down.
    # The existence of main.cud is the trigger to know this has happened.
    if os.path.exists(os.path.join(AV_DEFINITION_PATH, "main.cud")):
        os.remove(os.path.join(AV_DEFINITION_PATH, "main.cud"))
        if os.path.exists(os.path.join(AV_DEFINITION_PATH, "main.cvd")):
            os.remove(os.path.join(AV_DEFINITION_PATH, "main.cvd"))
        clamav.update_defs_from_freshclam(AV_DEFINITION_PATH, CLAMAVLIB_PATH)
    clamav.upload_defs_to_s3(
        s3_client, AV_DEFINITION_S3_BUCKET, AV_DEFINITION_S3_PREFIX, AV_DEFINITION_PATH
    )
    print("Script finished at %s\n" % get_timestamp())
