# db-host-prep

Automation to build a database host.

Note: The Ansible Helper can be found here: [ansible-helper](https://github.com/mminichino/ansible-helper)

````
$ ansible-helper.py playbooks/prep-db-host.yaml -h host01,host02,host03 --region us-east-1 --dnssecret "dm9pZHZvaWR2b2lkCg==" --domain domain.local --bucket my-software
````
