Introducing plight
==================

|Pypi| |Licence|


**plight** allows screen backlight adjustment.


Install
-------

To install plight:

.. code:: console

    pip install plight

or clone the repo and:

.. code:: console

    python setup.py install


You must allow users in the video group to change the brightness, a udev rule such as the following can be used:

/etc/udev/rules.d/backlight.rules

.. code:: console

    ACTION=="add", SUBSYSTEM=="backlight", KERNEL=="acpi_video0", RUN+="/bin/chgrp video /sys/class/backlight/%k/brightness"
    ACTION=="add", SUBSYSTEM=="backlight", KERNEL=="acpi_video0", RUN+="/bin/chmod g+w /sys/class/backlight/%k/brightness"

where acpi_video0 must be replaced by the right directory. Then add user to
video group:

gpasswd -a user video



.. |Pypi| image:: https://badge.fury.io/py/plight.svg
    :target: https://pypi.org/project/plight
    :alt: Pypi Package

.. |Licence| image:: https://img.shields.io/github/license/ipselium/plight.svg
