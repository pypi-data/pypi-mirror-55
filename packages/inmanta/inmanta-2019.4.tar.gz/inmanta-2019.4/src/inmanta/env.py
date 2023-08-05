"""
    Copyright 2017 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

import hashlib
import json
import logging
import os
import re
import site
import subprocess
import sys
import tempfile
import venv
from subprocess import CalledProcessError
from typing import Any, Dict, List, Optional, Set, Tuple

import pkg_resources

LOGGER = logging.getLogger(__name__)


class VirtualEnv(object):
    """
        Creates and uses a virtual environment for this process
    """

    _egg_fragment_re = re.compile(r"#egg=(?P<name>[^&]*)")
    _at_fragment_re = re.compile(r"^(?P<name>[^@]+)@(?P<req>.+)")

    def __init__(self, env_path: str) -> None:
        LOGGER.info("Creating new virtual environment in %s", env_path)
        self.env_path: str = env_path
        self.virtual_python: Optional[str] = None
        self.__cache_done: Set[str] = set()
        self._parent_python: Optional[str] = None
        self._packages_installed_in_parent_env: Optional[Dict[str, str]] = None

    def get_package_installed_in_parent_env(self) -> Optional[Dict[str, str]]:
        if self._packages_installed_in_parent_env is None:
            self._packages_installed_in_parent_env = self._get_installed_packages(self._parent_python)

        return self._packages_installed_in_parent_env

    def init_env(self) -> bool:
        """
            Init the virtual environment
        """
        self._parent_python = sys.executable

        python_name = os.path.basename(sys.executable)

        # check if the virtual env exists
        if sys.platform == "win32":
            python_bin = os.path.join(self.env_path, "Scripts", python_name)
        else:
            python_bin = os.path.join(self.env_path, "bin", python_name)

        if not os.path.exists(python_bin):
            # venv requires some care when the .env folder already exists
            # https://docs.python.org/3/library/venv.html
            if not os.path.exists(self.env_path):
                path = self.env_path
            else:
                # venv has problems with symlinks
                path = os.path.realpath(self.env_path)

            # --clear is required in python prior to 3.4 if the folder already exists
            try:
                venv.create(path, clear=True, with_pip=True)
            except CalledProcessError as e:
                LOGGER.exception("Unable to create new virtualenv at %s (%s)", self.env_path, e.stdout.decode())
                return False
            except Exception:
                LOGGER.exception("Unable to create new virtualenv at %s", self.env_path)
                return False
            LOGGER.debug("Created a new virtualenv at %s", self.env_path)

        # set the path to the python and the pip executables
        self.virtual_python = python_bin
        return True

    def use_virtual_env(self) -> None:
        """
            Use the virtual environment
        """
        if not self.init_env():
            raise Exception("Unable to init virtual environment")

        self.activate_that()

        # patch up pkg
        pkg_resources.working_set = pkg_resources.WorkingSet._build_master()

    def activate_that(self) -> None:
        # adapted from https://github.com/pypa/virtualenv/blob/master/virtualenv_embedded/activate_this.py
        # MIT license
        # Copyright (c) 2007 Ian Bicking and Contributors
        # Copyright (c) 2009 Ian Bicking, The Open Planning Project
        # Copyright (c) 2011-2016 The virtualenv developers

        if sys.platform == "win32":
            binpath = os.path.abspath(os.path.join(self.env_path, "Scripts"))
            base = os.path.dirname(binpath)
            site_packages = os.path.join(base, "Lib", "site-packages")
        else:
            binpath = os.path.abspath(os.path.join(self.env_path, "bin"))
            base = os.path.dirname(binpath)
            site_packages = os.path.join(base, "lib", "python%s" % sys.version[:3], "site-packages")

        old_os_path = os.environ.get("PATH", "")
        os.environ["PATH"] = binpath + os.pathsep + old_os_path
        prev_sys_path = list(sys.path)

        site.addsitedir(site_packages)
        sys.real_prefix = sys.prefix
        sys.prefix = base
        # Move the added items to the front of the path:
        new_sys_path = []
        for item in list(sys.path):
            if item not in prev_sys_path:
                new_sys_path.append(item)
                sys.path.remove(item)
        sys.path[:0] = new_sys_path

    def _parse_line(self, req_line: str) -> Tuple[Optional[str], str]:
        """
            Parse the requirement line
        """
        at = VirtualEnv._at_fragment_re.search(req_line)
        if at is not None:
            d = at.groupdict()
            return d["name"], d["req"] + "#egg=" + d["name"]

        egg = VirtualEnv._egg_fragment_re.search(req_line)
        if egg is not None:
            d = egg.groupdict()
            return d["name"], req_line

        return None, req_line

    def _gen_requirements_file(self, requirements_list: List[str]) -> str:
        modules: Dict[str, Any] = {}
        for req in requirements_list:
            parsed_name, req_spec = self._parse_line(req)

            if parsed_name is None:
                name = req
            else:
                name = parsed_name

            url = None
            version = None
            try:
                # this will fail is an url is supplied
                parsed_req = list(pkg_resources.parse_requirements(req_spec))
                if len(parsed_req) > 0:
                    item = parsed_req[0]
                    if hasattr(item, "name"):
                        name = item.name
                    elif hasattr(item, "unsafe_name"):
                        name = item.unsafe_name
                    version = item.specs
                    if hasattr(item, "url"):
                        url = item.url
            except pkg_resources.RequirementParseError:
                url = req_spec

            if name not in modules:
                modules[name] = {"name": name, "version": []}

            if version is not None:
                modules[name]["version"].extend(version)

            if url is not None:
                modules[name]["url"] = url

        requirements_file = ""
        for module, info in modules.items():
            version_spec = ""
            if len(info["version"]) > 0:
                version_spec = " " + (", ".join(["%s %s" % (a, b) for a, b in info["version"]]))

            if "url" in info:
                module = info["url"]

            requirements_file += module + version_spec + "\n"

        return requirements_file

    def _install(self, requirements_list: List[str]) -> None:
        """
            Install requirements in the given requirements file
        """
        requirements_file = self._gen_requirements_file(requirements_list)

        try:
            fdnum, path = tempfile.mkstemp()
            fd = os.fdopen(fdnum, "w+")
            fd.write(requirements_file)
            fd.close()

            assert self.virtual_python is not None
            cmd: List["str"] = [self.virtual_python, "-m", "pip", "install", "-r", path]
            try:
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            except CalledProcessError as e:
                LOGGER.error("%s: %s", cmd, e.output.decode())
                LOGGER.error("requirements: %s", requirements_file)
                raise
            except Exception:
                LOGGER.error("%s: %s", cmd, output.decode())
                LOGGER.error("requirements: %s", requirements_file)
                raise
            else:
                LOGGER.debug("%s: %s", cmd, output.decode())

        finally:
            if os.path.exists(path):
                os.remove(path)

        pkg_resources.working_set = pkg_resources.WorkingSet._build_master()

    def _read_current_requirements_hash(self) -> str:
        """
            Return the hash of the requirements file used to install the current environment
        """
        path = os.path.join(self.env_path, "requirements.sha1sum")
        if not os.path.exists(path):
            return ""

        with open(path, "r") as fd:
            return fd.read().strip()

    def _set_current_requirements_hash(self, new_hash):
        """
            Set the current requirements hahs
        """
        path = os.path.join(self.env_path, "requirements.sha1sum")
        with open(path, "w+") as fd:
            fd.write(new_hash)

    def install_from_list(self, requirements_list: List[str], detailed_cache: bool = False, cache: bool = True) -> None:
        """
            Install requirements from a list of requirement strings
        """
        requirements_list = sorted(requirements_list)

        if detailed_cache:
            requirements_list = sorted(list(set(requirements_list) - self.__cache_done))
            if len(requirements_list) == 0:
                return

        requirements_list = self._remove_requirements_present_in_parent_env(requirements_list)

        # hash it
        sha1sum = hashlib.sha1()
        sha1sum.update("\n".join(requirements_list).encode())
        new_req_hash = sha1sum.hexdigest()

        current_hash = self._read_current_requirements_hash()

        if new_req_hash == current_hash and cache:
            return

        self._install(requirements_list)
        self._set_current_requirements_hash(new_req_hash)
        for x in requirements_list:
            self.__cache_done.add(x)

    def _remove_requirements_present_in_parent_env(self, requirements_list: List[str]) -> List[str]:
        reqs_to_remove = []
        packages_installed_in_parent = self.get_package_installed_in_parent_env()
        for r in requirements_list:
            parsed_req = list(pkg_resources.parse_requirements(r))[0]
            # Package is installed and its version fits the constraint
            if (
                parsed_req.project_name in packages_installed_in_parent
                and packages_installed_in_parent[parsed_req.project_name] in parsed_req
            ):
                reqs_to_remove.append(r)
        return [r for r in requirements_list if r not in reqs_to_remove]

    @classmethod
    def _get_installed_packages(cls, python_interpreter: str) -> Dict[str, str]:
        cmd = [python_interpreter, "-m", "pip", "list", "--format", "json"]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        except CalledProcessError as e:
            LOGGER.error("%s: %s", cmd, e.output.decode())
            raise
        except Exception:
            LOGGER.error("%s: %s", cmd, output.decode())
            raise
        else:
            LOGGER.debug("%s: %s", cmd, output.decode())

        return {r["name"]: r["version"] for r in json.loads(output.decode())}
