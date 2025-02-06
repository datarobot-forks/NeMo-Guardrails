# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
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

from unittest.mock import patch

import pytest
from _hashlib import UnsupportedDigestmodError

from nemoguardrails.hashing import detect_default_hash_algorithm as setup_hashing
from nemoguardrails.hashing import (
    generate_hash,
    get_default_hash_algorithm,
    set_default_hash_algorithm,
)


@pytest.fixture(scope="function")
def md5_is_missing():
    """Raise an exception when hashlib.md5 is not available."""
    with patch("hashlib.md5", side_effect=AttributeError):
        setup_hashing()
        yield

    # cleanup
    setup_hashing()


@pytest.fixture(scope="function")
def md5_unsupported_digest():
    """Raise an exception when hashlib is using OpenSSL compiled in FIPS mode."""
    with patch("hashlib.md5", side_effect=UnsupportedDigestmodError):
        setup_hashing()
        yield

    # cleanup
    setup_hashing()


@pytest.fixture(params=["md5_is_missing", "md5_unsupported_digest"])
def md5_not_available(request):
    yield request.getfixturevalue(request.param)


def test_default_without_md5(md5_not_available):
    assert get_default_hash_algorithm() == "sha256"


def test_default_with_md5():
    assert get_default_hash_algorithm() == "md5"


def test_hash_without_md5(md5_not_available):
    hash_value = generate_hash("test")
    assert isinstance(hash_value, str)
    assert len(hash_value) == 64  # SHA256 hash is 64 characters long


def test_hash_with_md5():
    hash_value = generate_hash("test")
    assert isinstance(hash_value, str)
    assert len(hash_value) == 32  # MD5 hash is 32 characters long


def test_invalid_hash_algorithm_not_allowed():
    with pytest.raises(ValueError):
        set_default_hash_algorithm("invalid")
