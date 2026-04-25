import os
from pathlib import Path

import pytest

_SDS_ROOT = Path(__file__).parent / "sds-data-manager"


@pytest.fixture(scope="session", autouse=True)
def _patch_cdk_asset_paths():
    # CDK constructs in sds-data-manager/sds_data_manager/constructs/ reference
    # lambda assets with relative paths like "sds_data_manager/lambda_code/..."
    # that are anchored to the sds-data-manager project root.  Rather than
    # fighting jsii's Node.js process CWD, resolve those paths to absolute in
    # Python before they reach jsii.
    try:
        import aws_cdk.aws_lambda as lam
    except ImportError:
        yield
        return

    real_from_asset = lam.Code.from_asset

    def patched_from_asset(path, *args, **kwargs):
        if not os.path.isabs(path):
            path = str(_SDS_ROOT / path)
        return real_from_asset(path, *args, **kwargs)

    lam.Code.from_asset = patched_from_asset
    try:
        yield
    finally:
        lam.Code.from_asset = real_from_asset
