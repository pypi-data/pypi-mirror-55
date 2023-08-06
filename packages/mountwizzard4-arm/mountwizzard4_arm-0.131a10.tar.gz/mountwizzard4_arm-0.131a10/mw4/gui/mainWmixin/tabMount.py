############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.7.4
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
# standard libraries
import datetime
# external packages
import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.uic
from mountcontrol.convert import stringToAngle
# local import
from mw4.base import transform


class Mount(object):
    """
    the main window class handles the main menu as well as the show and no show part of
    any other window. all necessary processing for functions of that gui will be linked
    to this class. therefore window classes will have a threadpool for managing async
    processing if needed.
    """

    def __init__(self):
        ms = self.app.mount.signals
        ms.locationDone.connect(self.updateLocGUI)
        ms.pointDone.connect(self.updatePointGUI)
        ms.pointDone.connect(self.updateTimeGUI)
        ms.settingDone.connect(self.updateSettingGUI)
        ms.settingDone.connect(self.updateSetStatGUI)
        ms.locationDone.connect(self.updateTrackingGui)

        self.ui.park.clicked.connect(self.changePark)
        self.ui.tracking.clicked.connect(self.changeTracking)
        self.ui.setLunarTracking.clicked.connect(self.setLunarTracking)
        self.ui.setSiderealTracking.clicked.connect(self.setSiderealTracking)
        self.ui.setSolarTracking.clicked.connect(self.setSolarTracking)
        self.ui.stop.clicked.connect(self.stop)
        self.clickable(self.ui.meridianLimitTrack).connect(self.setMeridianLimitTrack)
        self.clickable(self.ui.meridianLimitSlew).connect(self.setMeridianLimitSlew)
        self.clickable(self.ui.horizonLimitHigh).connect(self.setHorizonLimitHigh)
        self.clickable(self.ui.horizonLimitLow).connect(self.setHorizonLimitLow)
        self.clickable(self.ui.slewRate).connect(self.setSlewRate)
        self.clickable(self.ui.siteLatitude).connect(self.setLatitude)
        self.clickable(self.ui.siteLongitude).connect(self.setLongitude)
        self.clickable(self.ui.siteElevation).connect(self.setElevation)
        self.clickable(self.ui.statusUnattendedFlip).connect(self.setUnattendedFlip)
        self.clickable(self.ui.statusDualAxisTracking).connect(self.setDualAxisTracking)
        self.clickable(self.ui.statusRefraction).connect(self.setRefraction)
        self.clickable(self.ui.statusRefraction_2).connect(self.setRefraction)

    def initConfig(self):
        """
        initConfig read the key out of the configuration dict and stores it to the gui
        elements. if some initialisations have to be proceeded with the loaded persistent
        data, they will be launched as well in this method.

        :return: True for test purpose
        """
        config = self.app.config['mainW']
        self.ui.checkJ2000.setChecked(config.get('checkJ2000', False))
        self.ui.checkJNow.setChecked(config.get('checkJNow', False))

        # showing once location data, because without mount heartbeat it won't show up
        self.updateLocGUI(self.app.mount.obsSite)
        return True

    def storeConfig(self):
        """
        storeConfig writes the keys to the configuration dict and stores. if some
        saving has to be proceeded to persistent data, they will be launched as
        well in this method.

        :return: True for test purpose
        """
        config = self.app.config['mainW']
        config['checkJ2000'] = self.ui.checkJ2000.isChecked()
        config['checkJNow'] = self.ui.checkJNow.isChecked()
        return True

    def updatePointGUI(self, obs):
        """
        updatePointGUI update the gui upon events triggered be the reception of new data
        from the mount. the mount data is polled, so we use this signal as well for the
        update process.

        :param obs:
        :return:    True if ok for testing
        """

        if obs.Alt is not None:
            self.ui.ALT.setText('{0:5.2f}'.format(obs.Alt.degrees))
        else:
            self.ui.ALT.setText('-')

        if obs.Az is not None:
            self.ui.AZ.setText('{0:5.2f}'.format(obs.Az.degrees))
        else:
            self.ui.AZ.setText('-')

        ra = obs.raJNow
        dec = obs.decJNow
        if self.ui.checkJ2000.isChecked():
            if ra is not None and dec is not None and obs.timeJD is not None:
                ra, dec = transform.JNowToJ2000(ra, dec, obs.timeJD)

        if ra is not None:
            raFormat = '{0:02.0f}:{1:02.0f}:{2:02.0f}'
            val = ra.hms()
            raText = raFormat.format(*val)
            self.ui.RA.setText(raText)
            self.ui.RAfloat.setText(f'{ra.hours:3.4f}')
        else:
            self.ui.RA.setText('-')
            self.ui.RAfloat.setText('-')

        if dec is not None:
            decFormat = '{sign}{0:02.0f}:{1:02.0f}:{2:02.0f}'
            val = dec.signed_dms()[1:4]
            decText = decFormat.format(*val, sign='+' if dec.degrees > 0 else '-')
            self.ui.DEC.setText(decText)
            self.ui.DECfloat.setText(f'{dec.degrees:+3.4f}')
        else:
            self.ui.DEC.setText('-')
            self.ui.DECfloat.setText('-')

        if obs.pierside is not None:
            self.ui.pierside.setText('WEST' if obs.pierside == 'W' else 'EAST')
        else:
            self.ui.pierside.setText('-')

        if obs.haJNow is not None:
            haFormat = '{0:02.0f}:{1:02.0f}:{2:02.0f}'
            val = obs.haJNow.hms()
            haText = haFormat.format(*val)
            self.ui.HA.setText(haText)
            self.ui.HAfloat.setText(f'{obs.haJNow.hours:3.4f}')
        else:
            self.ui.HA.setText('-')
            self.ui.HAfloat.setText('-')

        return True

    def updateTimeGUI(self, obs):
        """
        updateTimeGUI update the gui upon events triggered be the reception of new data
        from the mount. the mount data is polled, so we use this signal as well for the
        update process.

        :param obs:
        :return:    True if ok for testing
        """

        if obs.timeJD is not None:
            text = obs.timeJD.utc_strftime('%H:%M:%S')
            self.ui.timeJD.setText(text)
            self.ui.timeUTC.setText('UTC: ' + text)
        else:
            self.ui.timeJD.setText('-')

        if obs.timeSidereal is not None:
            siderealFormat = '{0:02.0f}:{1:02.0f}:{2:02.0f}'
            val = obs.timeSidereal.hms()
            siderealText = siderealFormat.format(*val)
            self.ui.timeSidereal.setText(siderealText)
        else:
            self.ui.timeSidereal.setText('-')

        return True

    def updateSetStatGUI(self, sett):
        """
        updateSetStatGUI update the gui upon events triggered be the reception of new
        settings from the mount. the mount data is polled, so we use this signal as well
        for the update process.

        :param sett:
        :return:    True if ok for testing
        """

        if sett.UTCExpire is not None:
            ui = self.ui.UTCExpire
            ui.setText(sett.UTCExpire)
            # coloring if close to end:
            now = datetime.datetime.now()
            expire = datetime.datetime.strptime(sett.UTCExpire, '%Y-%m-%d')
            deltaYellow = datetime.timedelta(days=30)
            if now > expire:
                self.changeStyleDynamic(ui, 'color', 'red')
            elif now > expire - deltaYellow:
                self.changeStyleDynamic(ui, 'color', 'yellow')
            else:
                self.changeStyleDynamic(ui, 'color', '')
        else:
            self.ui.UTCExpire.setText('-')

        if sett.statusUnattendedFlip is not None:
            self.ui.statusUnattendedFlip.setText('ON' if sett.statusUnattendedFlip else 'OFF')
        else:
            self.ui.statusUnattendedFlip.setText('-')

        if sett.statusDualAxisTracking is not None:
            self.ui.statusDualAxisTracking.setText('ON' if sett.statusDualAxisTracking else 'OFF')
        else:
            self.ui.statusDualAxisTracking.setText('-')

        if sett.statusRefraction is not None:
            self.ui.statusRefraction.setText('ON' if sett.statusRefraction else 'OFF')
            self.ui.statusRefraction_2.setText('ON' if sett.statusRefraction else 'OFF')
        else:
            self.ui.statusRefraction.setText('-')
            self.ui.statusRefraction_2.setText('-')

        if sett.gpsSynced is not None:
            self.ui.statusGPSSynced.setText('YES' if sett.gpsSynced else 'NO')
        else:
            self.ui.statusGPSSynced.setText('-')

        if sett.wakeOnLan is not None:
            self.ui.statusWOL.setText(sett.wakeOnLan)
        else:
            self.ui.statusWOL.setText('-')

        return True

    def updateSettingGUI(self, sett):
        """
        updateSettingGUI update the gui upon events triggered be the reception of new
        settings from the mount. the mount data is polled, so we use this signal as well
        for the update process.

        :return:    True if ok for testing
        """

        if sett.slewRate is not None:
            self.ui.slewRate.setText('{0:2.0f}'.format(sett.slewRate))
        else:
            self.ui.slewRate.setText('-')

        if sett.timeToFlip is not None:
            self.ui.timeToFlip.setText('{0:3.0f}'.format(sett.timeToFlip))
        else:
            self.ui.timeToFlip.setText('-')

        if sett.timeToMeridian() is not None:
            self.ui.timeToMeridian.setText('{0:3.0f}'.format(sett.timeToMeridian()))
        else:
            self.ui.timeToMeridian.setText('-')

        if sett.refractionTemp is not None:
            self.ui.refractionTemp.setText('{0:+4.1f}'.format(sett.refractionTemp))
            self.ui.refractionTemp1.setText('{0:+4.1f}'.format(sett.refractionTemp))
        else:
            self.ui.refractionTemp.setText('-')
            self.ui.refractionTemp1.setText('-')

        if sett.refractionPress is not None:
            self.ui.refractionPress.setText('{0:6.1f}'.format(sett.refractionPress))
            self.ui.refractionPress1.setText('{0:6.1f}'.format(sett.refractionPress))
        else:
            self.ui.refractionPress.setText('-')
            self.ui.refractionPress1.setText('-')

        if sett.meridianLimitTrack is not None:
            self.ui.meridianLimitTrack.setText(str(sett.meridianLimitTrack))
        else:
            self.ui.meridianLimitTrack.setText('-')

        if sett.meridianLimitSlew is not None:
            self.ui.meridianLimitSlew.setText(str(sett.meridianLimitSlew))
        else:
            self.ui.meridianLimitSlew.setText('-')

        if sett.horizonLimitLow is not None:
            self.ui.horizonLimitLow.setText(str(sett.horizonLimitLow))
        else:
            self.ui.horizonLimitLow.setText('-')

        if sett.horizonLimitHigh is not None:
            self.ui.horizonLimitHigh.setText(str(sett.horizonLimitHigh))
        else:
            self.ui.horizonLimitHigh.setText('-')

        return True

    def updateLocGUI(self, obs):
        """
        updateLocGUI update the gui upon events triggered be the reception of new
        settings from the mount. the mount data is polled, so we use this signal as well
        for the update process.

        :param obs:
        :return:    True if ok for testing
        """
        if obs is None:
            return False
        location = obs.location
        if location is None:
            return False
        lon = location.longitude.dstr().replace('deg', '')
        self.ui.siteLongitude.setText(lon)
        lat = location.latitude.dstr().replace('deg', '')
        self.ui.siteLatitude.setText(lat)
        self.ui.siteElevation.setText(str(location.elevation.m))

        return True

    def updateTrackingGui(self, obs):
        """
        updateTrackingGui update the gui upon events triggered be the reception of new
        settings from the mount. the mount data is polled, so we use this signal as well
        for the update process.

        :param obs:
        :return:    True if ok for testing
        """

        if obs is None:
            return False

        if obs.checkRateLunar():
            self.changeStyleDynamic(self.ui.setLunarTracking, 'running', 'true')
            self.changeStyleDynamic(self.ui.setSiderealTracking, 'running', 'false')
            self.changeStyleDynamic(self.ui.setSolarTracking, 'running', 'false')
        elif obs.checkRateSidereal():
            self.changeStyleDynamic(self.ui.setLunarTracking, 'running', 'false')
            self.changeStyleDynamic(self.ui.setSiderealTracking, 'running', 'true')
            self.changeStyleDynamic(self.ui.setSolarTracking, 'running', 'false')
        elif obs.checkRateSolar():
            self.changeStyleDynamic(self.ui.setLunarTracking, 'running', 'false')
            self.changeStyleDynamic(self.ui.setSiderealTracking, 'running', 'false')
            self.changeStyleDynamic(self.ui.setSolarTracking, 'running', 'true')

        return True

    def changeTracking(self):
        """

        :return:
        """

        obs = self.app.mount.obsSite
        if obs.status == 0:
            suc = obs.stopTracking()
            if not suc:
                self.app.message.emit('Cannot stop tracking', 2)
            else:
                self.app.message.emit('Stopped tracking', 0)
        else:
            suc = obs.startTracking()
            if not suc:
                self.app.message.emit('Cannot start tracking', 2)
            else:
                self.app.message.emit('Started tracking', 0)

        return True

    def changePark(self):
        """

        :return:
        """

        obs = self.app.mount.obsSite
        if obs.status == 5:
            suc = obs.unpark()
            if not suc:
                self.app.message.emit('Cannot unpark mount', 2)
            else:
                self.app.message.emit('Mount unparked', 0)
        else:
            suc = obs.park()
            if not suc:
                self.app.message.emit('Cannot park mount', 2)
            else:
                self.app.message.emit('Mount parked', 0)

        return True

    def setLunarTracking(self):
        """

        :return:
        """

        obs = self.app.mount.obsSite
        suc = obs.setLunarTracking()
        if not suc:
            self.app.message.emit('Cannot set tracking to Lunar', 2)
            return False
        else:
            self.app.message.emit('Tracking set to Lunar', 0)
            return True

    def setSiderealTracking(self):
        """

        :return:
        """

        obs = self.app.mount.obsSite
        suc = obs.setSiderealTracking()
        if not suc:
            self.app.message.emit('Cannot set tracking to Sidereal', 2)
            return False
        else:
            self.app.message.emit('Tracking set to Sidereal', 0)
            return True

    def setSolarTracking(self):
        """

        :return:
        """

        obs = self.app.mount.obsSite
        suc = obs.setSolarTracking()
        if not suc:
            self.app.message.emit('Cannot set tracking to Solar', 2)
            return False
        else:
            self.app.message.emit('Tracking set to Solar', 0)
            return True

    def stop(self):
        """

        :return:
        """

        obs = self.app.mount.obsSite
        suc = obs.stop()
        if not suc:
            self.app.message.emit('Cannot stop mount', 2)
            return False
        else:
            self.app.message.emit('Mount stopped', 0)
            return True

    def setMeridianLimitTrack(self):
        """
        setMeridianLimitTrack implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting
        actValue = sett.meridianLimitTrack

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getInt(self,
                               'Set Meridian Limit Track',
                               'Value (-20-20):',
                               actValue,
                               -20,
                               20,
                               1,
                               )

        if not ok:
            return False

        if sett.setMeridianLimitTrack(value):
            self.app.message.emit(f'Meridian Limit Track: [{value}]', 0)
            return True
        else:
            self.app.message.emit('Meridian Limit Track cannot be set', 2)
            return False

    def setMeridianLimitSlew(self):
        """
        setMeridianLimitSlew implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting
        actValue = sett.meridianLimitSlew

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getInt(self,
                               'Set Meridian Limit Slew',
                               'Value (-20-20):',
                               actValue,
                               -20,
                               20,
                               1,
                               )

        if not ok:
            return False

        if sett.setMeridianLimitSlew(value):
            self.app.message.emit(f'Meridian Limit Slew: [{value}]', 0)
            return True
        else:
            self.app.message.emit('Meridian Limit Slew cannot be set', 2)
            return False

    def setHorizonLimitHigh(self):
        """
        setHorizonLimitHigh implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting
        actValue = sett.horizonLimitHigh

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getInt(self,
                               'Set Horizon Limit High',
                               'Value (0-90):',
                               actValue,
                               0,
                               90,
                               1,
                               )

        if not ok:
            return False

        if sett.setHorizonLimitHigh(value):
            self.app.message.emit(f'Horizon Limit High: [{value}]', 0)
            return True
        else:
            self.app.message.emit('Horizon Limit High cannot be set', 2)
            return False

    def setHorizonLimitLow(self):
        """
        setHorizonLimitLow implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting
        actValue = sett.horizonLimitLow

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getInt(self,
                               'Set Horizon Limit Low',
                               'Value (0-90):',
                               actValue,
                               0,
                               90,
                               1,
                               )

        if not ok:
            return False

        if sett.setHorizonLimitLow(value):
            self.app.message.emit(f'Horizon Limit Low: [{value}]', 0)
            return True
        else:
            self.app.message.emit('Horizon Limit Low cannot be set', 2)
            return False

    def setSlewRate(self):
        """
        setSlewRate implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting
        actValue = sett.slewRate

        minRate = sett.slewRateMin
        maxRate = sett.slewRateMax
        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getInt(self,
                               'Set Slew Rate',
                               f'Value ({minRate}-{maxRate}):',
                               actValue,
                               minRate,
                               maxRate,
                               1,
                               )

        if not ok:
            return False

        if sett.setSlewRate(value):
            self.app.message.emit(f'Slew Rate: [{value}]', 0)
            return True
        else:
            self.app.message.emit('Slew Rate cannot be set', 2)
            return False

    def setLongitude(self):
        """
        setSiteLongitude implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        obs = self.app.mount.obsSite

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getText(self,
                                'Set Site Longitude',
                                'Value: (East positive)',
                                PyQt5.QtWidgets.QLineEdit.Normal,
                                obs.location.longitude.dstr(),
                                )
        if not ok:
            return False

        topo = (value,
                self.app.mount.obsSite.location.latitude,
                self.app.mount.obsSite.elevation.m)
        self.app.mount.obsSite.location = topo

        self.app.mount.obsSite.location.longitude = stringToAngle(value)

        if not self.app.mountUp:
            self.updateLocGUI(obs)
            return False

        if obs.setLongitude(value):
            self.app.message.emit(f'Longitude: [{value}]', 0)
            self.app.mount.getLocation()
            return True
        else:
            self.app.message.emit('Longitude cannot be set', 2)
            return False

    def setLatitude(self):
        """
        setSiteLatitude implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        obs = self.app.mount.obsSite

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getText(self,
                                'Set Site Latitude',
                                'Value:',
                                PyQt5.QtWidgets.QLineEdit.Normal,
                                obs.location.latitude.dstr(),
                                )
        if not ok:
            return False

        topo = (self.app.mount.obsSite.location.longitude,
                value,
                self.app.mount.obsSite.elevation.m)
        self.app.mount.obsSite.location = topo

        if not self.app.mountUp:
            self.updateLocGUI(obs)
            return False

        if obs.setLatitude(value):
            self.app.message.emit(f'Latitude: [{value}]', 0)
            self.app.mount.getLocation()
            return True
        else:
            self.app.message.emit('Latitude cannot be set', 2)
            return False

    def setElevation(self):
        """
        setSiteElevation implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        obs = self.app.mount.obsSite

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getDouble(self,
                                  'Set Site Elevation',
                                  'Value: (meters)',
                                  obs.location.elevation.m,
                                  0,
                                  8000,
                                  1,
                                  )
        if not ok:
            return False

        topo = (self.app.mount.obsSite.location.longitude,
                self.app.mount.obsSite.location.latitude,
                value)
        self.app.mount.obsSite.location = topo

        if not self.app.mountUp:
            self.updateLocGUI(obs)
            return False

        if obs.setElevation(value):
            self.app.message.emit(f'Elevation: [{value}]', 0)
            self.app.mount.getLocation()
            return True
        else:
            self.app.message.emit('Elevation cannot be set', 2)

    def setUnattendedFlip(self):
        """
        setUnattendedFlip implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getItem(self,
                                'Set Unattended Flip',
                                'Value: On / Off',
                                ['ON', 'OFF'],
                                0,
                                False,
                                )
        if not ok:
            return False

        suc = sett.setUnattendedFlip(value == 'ON')
        if suc:
            self.app.message.emit(f'Unattended flip set to [{value}]', 0)
        else:
            self.app.message.emit('Unattended flip cannot be set', 2)

        return suc

    def setDualAxisTracking(self):
        """
        setDualAxisTracking implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getItem(self,
                                'Set Dual Axis Tracking',
                                'Value: On / Off',
                                ['ON', 'OFF'],
                                0,
                                False,
                                )
        if not ok:
            return False

        suc = sett.setDualAxisTracking(value == 'ON')
        if suc:
            self.app.message.emit(f'Dual axis tracking set to [{value}]', 0)
        else:
            self.app.message.emit('Dual axis tracking cannot be set', 2)

        return suc

    def setRefraction(self):
        """
        setRefractionCorrection implements a modal dialog for entering the value

        :return:    success as bool if value could be changed
        """

        msg = PyQt5.QtWidgets.QMessageBox
        if not self.app.mountUp:
            msg.critical(self,
                         'Error Message',
                         'Value cannot be set when mount not connected !')
            return False

        sett = self.app.mount.setting

        dlg = PyQt5.QtWidgets.QInputDialog()
        value, ok = dlg.getItem(self,
                                'Set Refraction Correction',
                                'Value: On / Off',
                                ['ON', 'OFF'],
                                0,
                                False,
                                )
        if not ok:
            return False

        suc = sett.setRefraction(value == 'ON')
        if suc:
            self.app.message.emit(f'Refraction correction set to [{value}]', 0)
        else:
            self.app.message.emit('Refraction correction cannot be set', 2)

        return suc
