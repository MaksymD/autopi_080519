
{% set _timestamp = None|strftime("%Y%m%d%H%M%S") %}

minion-restart-requested-after-patching:
  module.wait:
    - name: minionutil.request_restart
    - reason: minion_patched

minion-script-001-backed-up:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/minion.py.{{ _timestamp }}
    - source: /usr/lib/python2.7/dist-packages/salt/minion.py
    - force: true
    - prereq:
      - file: minion-script-001-patched
minion-script-001-patched:
  file.patch:
    - name: /usr/lib/python2.7/dist-packages/salt/minion.py
    - source: salt://minion/patch/minion.py.patch001
    - hash: 36d5e76a283786e8040f2576e3ebd52910326d31
    # Only apply this patch if hash matches specific version
    - onlyif: cd /usr/lib/python2.7/dist-packages/salt/ && echo '31fa372f166f5d1e27394022780709de6e03e337 minion.py' | sha1sum -c -
    - watch_in:
      - module: minion-restart-requested-after-patching
minion-script-001-rolled-back:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/minion.py
    - source: /usr/lib/python2.7/dist-packages/salt/minion.py.{{ _timestamp }}
    - force: true
    - onfail:
      - file: minion-script-001-patched
minion-script-002-backed-up:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/minion.py.{{ _timestamp }}
    - source: /usr/lib/python2.7/dist-packages/salt/minion.py
    - force: true
    - prereq:
      - file: minion-script-002-patched
minion-script-002-patched:
  file.patch:
    - name: /usr/lib/python2.7/dist-packages/salt/minion.py
    - source: salt://minion/patch/minion.py.patch002
    - hash: 422b3a0877b468ad09327b50322274cc71b829f4
    # IMPORTANT: No 'onlyif' requisite for latest patch
    - watch_in:
      - module: minion-restart-requested-after-patching
minion-script-002-rolled-back:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/minion.py
    - source: /usr/lib/python2.7/dist-packages/salt/minion.py.{{ _timestamp }}
    - force: true
    - onfail:
      - file: minion-script-002-patched

fileclient-script-001-backed-up:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/fileclient.py.{{ _timestamp }}
    - source: /usr/lib/python2.7/dist-packages/salt/fileclient.py
    - force: true
    - prereq:
      - file: fileclient-script-001-patched
fileclient-script-001-patched:
  file.patch:
    - name: /usr/lib/python2.7/dist-packages/salt/fileclient.py
    - source: salt://minion/patch/fileclient.py.patch001
    - hash: 2ed2f597d4f69ec85bc65e8a7002ca507c3cfc9a
    # Only apply this patch if hash matches specific version
    - onlyif: cd /usr/lib/python2.7/dist-packages/salt/ && echo '08413a2972ac91821ed06f0b0a9bd92c314cbf80 fileclient.py' | sha1sum -c -
    - watch_in:
      - module: minion-restart-requested-after-patching
fileclient-script-001-rolled-back:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/fileclient.py
    - source: /usr/lib/python2.7/dist-packages/salt/fileclient.py.{{ _timestamp }}
    - force: true
    - onfail:
      - file: fileclient-script-001-patched
fileclient-script-002-backed-up:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/fileclient.py.{{ _timestamp }}
    - source: /usr/lib/python2.7/dist-packages/salt/fileclient.py
    - force: true
    - prereq:
      - file: fileclient-script-002-patched
fileclient-script-002-patched:
  file.patch:
    - name: /usr/lib/python2.7/dist-packages/salt/fileclient.py
    - source: salt://minion/patch/fileclient.py.patch002
    - hash: a8b8890707ff803e9e068b0d1d3ce51c4c44c844
    # IMPORTANT: No 'onlyif' requisite for latest patch
    - watch_in:
      - module: minion-restart-requested-after-patching
fileclient-script-002-rolled-back:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/fileclient.py
    - source: /usr/lib/python2.7/dist-packages/salt/fileclient.py.{{ _timestamp }}
    - force: true
    - onfail:
      - file: fileclient-script-002-patched

utils-schedule-script-backed-up:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/utils/schedule.py.{{ _timestamp }}
    - source: /usr/lib/python2.7/dist-packages/salt/utils/schedule.py
    - force: true
    - prereq:
      - file: utils-schedule-script-patched
utils-schedule-script-patched:
  file.patch:
    - name: /usr/lib/python2.7/dist-packages/salt/utils/schedule.py
    - source: salt://minion/patch/utils/schedule.py.patch
    - hash: e0b2c0262264ce39b50cca882cc95524fc08b4ff
    - watch_in:
      - module: minion-restart-requested-after-patching
utils-schedule-script-rolled-back:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/utils/schedule.py
    - source: /usr/lib/python2.7/dist-packages/salt/utils/schedule.py.{{ _timestamp }}
    - force: true
    - onfail:
      - file: utils-schedule-script-patched

log-setup-script-backed-up:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/log/setup.py.{{ _timestamp }}
    - source: /usr/lib/python2.7/dist-packages/salt/log/setup.py
    - force: true
    - prereq:
      - file: log-setup-script-patched
log-setup-script-patched:
  file.patch:
    - name: /usr/lib/python2.7/dist-packages/salt/log/setup.py
    - source: salt://minion/patch/log/setup.py.patch
    - hash: 3dfe270678c4bff4247fdb35e41f887c7938d332
    - watch_in:
      - module: minion-restart-requested-after-patching
log-setup-script-rolled-back:
  file.copy:
    - name: /usr/lib/python2.7/dist-packages/salt/log/setup.py
    - source: /usr/lib/python2.7/dist-packages/salt/log/setup.py.{{ _timestamp }}
    - force: true
    - onfail:
      - file: log-setup-script-patched
