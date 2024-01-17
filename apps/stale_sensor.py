import appdaemon.appapi as appapi
import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, time

#
# Notify stale sensors.
# Each minute last update of sensor is checked to see if it is higher than the configured value
#
# Args:
# sensor = sensor to monitor
# tiempo = minutes threshold to notify
# notify = comma separated list of notifiers
#

class StaleSensor(hass.Hass):

  def initialize(self):
    czas = self.get_now()
    self.log("Hello from AppDaemon")
    self.log("You are now ready to run Apps!" + czas)
