=============
awscli-cwlogs
=============

This awscli plugin provides the ``pull``, ``push`` and ``filter`` commands to access AWS CloudWatch Logs service.


The awscli-cwlogs package works on Python versions:

* 2.6.5 and greater
* 2.7.x and greater
* 3.3.x and greater


------------
Installation
------------

The easiest way to install awscli-cwlogs is to use `pip`_::

    $ pip install awscli-cwlogs

or, if you are not installing in a ``virtualenv``::

    $ sudo pip install awscli-cwlogs

If you have the awscli-cwlogs installed and want to upgrade to the latest version
you can run::

    $ pip install --upgrade awscli-cwlogs

This will install the awscli-cwlogs package as well as all dependencies, including awscli.

.. attention::
    If you have awscli installed, installing awscli-cwlogs might upgrade or downgrade your awscli depending on whether the awscli version you have is older or newer than what the awscli-cwlogs depends on. After installing awscli-cwlogs, you can run ``pip install --upgrade awscli`` to upgrade your awscli though potentially the latest awscli might not work well with the plugin. If you want to isolate awscli-cwlogs plugin from your existing awscli, you may consider ``virtaulenv``. Be careful that awscli by default stores its configuration to ~/.aws/config (or in %UserProfile%\.aws\config on Windows), to also isolate the configuration, you can define a separate config file ``export AWS_CONFIG_FILE=/path/to/config_file``.


---------------
Getting Started
---------------

Before using awscli-cwlogs plugin, you need to `configure awscli <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>`__ first.

Once that's done, to enable awscli-cwlogs, you can run::

    $ aws configure set plugins.cwlogs cwlogs

The above command adds below section to your aws config file::

    [plugins]
    cwlogs = cwlogs

To verify if awscli-cwlogs plugin is installed and configured properly, you can run::

    $ aws logs help

You will see the ``pull``, ``push`` and ``fitler`` commands from available commands, otherwise it means the cwlogs plugin is not registered properly.

If you see ``ImportError: No module named cwlogs`` error, it means the cwlogs plugin is registered in config file, but the plugin is not installed.

^^^^^^^^
Examples
^^^^^^^^
.............
 Push command
.............
You can use ``aws logs push help`` to check supported options.
The ``push`` command is used by CloudWatch Logs agent, check the `CloudWatch Logs Agent Reference <https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/AgentReference.html>`__ to see all supported options or if you want to keep the ``push`` command running.

1) Uploading a single log event to CloudWatch Logs service. The log group and log stream get created automatically if they don't exist.

::

    echo "Hello World" | aws logs push --log-group-name MyLogGroup --log-stream-name MyLogStream

2) The following ``push`` command pushes log events from a syslog file to log stream which is specified by ``/var/log/syslog`` and ``myhost1`` and exits after pushing all log events. This command doesn't push the incremental log events. To achieve that, use ``tail -f file | aws logs push ...``.

::

    cat /var/log/kernel.log | aws logs push --log-group-name /var/log/syslog --log-stream-name myhost1 --datetime-format '%b %d %H:%M:%S' --time-zone LOCAL --encoding ascii

3) The following ``push`` command pushes log events from multiple files based on configuration file. The ``initial_position`` determines where to start if the state of  ``file`` is not available.

::

    aws logs push --config-file push.cfg

::

    [general]
    state_file = push-state
    [logstream-messages]
    datetime_format = %b %d %H:%M:%S
    time_zone = LOCAL
    file = /var/log/messages
    file_fingerprint_lines = 1
    log_group_name = /var/log/messages
    log_stream_name = {hostname}
    initial_position = start_of_file
    encoding = utf_8
    buffer_duration = 5000
    [logstream-system.log]
    datetime_format = %b %d %H:%M:%S
    time_zone = UTC
    file = /var/log/system.log
    file_fingerprint_lines = 1-3
    log_group_name = /var/log/system.log
    log_stream_name = {hostname}
    initial_position = end_of_file
    encoding = ascii
    buffer_duration = 10000


.............
 Pull command
.............
You can use ``aws logs pull help`` to check supported options.

1) The following ``pull`` command pulls log events starting at ``2014-01-23T00:00:00Z`` from one log stream which is specified by ``website1/access_log`` and ``webhost-001`` and exits after pulling all log events.

::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z

2) When invoked with the ``--end-time`` option, the following ``pull`` command pulls all log events between ``2014-01-23T00:00:00Z`` (inclusive) and ``2014-01-23T01:00:00Z`` (not inclusive).

::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z --end-time 2014-01-23T01:00:00Z

3) When invoked with the ``--follow`` option, the following ``pull`` command does not exit after pulling all log events, but polls continuously for new log events.

::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z --follow

4) When invoked with the ``--output-format`` option, the following ``pull`` command only outputs the message field. By default, the output format is ``"{timestamp} {message}"``. Ingestion time can be included with ``"{timestamp} {ingestionTime} {message}"``.


::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z --output-format "{message}"

...............
 Filter command
...............
See `this AWS developer guide <http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/SearchDataFilterPattern.html>`__.

.. _pip: ht`tp://www.pip-installer.org/en/latest/
