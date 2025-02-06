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
import hashlib

_default_hash_algorithm: str


def set_default_hash_algorithm(algorithm: str):
    """
    Set the default hash algorithm.

    Parameters
    ----------
    algorithm : str
        The name of the hash algorithm to set as default.
        The available options are: "md5", "sha256".

    Raises
    ------
    ValueError
        If the provided algorithm is not supported.
    """
    _supported = {"md5", "sha256"}

    if algorithm not in _supported:
        raise ValueError(
            f"Unsupported value: {algorithm}, " f"use one of {','.join(_supported)}"
        )

    global _default_hash_algorithm
    _default_hash_algorithm = algorithm


def get_default_hash_algorithm() -> str:
    """Returns the default hash algorithm based on the system configuration."""
    return _default_hash_algorithm


def generate_hash(text: str) -> str:
    """
    Get the hash of a given text using the default hash function.

    Args:
        text (str): The text to hash.

    Returns:
        str: The hash of the text.
    """
    hash_func = getattr(hashlib, _default_hash_algorithm)
    return hash_func(text.encode()).hexdigest()


def _is_md5_available() -> bool:
    """
    Check if MD5 usage is allowed. In some FIPS-compliant Python builds, the MD5 hashing
    function may be missing or raise an exception when using OpenSSL compiled in FIPS mode.

    When MD5 is not available, AttributeError will be raised for missing hashlib.md5.
    When OpenSSL is compiled in FIPS mode, the _hashlib.UnsupportedDigestmodError(ValueError)
    will be raised.

    Returns
    -------
    bool
        True if MD5 is available, False otherwise.
    """
    try:
        hashlib.md5()
        return True
    except (AttributeError, ValueError):
        return False


def detect_default_hash_algorithm():
    set_default_hash_algorithm("md5" if _is_md5_available() else "sha256")


detect_default_hash_algorithm()
