import os
import platform
import shutil
import sys

import click
import yaml
from dots.logging import Logger, log
from dots.utils import run_output


class SystemChecker(object):
    """A super-fancy helper for checking the system configuration
    """

    def __init__(self):
        super().__init__()
        self._logger = Logger()

    def _log_happy(self, msg):
        self._logger.spaced_status("pass", msg, fit_width=4)

    def _log_angry(self, msg, is_warning):
        if is_warning:
            self._logger.spaced_status("warn", msg, fit_width=4)
        else:
            self._logger.spaced_status("fail", msg, fit_width=4)

    def platform(self):
        return platform.system()

    def equal(self, expected, *, should_warn=False, **kwargs):
        """Check if a given value for something is equal to the expected value.

        checker.equal(value, name=from_system)
        """
        assert len(kwargs) == 1, "expected 1 keyword argument"

        name, value = next(iter(kwargs.items()))
        if value == expected:
            self._log_happy(name + " is correct")
        else:
            self._log_angry(
                "{} is not {!r}, it is {!r}".format(name, expected, value),
                is_warning=should_warn,
            )

    # The actual logic is below
    def run(self, fname):
        data = self._load_yaml(fname)

        self._check_username(data["identity"]["username"])
        self._check_ssh(data["identity"]["ssh-key"])
        self._check_gpg(data["identity"]["gpg-key"])

        for category, contents in data["things"].items():
            self._check_category(category, contents, data)

    def _load_yaml(self, fname):
        with open(fname) as f:
            try:
                return yaml.load(f)
            except Exception as e:
                click.secho("ERROR: Could not parse file.", fg="red")
                click.secho(str(e), fg="red")
                sys.exit(1)

    def _check_username(self, expected):
        self.equal(expected, Username=os.environ["USER"])

    def _check_ssh(self, expected):
        # FIXME: Is this fragile?
        output = run_output(
            "ssh-keygen -E md5 -lf {}".format(os.path.expanduser("~/.ssh/id_rsa.pub"))
        )
        if output is None:
            ssh_key = "not found"
        else:
            ssh_key = output.split()[1]
            if ssh_key.startswith("MD5:"):
                ssh_key = ssh_key[4:]

        self.equal(expected, **{"SSH key": ssh_key})

    def _check_gpg(self, expected):
        # This checks that the GPG key exists in the dB
        output = run_output("gpg --list-keys {}".format(expected))
        if output is not None:
            self.equal(expected, **{"GPG key": expected})
        else:
            self.equal(expected, **{"GPG key": "not found"})

    def _check_category(self, category, contents, data):
        if "if" in contents:
            if list(contents["if"]) != ["platform"]:
                raise ValueError(
                    "Needed condition of category {} to be 'platform'".format(category)
                )
            if contents["if"]["platform"] != self.platform():
                log.spaced_status("skip", category)
                return

        log.spaced_status("topic", category, fit_width=5)
        with log:
            self._check_executables(category, contents.get("executables", None))
            self._check_run_items(category, contents.get("run_check", None), data)

    def _check_executables(self, category, executables):
        if not executables:
            return

        def noun_for(x):
            return "executable" if len(x) == 1 else "executables"

        # Convert the string to a list.
        executables = list(map(lambda x: x.strip(), executables.split(",")))

        missing = set()
        for fname in executables:
            if shutil.which(fname) is None:
                missing.add(fname)

        if missing:
            desc = "missing {}: {}".format(
                noun_for(missing), ", ".join(map(repr, missing))
            )

            log.spaced_status("fail", desc, fit_width=4)
        else:
            log.spaced_status(
                "pass",
                "{} {} available".format(len(executables), noun_for(executables)),
                fit_width=4,
            )

    def _check_run_items(self, category, run_items, data):
        if not run_items:
            return

        for name, cmd_dict in run_items.items():
            if not isinstance(cmd_dict, dict) or "cmd" not in cmd_dict:
                log.spaced_status(
                    "warn", "!!! invalid !!! {}".format(category, name), fit_width=4
                )
                continue

            if "equal" in cmd_dict:
                # Matching output.
                expected = cmd_dict["equal"]
                # Perform substitution
                if expected.startswith("$"):
                    item = data
                    for part in expected[1:].split("."):
                        item = item[part]
                    expected = item

                got = run_output(cmd_dict["cmd"])
                if isinstance(got, str) and expected == got.strip():
                    log.spaced_status("pass", name, fit_width=4)
                else:
                    log.spaced_status("fail", name, fit_width=4)
            else:
                log.spaced_status("warn", name + " -- did not check.", fit_width=4)
