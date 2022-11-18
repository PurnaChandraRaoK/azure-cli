# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import os
import time
import pathlib
import getopt
import uuid
import sys
from knack.log import get_logger

from datetime import datetime
from time import sleep
from dateutil.tz import tzutc  # pylint: disable=import-error
from azure.cli.testsdk.scenario_tests import AllowLargeResponse
from msrestazure.azure_exceptions import CloudError
from azure.cli.core.util import CLIError
from azure.cli.core.util import parse_proxy_resource_id
from azure.cli.testsdk.base import execute
from azure.cli.testsdk.exceptions import CliTestError  # pylint: disable=unused-import
from azure.cli.testsdk import (
    JMESPathCheck,
    NoneCheck,
    ResourceGroupPreparer,
    ScenarioTest,
    StringContainCheck,
    live_only)
from azure.cli.testsdk.preparers import (
    AbstractPreparer,
    SingleValueReplacer)

logger = get_logger(__name__)


class MigrationScenarioTest(ScenarioTest):

    @AllowLargeResponse()
    def test_postgres_flexible_server_migration(self):
        self._test_server_migration('postgres')

    def _test_server_migration(self, database_engine):
        # Set this to True or False depending on whether we are in live mode or test mode
        # livemode = True
        livemode = False

        if livemode:
            # Live mode values
            target_subscription_id = "bb5358e5-fa78-4717-87e1-e57f1b4da5d1"
            migration_name = str(uuid.uuid4())
        else:
            # Mock test mode values
            target_subscription_id = "00000000-0000-0000-0000-000000000000"
            migration_name = "00000000-0000-0000-0000-000000000000"

        target_resource_group_name = "Sterling2MeruRG"
        target_server_name = "target-server-longhaul"
        curr_dir = os.path.dirname(os.path.realpath(__file__))