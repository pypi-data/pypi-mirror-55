EGCG-Core
===========
[![PyPI](https://img.shields.io/pypi/v/EGCG-Core.svg)](https://pypi.python.org/pypi/EGCG-Core)
[![PyPI](https://img.shields.io/pypi/pyversions/EGCG-Core.svg)](https://pypi.python.org/pypi/EGCG-Core)
[![travis](https://img.shields.io/travis/EdinburghGenomics/EGCG-Core/master.svg)](https://travis-ci.org/EdinburghGenomics/EGCG-Core)
[![landscape](https://landscape.io/github/EdinburghGenomics/EGCG-Core/master/landscape.svg)](https://landscape.io/github/EdinburghGenomics/EGCG-Core)
[![GitHub issues](https://img.shields.io/github/issues/EdinburghGenomics/EGCG-Core.svg)](https://github.com/EdinburghGenomics/EGCG-Core/issues)  
[![Coverage Status](https://coveralls.io/repos/github/EdinburghGenomics/EGCG-Core/badge.svg)](https://coveralls.io/github/EdinburghGenomics/EGCG-Core)

This is a core module for Edinburgh Genomics' clinical processing. It contains common modules for use across
EGCG's various projects, including logging, configuration, exceptions and random utility functions. There are
also modules for interfacing with EGCG\'s reporting app and Clarity LIMS instance.

Modules
----------

### executor
This module allows the execution of Bash commands from Python. Executor classes include
a non-threaded Executor, a threaded StreamExecutor that streams its stdout/stderr as it runs, and an
ArrayExecutor that combines multiple Executors into a job array. There is also ClusterExecutor, which writes
and submits a Bash script for a resource manager. All Executor classes implement a `start` method and a `join`
method, which returns an integer exit status.

- execute - Takes some string commands, decides whether or not to use cluster execution depending on the
  config, and calls either `local_execute` or `cluster_execute`.
- local_execute - Takes one or more string commands and calls Executor or StreamExecutor, depending on
  arguments. If multiple commands are given, Executor/StreamExecutors will be called via ArrayExecutor.
- cluster_execute - Takes one or more string commands and calls the appropriate ClusterExecutor depending on
  the config.
- Executor - Executes a Bash command via `subprocess.Popen`.
- StreamExecutor - Executes via `Popen` and `threading.Thread`, allowing it to output the job's stdout in real
  time. Can use `self.run` or `self.start` followed by `self.join`.
- ArrayExecutor - Takes a list of Bash commands and generates an Executor object for each. In `self.run`, it
  iterates over these and calls `start` and `join` for each one.
- ClusterExecutor - Takes one or more Bash commands. Upon creation, it calls creates a script writer and
  writes a Bash script. `prelim_cmds` may be specified to, e.g, export Java paths prior to commencing the
  job array. `self.start` and `self.join` executes a qsub/sbatch/etc. Bash command on the script.

#### script_writers
This `executor` submodule containing classes that can write scripts executable by the shell or by a resource manager.
Each ScriptWriter writes a header giving arguments to the resource manager, including `walltime`, `cpus`,
`mem`, job name, stdout file and queue id, and also allows the writing of job arrays specific to the manager.

- ScriptWriter - Base class that can open a file for writing, write commands to it and save.
- PBSWriter
- SlurmWriter


### util
Contains convenience functions:
- find_files - Convenience function combining `glob.glob` and `os.path.join`. If any files are found for the
  given pattern, returns them.
- find_file - Returns the first result from find_files.
- str_join - Convenience function for calling str.join using `*args`.
- query_dict - Drills down into a nested dict with a dot-notated query string


### app_logging
Contains AppLogger, which can be subclassed to implement logging methods within a class, and
LoggingConfiguration, which contains all relevant loggers, handlers and formatters and provides `get_logger`,
which generates a logger registered with all active handlers.

- LoggingConfiguration - Contains handlers, loggers, and methods for adding/configuring them.
  - get_logger - Adds a logger with a given name and adds all active handlers to it.
  - add_handler - Adds a created handler and adds it to all active loggers.
  - set_log_level - Sets the log level for all active loggers and handlers.
  - set_formatter - Sets the format for all active handlers.
  - configure_handlers_from_config - Adds handlers using a dict config (example below). Uses
    `BaseConfigurator.convert` to allow the use of, e.g, `ext://sys.stdout`. Passes all args from the dict to
    the relevant object's constructor. Currently allows `StreamHandler`, `FileHandler` and
    `TimedRotatingFileHandler`.

```
log_cfg.configure_handlers_from_config(
    {
        'stream_handlers': [
            {'stream': 'ext://sys.stdout', 'level': 'DEBUG'},
            {'stream': 'ext://sys.stderr', 'level': 'ERROR'}
        ],
        'file_handlers': [{'filename': 'test.log'}],
        'timed_rotating_file_handlers': [{'filename': 'test2.log', 'when': 'midnight'}]
    }
)
```

- AppLogger - Mixin class containing a logger object created through LoggingConfiguration by @property, and
  named using `self.__class__.__name__`.


### config
Contains config classes able to scan possible file locations for Yaml config files, then uses `yaml` to read
it into a Python dict contained in `self.content`.

#### Configuration
Config class. Implements `__getitem__` for dict-style square bracket querying; `__contains__` to allow
the use of, e.g, `if x in cfg`; `get` as in `dict.get`; and `query` for drilling down into the dict, returning
`None` if nothing is found.

Is constructed with a list of possible files, and uses the first one it finds. Can also read config files containing
multiple environments. For example:

```
this: 1
that: 2
other: 3

testing:
    this: 1337

production:
    this: 1338
    that: 4
```
Upon loading a config file, the class can read an environment variable telling it which environment to use. It will then
merge the environment into `self.content`. For example, a Configuration set to 'testing' will have
`{'this': 1337, 'that': 2, 'other': 3}`, and one set to 'production' will have `{'this': 1338, 'that': 4, 'other': 3}`.

#### EnvConfiguration
Backward compatibility only.


### constants
Contains constants used in other EGCG projects, including dataset statuses and database keys/column names.


### exceptions
Custom exceptions raised by the pipeline: EGCGError, ConfigError, RestCommunicationError, LimsCommunicationError and
ArchivingError.


### rest_communication
Contains functions for interacting with the external Rest API. Uses the `requests` module.

- get_documents
- get_document
- post_entry
- put_entry
- patch_entry
- patch_entries - Iterates through payloads and patches each one. Only runs get_documents once.
- post_or_patch - Tries to post an entry and if unsuccessful, prepares the payload and patches instead.

#### uploading files
Post, put and patch requests are also able to upload files to the Rest API where the data type in the schema
is 'media'. To pass files to `requests`, specify the file to upload as a tuple consisting of the string 'file'
plus the file path. However, files cannot be uploaded inside complex nested JSON, so in this case, two
separate pushes would be necessary - one for the JSON and one for the files.

```python
import rest_communication

# files with simple json --> can do this in one action
data = [
    {'element_id': 'e1', 'key1': 'value1', 'report_r1': ('file', 'path/to/file/to/upload1.html')},
    {'element_id': 'e2', 'key1': 'value2', 'report_r1': ('file', 'path/to/file/to/upload2.html')}
]
rest_communication.post_or_patch('endpoint', data, 'element_id')


# files with nested json --> cannot do this in one action
data = [
    {'element_id': 'e1', 'key1': {'k': 'v1'}, 'report_r1': ('file', 'path/to/file/to/upload1.html')},
    {'element_id': 'e2', 'key1': {'k': 'v2'}, 'report_r1': ('file', 'path/to/file/to/upload2.html')}
]
rest_communication.post_or_patch('endpoint', data, 'element_id')
# raises RestCommunicationError('Cannot upload files and nested json in one query')


# files with nested json --> need to split into two actions
data = [
    {'element_id': 'e1', 'key1': {'k': 'v1'}},
    {'element_id': 'e2', 'key1': {'k': 'v2'}}
]
files = [
    {'element_id': 'e1', 'report_r1': ('file', 'path/to/file/to/upload1.html')},
    {'element_id': 'e2', 'report_r1': ('file', 'path/to/file/to/upload2.html')}
]
rest_communication.post_or_patch('endpoint', data, 'element_id')
rest_communication.post_or_patch('endpoint', files, 'element_id')
```


### integration_testing
This is a library and runner script for quality-oriented testing.


#### IntegrationTest
Wraps most of `unittest.TestCase`'s assert methods (with the exception of methods that use the context manager, such as
AssertRaises). Each wrapped assert method takes a string arg describing the assertion, and passes all other args to the
corresponding `TestCase` method, logging the result of the test to `checks.log` in the working dir. For example:

```python
class TestThing(IntegrationTest):
    def test_thing(self):
        x = 1
        y = 1
        z = False
        self.assertEqual('x equals y', x, y)
        self.assertTrue('z is True', z)
```

This will call the relevant `TestCase` methods and write some output to `checks.log`:

```
test_method             check_name  assert_method   result  args
TestThing.test_thing    x equals y  assertEqual     success (1, 1)
TestThing.test_thing    z is True   assertTrue      failed  (False,)
```

IntegrationTest also defines the attribute `patches`, which in subclasses can be a tuple or list of
`unittest.mock.patch` calls. These patches will have `__enter__` called on them on test setup, and `__exit__` on test
teardown.

#### ReportingAppIntegrationTest
Subclass of `IntegrationTest` which can run a Docker image of
[EGCG's reporting app](https://github.com/EdinburghGenomics/Reporting-App). On test setup, it starts an image from a
specified Reporting-App branch with an empty database, stores the image's IP address to
`rest_communication.default`, and waits for the image to become responsive. On teardown, it stops and removes the image.

#### integration_test_runner
The test runner is available in `bin` if running from source, or as an executable if installed. It does the following:

- Sets up a uniquely-named test run dir and `cd`s into it
- Takes a copy of the repo to test into the run dir (either from a local dir or remote Git repo) and `cd`s into it
- Checks out a Git branch on the tested repo (optional)
- Takes a copy of a config file for the repo and sets a config environment (optional)
- Runs pytest in directory `integration_tests` by default, with args for coverage, collect-only, multiprocessing, etc.
- Captures the output from pytest and `checks.log`, and logs it to a file, stdout and/or email as specified
- Cleans up the test run dir

The runner can use [pytest-xdist](https://pypi.org/project/pytest-xdist) to run tests in parallel, however this assumes
that both the tested code and the tests themselves are thread-safe.

Installing the test runner can be done via pip or with `python setup.py install`. If installing via setup.py on macOS,
Python may have trouble communicating with PyPI and run into SSL errors. This can be fixed by pip-installing the
certificate library `certifi`.
