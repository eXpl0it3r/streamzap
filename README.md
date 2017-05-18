# Streamzap

streamzap is a video stream detection tool using the OWASP Zed Attack Proxy (ZAP).

The goal is to detect and track video streams of common (Swiss) video portals on a given device by redirecting its
traffic to the ZAP and letting streamzap analyze the data.


## Setup

The recommended setup for streamzap involves two or more systems:

* Proxy & application system that runs ZAP and streamzap
* Client systems that consumes video streams and has its proxy setup to point to the proxy system


## Prerequisites

* [Python 2.7](https://www.python.org/downloads/) needs to be installed on the application system
    * Ensure you add the Python script directory to PATH!
* [OWASP ZAP](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project) needs to be installed on the proxy system


## Installation

1. Download & extract the zip archive
2. Open a terminal and navigate to the streamzap root directory
3. Run `pip install .` to install the streamzap script and download the depdencies
4. Start streamzap

## Usage

Make sure the Python script directory is in PATH and that streamzap has been installed.

### Starting

streamzap can be started from anywhere on your system with the following command

```
streamzap
```
