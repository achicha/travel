Cheap tickets parser.

todo:

- cron -> celery
- celery/flower, to check processes
- add better readme
- add wizzair tickets
- round trips?
- docker?
- sentry logs
- grab -> requests
- if connection filed parse several times more.

Selenium dependencies:
- [Selenium ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) 
- yum provides */libgconf-2.so.4
- sudo yum install GConf2
- [chrome browser](https://sites.google.com/site/imemoryloss/redhat-as-es-centos/install-google-chrome-with-yum-on-fedora-15-14-centos-red-hat-rhel-6)
- sudo yum install Xvfb

run on server:
export DISPLAY=:99
Xvfb :99 -ac -screen 0 1280x1024x24 &
./run.py 
killall Xvfb