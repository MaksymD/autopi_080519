
packages-installed:
  pkg.installed:
    - pkgs:
      - python-pip
      - python-smbus
      - python-pygame
      - raspi-gpio
      - lighttpd
      - git
      - avrdude
      - espeak

pip-requirements-distributed:
  file.managed:
    - name: /etc/pip-requirements.txt
    - source: salt://requirements.txt

pip-requirements-installed:
  pip.installed:
    - requirements: /etc/pip-requirements.txt
    - upgrade: true  # Needed in order to get newest changes from git repos
    - require:
      - file: /etc/pip-requirements.txt
    - unless: diff /etc/pip-requirements.txt /etc/pip-requirements-installed.txt

pip-requirements-installation-completed:
  file.managed:
    - name: /etc/pip-requirements-installed.txt
    - source: /etc/pip-requirements.txt
    - watch:
      - pip: pip-requirements-installed

minion-restart-after-pip-requirements-installed:
  module.wait:
    - name: minionutil.request_restart
    - reason: pip_requirements_installed
    - watch:
      - pip: pip-requirements-installed
