import warnings

import entrypoints

from mlflow.exceptions import MlflowException
from mlflow.utils import get_uri_scheme


class TrackingStoreRegistry:
    """Scheme-based registry for tracking store implementations

    This class allows the registration of a function or class to provide an
    implementation for a given scheme of `store_uri` through the `register`
    methods. Implementations declared though the entrypoints
    `mlflow.tracking_store` group can be automatically registered through the
    `register_entrypoints` method.

    When instantiating a store through the `get_store` method, the scheme of
    the store URI provided (or inferred from environment) will be used to
    select which implementation to instantiate, which will be called with same
    arguments passed to the `get_store` method.
    """

    def __init__(self):
        self._registry = {}

    def register(self, scheme, store_builder):
        self._registry[scheme] = store_builder

    def register_entrypoints(self):
        """Register tracking stores provided by other packages"""
        for entrypoint in entrypoints.get_group_all("mlflow.tracking_store"):
            try:
                self.register(entrypoint.name, entrypoint.load())
            except (AttributeError, ImportError) as exc:
                warnings.warn(
                    'Failure attempting to register tracking store for scheme "{}": {}'.format(
                        entrypoint.name, str(exc)
                    ),
                    stacklevel=2
                )

    def get_store(self, store_uri=None, artifact_uri=None):
        """Get a store from the registry based on the scheme of store_uri

        :param store_uri: The store URI. If None, it will be inferred from the environment. This URI
                          is used to select which tracking store implementation to instantiate and
                          is passed to the constructor of the implementation.
        :param artifact_uri: Artifact repository URI. Passed through to the tracking store
                             implementation.

        :return: An instance of `mlflow.store.AbstractStore` that fulfills the store URI
                 requirements.
        """
        from mlflow.tracking import utils
        store_uri = store_uri if store_uri is not None else utils.get_tracking_uri()
        scheme = store_uri if store_uri == "databricks" else get_uri_scheme(store_uri)

        try:
            store_builder = self._registry[scheme]
        except KeyError:
            raise MlflowException(
                "Unexpected URI scheme '{}' for tracking store. "
                "Valid schemes are: {}".format(store_uri, list(self._registry.keys())))
        return store_builder(store_uri=store_uri, artifact_uri=artifact_uri)
