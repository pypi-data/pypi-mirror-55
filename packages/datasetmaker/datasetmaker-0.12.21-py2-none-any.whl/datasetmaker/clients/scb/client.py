import logging
from pathlib import Path
from typing import Any, Union

import pandas as pd

from datasetmaker.datapackage import DataPackage
from datasetmaker.merge import merge_packages
from datasetmaker.models import Client

from .election_results import get_election_results
from .psu_polls import get_psu_data

log = logging.getLogger(__name__)


class SCBClient(Client):
    """
    Client for the Swedish statistical agency Statistiska Centralbyrån.

    Fetches data from a number of selected tables.
    """

    def get(self, **kwargs: Any) -> pd.DataFrame:
        """Get the data."""
        psu_data = get_psu_data()
        election_results = get_election_results()

        self.data = [psu_data, election_results]
        return self.data

    def save(self, path: Union[Path, str], **kwargs: Any) -> None:
        """Save the data."""
        log.info('Creating DataPackage')

        kwargs.update({
            'author': 'Datastory',
            'name': 'scb',
            'source': 'Statistiska Centralbyrån',
            'status': 'draft',
            'title': 'Statistiska Centralbyrån',
            'topics': ['politics', 'sweden'],
        })

        packages: list = []

        for data in self.data:
            package = DataPackage(data)
            packages.append(package)

        merge_packages(packages, path, **kwargs)

        log.info('Datapackage successfully created')
