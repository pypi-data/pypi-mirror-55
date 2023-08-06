# onlykey-agent

SSH agent for the OnlyKey.

SSH is a popular remote access tool that is often used by administrators. Thanks to the OnlyKey SSH Agent remote access can be passwordless and more secure.

## SSH Agent Quickstart Guide

1) After installing [prerequisites](#install), install OnlyKey agent on your client machine:
```
$ sudo pip install onlykey
$ sudo pip install onlykey-agent
```

2) Generate public key using onlykey-agent
```
$ onlykey-agent user@example.com
```

3) Log in to your server as usual and copy the row containing the output from the previous step into ~/.ssh/authorized_keys file on your server

i.e.

`ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBFwsFGFI7px8toa38FVeBIKcYdBvWzYXAiVcbB2d1o3zEsRB6Lm/ZuCzQjaLwQdcpT1aF8tycqt4K6AGI1o+qFk= user@example.com`

4) From now on you can log in to your server using OnlyKey using the following command:
```
$ onlykey-agent -c user@example.com
```

5) This method can also be used for git push or other mechanisms that are using SSH as their communication protocol:
```
$ onlykey-agent user@example.com git push
```

## Installation {#install}

### Linux UDEV Rule

In order for non-root users in Linux to be able to communicate with OnlyKey a udev rule must be created as described [here](https://docs.crp.to/linux.html).

### MacOS Install with dependencies
Python2 and pip are required. To setup a Python environment on MacOS we recommend Anaconda https://www.anaconda.com/download/#macos

```
$ pip install onlykey onlykey-agent
```

### Ubuntu Install with dependencies
```
$ apt update && apt upgrade
$ apt install python-pip python-dev libusb-1.0-0-dev libudev-dev
$ pip install onlykey onlykey-agent
```

### Debian Install with dependencies
```
$ apt update && apt upgrade
$ apt install python-pip python-dev libusb-1.0-0-dev libudev-dev
$ pip install onlykey onlykey-agent
```

### Fedora/RedHat/CentOS Install with dependencies
```
$ yum update
$ yum install python-pip python-devel libusb-devel libudev-devel \
              gcc redhat-rpm-config
$ pip install onlykey onlykey-agent
```
### OpenSUSE Install with dependencies
```
$ zypper install python-pip python-devel libusb-1_0-devel libudev-devel
$ pip install onlykey onlykey-agent
```

### Arch Linux Install with dependencies

```
$ sudo pacman -Sy git python2-setuptools python2 libusb python2-pip
$ pip install onlykey
```

### Linux UDEV Rule

In order for non-root users in Linux to be able to communicate with OnlyKey a udev rule must be created as described [here](https://docs.crp.to/linux).

## Advanced Options

### Supported curves

Keys are generated unique for each user / host combination. By default OnlyKey agent uses NIST P256 but also supports ED25519 keys. ED25519 can be used as follows:

1) Generate ED25519 public key using onlykey-agent
```
$ onlykey-agent user@example.com -e ed25519
```

2) Log in using ED25519 public key
```
$ onlykey-agent -c user@example.com -e ed25519
```

You can also just type `-e e` instead of typing out the full `-e ed25519`

The project started from a fork [trezor-agent](https://github.com/romanz/trezor-agent) (thanks!).
