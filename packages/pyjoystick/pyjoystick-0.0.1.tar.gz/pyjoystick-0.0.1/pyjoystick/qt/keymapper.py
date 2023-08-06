"""
    bt_controller.keymapper
    SeaLandAire Technologies
    @author: jengel
"""
import threading
from qtpy import QtCore, QtGui, QtWidgets

from pyjoystick.interface import Joystick


class JoystickKeyMapper(QtWidgets.QWidget):
    """Help the user map the keys."""

    Joystick = Joystick

    def __init__(self, joystick=None, parent=None, event_mngr=None):
        super().__init__(parent)

        self._event_mngr = None
        self.joystick = None
        self._joysticks = []
        self.btns_per_row = 5

        # Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        # Joystick name
        self.name_lbl = QtWidgets.QLabel("Joystick Name")
        self.name_lbl.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        font = self.name_lbl.font()
        font.setPointSize(12)
#         font.setWeight(QtWidgets.QFont.Bold)
        self.name_lbl.setFont(font)
        self.name_lay = QtWidgets.QHBoxLayout()
        self.name_lay.addWidget(self.name_lbl, alignment=QtCore.Qt.AlignLeft)
        self.main_layout.addLayout(self.name_lay)
        
        # Button layouts
        lbl = QtWidgets.QLabel("Axes (Analog sticks or triggers):")
        lbl.setToolTip("Values are scaled -100.0 to 100.0 for the slider display.\n"
                       "real values are -1.0 to 1.0")
        self.main_layout.addWidget(lbl)
        self.axis_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.axis_layout)

        self.main_layout.addWidget(QtWidgets.QLabel("Buttons:"))
        self.button_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.main_layout.addWidget(QtWidgets.QLabel("Hats (D-pads):"))
        self.hat_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.hat_layout)

        self.main_layout.addWidget(QtWidgets.QLabel("Track Balls:"))
        self.ball_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.ball_layout)

        # Select joystick button
        self.sel_btn = QtWidgets.QPushButton("Select Joystick")
        self.sel_btn.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.sel_btn.clicked.connect(self.select_joystick)
        self.name_lay.addWidget(self.sel_btn, alignment=QtCore.Qt.AlignLeft)
        self._dialog = None

        # Items
        self._lock = threading.Lock()
        if joystick is not None:
            self.sel_btn.hide()
            self.set_joystick(joystick)

        if event_mngr is not None:
            self.set_event_mngr(event_mngr)
    # end Constructor

    def get_event_mngr(self):
        """Return the event manager."""
        return self._event_mngr

    def set_event_mngr(self, value):
        """Set the event manager."""
        self._event_mngr = value
        try:
            self._event_mngr.add_joystick = self.add_joystick
            self._event_mngr.remove_joystick = self.remove_joystick
            self._event_mngr.handle_key_event = self.handle_key_event
            self._event_mngr.start()
        except:
            pass

    event_mngr = property(get_event_mngr, set_event_mngr)

    def add_joystick(self, joy):
        """Add the joystick that was found."""
        self._joysticks.append(joy)

    def remove_joystick(self, joy):
        """Remove teh joystick that was removed."""
        try:
            self._joysticks.remove(joy)
        except:
            pass

    def handle_key_event(self, key):
        """Handle the given key that an event occurred on."""
        if self.joystick != key.joystick:
            return

        if key.keytype == key.AXIS:
            self.set_axes_values(key)
        elif key.keytype == key.BUTTON:
            self.set_button_values(key)
        elif key.keytype == key.HAT:
            self.set_hat_values(key)
        elif key.keytype == key.BALL:
            self.set_ball_values(key)

    def get_joysticks(self):
        """Return a list of joysticks."""
        return self._joysticks

    def select_joystick(self):
        """Select a gamepad if there is no joystick selected."""
        try: self._dialog.close()
        except AttributeError: pass

        self._dialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout()
        self._dialog.setLayout(layout)
        
        # Joysticks
        btngroup = QtWidgets.QButtonGroup()
        btngroup.setExclusive(True)
        for item in self.get_joysticks():
            btn = QtWidgets.QRadioButton(item.get_name())
            layout.addWidget(btn)
            btngroup.addButton(btn)

        # Accept method        
        def select():
            btn = btngroup.checkedButton()
            joystick = None
            if btn is not None:
                name = btn.text()
                for joy in self.get_joysticks():
                    if joy.get_name() == name:
                        joystick = joy
                        break
            self.set_joystick(joystick)
            self._dialog.close()

        # Buttons
        accept = QtWidgets.QPushButton("Select")
        accept.clicked.connect(select)
        cancel = QtWidgets.QPushButton("Cancel")
        cancel.clicked.connect(self._dialog.close)

        # Button layout
        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget(accept, alignment=QtCore.Qt.AlignRight)
        hlay.addWidget(cancel, alignment=QtCore.Qt.AlignRight)
        layout.addLayout(hlay)
        self._dialog.show()

    def _clear_layout(self, layout):
        """Clear a layout."""
        while layout.itemAt(0) is not None:
            item = layout.takeAt(0)
            try:
                obj = item.widget()
                if obj is None:
                    obj = item.layout()
                    self._clear_layout(obj)
                    obj.setParent(None)
                    obj.deleteLater()
                else:
                    obj.close()
                    obj.setParent(None)
                    obj.deleteLater()
            except AttributeError:
                pass
            del item

    def removeWidgets(self):
        """Remove all of the testing widgets."""
        self._clear_layout(self.axis_layout)
        self._clear_layout(self.button_layout)
        self._clear_layout(self.hat_layout)
        self._clear_layout(self.ball_layout)

    def createWidgets(self, joystick=None):
        """Initialize the widgets."""
        self.removeWidgets()

        for i in range(joystick.get_numaxes()):
            widg = AxisWidget("Axis "+str(i))
            self.axis_layout.addWidget(widg)

        btn_lay = []
        for i in range(joystick.get_numbuttons()):
            if (i % self.btns_per_row) == 0:
                btn_lay.append(QtWidgets.QHBoxLayout())
                self.button_layout.addLayout(btn_lay[-1])
            widg = ButtonWidget("Button "+str(i)+":")
            btn_lay[-1].addWidget(widg)

        for i in range(joystick.get_numhats()):
            widg = HatWidget("Hat "+str(i)+":")
            self.hat_layout.addWidget(widg)

        for i in range(joystick.get_numballs()):
            widg = HatWidget("Ball "+str(i)+":")
            self.ball_layout.addWidget(widg)

    def set_joystick(self, joystick):
        """Set the active joystick."""
        if joystick is None:
            self.removeWidgets()
            return

        self.joystick = joystick
        self.createWidgets(self.joystick)
        try:
            self.name_lbl.setText(self.joystick.get_name())
        except:
            pass

    def set_axes_values(self, key):
        self.axis_layout.itemAt(key.number).widget().setValue(key.get_value())

    def set_button_values(self, key):
        btn_lay = self.button_layout.itemAt(int(key.number // self.btns_per_row)).layout()
        btn_lay.itemAt(key.number % self.btns_per_row).widget().setValue(key.get_value())

    def set_hat_values(self, key):
        self.hat_layout.itemAt(key.number).widget().setValue(key.get_value())

    def set_ball_values(self, key):
        self.ball_layout.itemAt(key.number).widget().setValue(key.get_value())

    def closeEvent(self, *args, **kwargs):
        try:
            self._event_mngr.stop()
        except:
            pass
        return QtWidgets.QWidget.closeEvent(self, *args, **kwargs)


class AxisWidget(QtWidgets.QWidget):
    def __init__(self, title=""):
        super().__init__()

        # Layout
        self._thread_value = False
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self._value = 0
        self.title = QtWidgets.QLabel(title)
        self.slider = SpinSlider(-100.0, 100.0, decimals=2)
        self.slider.setReadOnly(True)
        self.slider.setTickInterval(10)
        self.slider.setMinimumHeight(200)
        self.slider.setOrientation(QtCore.Qt.Vertical)
        self.slider.setValue(0)
        
        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(self.title)
    # end Constructor
    
    def setValue(self, value):
        self._value = value * 100
        self._thread_value = False
        if threading.current_thread() != threading.main_thread():
            # Make thread safe!
            self._thread_value = True
            self.update()
        else:
            self.slider.setValue(self._value)

    def paintEvent(self, event):
        if self._thread_value:
            # Make thread safe!
            self.slider.setValue(self._value)
            self._thread_value = False
        return super().paintEvent(event)
# end class AxisWidget


class ButtonWidget(QtWidgets.QWidget):
    def __init__(self, title=""):
        super().__init__()

        # Layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self._thread_value = False
        self._value = 0
        self.title = QtWidgets.QLabel(title)
        self.led = LED()
        self.led.setValue(0)
        
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.led)
        
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
    # end Constructor
    
    def setValue(self, value):
        self._value = value
        self._thread_value = False
        if threading.current_thread() != threading.main_thread():
            # Make thread safe!
            self._thread_value = True
            self.update()
        else:
            self.led.setValue(self._value)

    def paintEvent(self, event):
        if self._thread_value:
            # Make thread safe!
            self.led.setValue(self._value)
            self._thread_value = False
        return super().paintEvent(event)
# end ButtonWidget


class HatWidget(QtWidgets.QWidget):
    def __init__(self, title=""):
        super().__init__()

        # Layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self._value = ""
        self._thread_value = False
        self.title = QtWidgets.QLabel(title)
        self.edit = QtWidgets.QLineEdit()
        self.edit.setMaximumWidth(100)
        self.edit.setReadOnly(True)
        
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.edit)
        
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
    # end Constructor

    def setValue(self, value):
        self._value = str(value)
        self._thread_value = False
        if threading.current_thread() != threading.main_thread():
            # Make thread safe!
            self._thread_value = True
            self.update()
        else:
            self.edit.setText(self._value)

    def paintEvent(self, event):
        if self._thread_value:
            # Make thread safe!
            self.edit.setText(self._value)
            self._thread_value = False
        return super().paintEvent(event)
# end HatWidget


class SpinSlider(QtWidgets.QWidget):
    """Custom slider that displays the minimum, maximum, and spinbox next to the slider to aid in
    usability.
    
    Args:
        minimum (int)[None]: Minimum value
        maximum (int)[None]: Maximum value
        decimals (int)[0]: Number of decimals to display and control.
    """
    # Signals
    actionTriggered = QtCore.Signal(object)
    rangeChanged = QtCore.Signal(object, object)
    sliderMoved = QtCore.Signal(object)
    sliderPressed = QtCore.Signal()
    sliderReleased = QtCore.Signal()
    valueChanged = QtCore.Signal(object)

    # Slider class attributes
    TickPosition = QtWidgets.QSlider.TickPosition
    NoTicks = QtWidgets.QSlider.NoTicks
    TicksAbove = QtWidgets.QSlider.TicksAbove
    TicksBelow = QtWidgets.QSlider.TicksBelow
    TicksBothSides = QtWidgets.QSlider.TicksBothSides
    TicksLeft = QtWidgets.QSlider.TicksLeft
    TicksRight = QtWidgets.QSlider.TicksRight
    
    SliderAction = QtWidgets.QSlider.SliderAction
    SliderMove = QtWidgets.QSlider.SliderMove
    SliderNoAction = QtWidgets.QSlider.SliderNoAction
    SliderPageStepAdd = QtWidgets.QSlider.SliderPageStepAdd
    SliderPageStepSub = QtWidgets.QSlider.SliderPageStepSub
    SliderSingleStepAdd = QtWidgets.QSlider.SliderSingleStepAdd
    SliderSingleStepSub = QtWidgets.QSlider.SliderSingleStepSub
    SliderToMaximum = QtWidgets.QSlider.SliderToMaximum
    SliderToMinimum = QtWidgets.QSlider.SliderToMinimum
    
    SliderChange = QtWidgets.QSlider.SliderChange
    SliderOrientationChange = QtWidgets.QSlider.SliderOrientationChange
    SliderRangeChange = QtWidgets.QSlider.SliderRangeChange
    SliderStepsChange = QtWidgets.QSlider.SliderStepsChange
    SliderValueChange = QtWidgets.QSlider.SliderValueChange

    # SpinBox class attributes
    ButtonSymbols = QtWidgets.QDoubleSpinBox.ButtonSymbols
    NoButtons = QtWidgets.QDoubleSpinBox.NoButtons
    PlusMinus = QtWidgets.QDoubleSpinBox.PlusMinus
    UpDownArrows = QtWidgets.QDoubleSpinBox.UpDownArrows

    CorrectionMode = QtWidgets.QDoubleSpinBox.CorrectionMode
    CorrectToNearestValue = QtWidgets.QDoubleSpinBox.CorrectToNearestValue
    CorrectToPreviousValue = QtWidgets.QDoubleSpinBox.CorrectToPreviousValue

    StepEnabledFlag = QtWidgets.QDoubleSpinBox.StepEnabledFlag
    StepDownEnabled = QtWidgets.QDoubleSpinBox.StepDownEnabled
    StepNone = QtWidgets.QDoubleSpinBox.StepNone
    StepUPEnabled = QtWidgets.QDoubleSpinBox.StepUpEnabled

    def __init__(self, minimum=0, maximum=99, decimals=0, parent=None):
        super().__init__(parent)
        
        # Widgets
        self.spinbox = QtWidgets.QDoubleSpinBox()
        self.slider = QtWidgets.QSlider()
        self._min = QtWidgets.QLabel("0")
        self._max = QtWidgets.QLabel("99")
        self._value = 0
        self._thread_value = False

        # Check Inputs
        self.setDecimals(decimals)
        self.setRange(minimum, maximum)
        self.setValue(minimum)

        # Create the layout
        self.main_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.setLayout(self.main_layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
          
        self.main_layout.addWidget(self.spinbox)
        self.main_layout.addWidget(self._min)
        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(self._max)
        
        # Style
        self.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus) # Keyboard up and down -> spinbox
        
        # Signals
        self.slider.actionTriggered.connect(self.actionTriggered.emit)
        self.slider.rangeChanged.connect(self.rangeChanged.emit)
        self.slider.sliderMoved.connect(self.sliderMoved.emit)
        self.slider.sliderPressed.connect(self.sliderPressed.emit)
        self.slider.sliderReleased.connect(self.sliderReleased.emit)
        self.slider.valueChanged.connect(self._value_changed)
        self.spinbox.valueChanged.connect(self._value_changed)
    # end Constructor

    def _value_changed(self, value):
        """Sync the spinbox and slider values."""
        if self.spinbox.value() != value:
            self.spinbox.blockSignals(True)    
            self.spinbox.setValue(value)
            self.spinbox.blockSignals(False)
        if self.slider.value() != value:
            self.slider.blockSignals(True)
            self.slider.setValue(value)
            self.slider.blockSignals(False)
        self.valueChanged.emit(self.spinbox.value())
    # end _value_changed

    def isReadOnly(self):
        return self.spinbox.isReadOnly()
    def setReadOnly(self, value):
        self.slider.setEnabled(not value)
        self.spinbox.setReadOnly(value)
        if value:
            self.spinbox.setButtonSymbols(QtWidgets.QDoubleSpinBox.NoButtons)
        else:
            self.spinbox.setButtonSymbols(QtWidgets.QDoubleSpinBox.UpDownArrows)
    # end isReadOnly

    def decimals(self):
        """Return the decimals.
        
        Returns:
            decimals (int): Number of decimals that are available. 0 Means a regular spin box is used.
        """
        return self.spinbox.decimals()
    # end decimals
    
    def setDecimals(self, decimals):
        """Set the number of decimals.
        
        Args:
            decimals (int): Number of decimals to display.
        """
        self.spinbox.setDecimals(decimals)
        if decimals > 0:
            single_step = float("0."+str(1).zfill(decimals))
            self.spinbox.setSingleStep(single_step)
            self.slider.setSingleStep(single_step)
        elif self.spinbox.singleStep() < 1:
            self.spinbox.setSingleStep(1)
            self.slider.setSingleStep(1)
    # end setDecimals

    def minimum(self):
        """Return the minimum range value."""
        return self.slider.minimum()
    def setMinimum(self, minimum):
        """Set the minimum range value.

         Note:
             The default value is 0.

        Args:
            minimum (int/flaot): Minimum value.
        """
        self.slider.setMinimum(minimum)
        self.spinbox.setMinimum(minimum)
        self._min.setText(str(self.minimum()))
    # end setMinimum

    def maximum(self):
        """Return the maximum range value."""
        return self.slider.maximum()
    def setMaximum(self, maximum):
        """Set the maximum range value.

        Note:
             The default value is 99.

        Args:
            maximum (int/flaot): Maximum value.
        """
        self.slider.setMaximum(maximum)
        self.spinbox.setMaximum(maximum)
        self._max.setText(str(self.maximum()))
    # end setMinimum

    def setRange(self, minimum, maximum):
        """Set the min and max range.
        
        Args:
            minimum (int/flaot): Minimum value.
            maximum (int/flaot): Maximum value.
        """
        # flip
        if minimum > maximum:
            temp = minimum
            minimum = maximum
            maximum = temp

        self.slider.setRange(minimum, maximum)
        self.spinbox.setRange(minimum, maximum)

        self._min.setText(str(self.minimum()))
        self._max.setText(str(self.maximum()))
    # end setRange

    def singleStep(self):
        return self.spinbox.singleStep()
    def setSingleStep(self, value):
        self.spinbox.setSingleStep(value)
        self.slider.setSingleStep(value)
    # end singleStep
    
    def hasTracking(self):
        return self.slider.hasTracking()
    def setTracking(self, value):
        """Set if the valueChanged signal should be activated whenever the slider is moved."""
        self.slider.setTracking(value)
        self.spinbox.setKeyboardTracking(value)
    # end tracking
    
    def specialValueText(self):
        """This property holds the special-value text.

        If set, the spin box will display this text instead of a numeric value whenever the 
        current value is equal to minimum(). Typical use is to indicate that this choice has 
        a special (default) meaning.

        See Also:
            QAbstractSpinBox.specialValueText
        """
        return self.spinbox.specialValueText()
    def setSpecialValueText(self, text):
        self.spinbox.setSpecialValueText(text)
    # end setSpecialValueText

    # ========== Slider Override ==========
    def tickInterval(self):
        return self.slider.tickInterval()
    def setTickInterval(self, ti):
        if self.tickPosition() == QtWidgets.QSlider.NoTicks:
            self.slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider.setTickInterval(ti)
    # end tickInterval

    def tickPosition(self):
        return self.slider.tickPosition()
    def setTickPosition(self, position):
        self.slider.setTickPosition(position)
    # end tickPosition

    def invertedAppearance(self):
        """Return if the appearance is inverted."""
        return self.slider.invertedAppearance()
    def setInvertedAppearance(self, value):
        """Set the slider inverted appearance.

        Args:
            value (bool): Is the appearance backwards?
        """
        self.slider.setInvertedAppearance(value)
        self.setOrientation(self.orientation())
    # end invertedAppearance
    
    def invertedControls(self):
        return self.slider.invertedControls()
    def setInvertedControls(self, value):
        """Set if the keyboard controls for the slider should be inverted."""
        self.slider.setInvertedControls(value)
    # end invertedControls

    def isSliderDown(self):
        """Return if the slider is pressed down."""
        return self.slider.isSliderDown()
    def setSliderDown(self, value):
        self.slider.setSliderDown(value)
    # end isSliderDown
    
    def orientation(self):
        """Return the slider orientation."""
        return self.slider.orientation()
    def setOrientation(self, orientation):
        """Set the orientation."""
        self.slider.setOrientation(orientation)
        if orientation == QtCore.Qt.Horizontal:
            self.main_layout.insertWidget(1, self._min)
            self.main_layout.insertWidget(3, self._max)
            if self.invertedAppearance():
                self.main_layout.setDirection(QtWidgets.QBoxLayout.RightToLeft)
            else:
                self.main_layout.setDirection(QtWidgets.QBoxLayout.LeftToRight)
        else:
            self.main_layout.insertWidget(3, self._min)
            self.main_layout.insertWidget(1, self._max)
            if self.invertedAppearance():
                self.main_layout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
            else:
                self.main_layout.setDirection(QtWidgets.QBoxLayout.TopToBottom)
    # end setOrientation

    def pageStep(self):
        return self.slider.pageStep()
    def setPageStep(self, value):
        self.slider.setPageStep(value)
    # end pageStep

    def repeatAction(self):
        return self.slider.repeatAction()
    def setRepeatAction(self, action, thresholdTime=5000, repeatTime=50):
        self.slider.setRepeatAction(action, thresholdTime, repeatTime)
    # end repeatAction

    def sliderPosition(self):
        return self.slider.sliderPosition()
    def setSliderPosition(self, value):
        self.slider.setSliderPosition(value)
    # end sliderPosition

    def triggerAction(self, action):
        self.slider.triggerAction(action)
    # end triggerAction

    def value(self):
        """Return the value."""
        return self._value

    def setValue(self, value):
        self._value = value
        self._thread_value = False
        if threading.current_thread() != threading.main_thread():
            # Make thread safe!
            self._thread_value = True
            self.update()
        else:
            self.slider.setValue(self._value)
            self.spinbox.setValue(self._value)

    def paintEvent(self, event):
        if self._thread_value:
            # Make thread safe!
            self.slider.setValue(self._value)
            self.spinbox.setValue(self._value)
            self._thread_value = False
        return super().paintEvent(event)

    def sliderChange(self, change):
        self.slider.sliderChange(change)
    # end sliderChange
    
    # ========== SpinBox Override ==========
    def setCleanText(self, value):
        try:
            value = float(value)
        except: pass
        self.setValue(value)
    def cleanText(self):
        return self.spinbox.cleanText()
    # end cleanText
    
    def prefix(self):
        return self.spinbox.prefix()
    def setPrefix(self, prefix):
        self.spinbox.setPrefix(prefix)
    # end prefix

    def suffix(self):
        return self.spinbox.suffix()
    def setSuffix(self, suffix):
        self.spinbox.setSuffix(suffix)
    # end suffix

    def textFromValue(self, val):
        return self.spinbox.textFromValue(val)
    def valueFromText(self, text):
        return self.spinbox.valueFromText(text)
    # end textFromValue
# end class SpinSlider


class LED(QtWidgets.QWidget):
    """Display for showing an LED light color.
    
    This class can be used to show a Text Label and LED light or just an LED light. This class is
    also capable of making the LED a clickable button.
    """
    
    clicked = QtCore.Signal()
    
    def __init__(self, state=None):
        super().__init__()
        self.setObjectName("LED")
        self.setMinimumSize(14, 14)
        
        # Properties
        self._state = None
        self._colors = {}
        self._value = QtGui.QColor(255, 0, 0)
        self.alert_time = 1000
        self._timer_arg = "blank"
        self._alert_timer = QtCore.QTimer()
        self._alert_timer.setSingleShot(True)
        self._alert_timer.timeout.connect(self.alert_timeout)
        
        # Button Properties
        self._seq_iter = None
        self._btn_seq = None
        
        # Add Default Colors
        self.addColor("red", QtGui.QColor(255, 0, 0))
        self.addColor(0, QtGui.QColor(255, 0, 0))
        self.addColor("off", QtGui.QColor(255, 0, 0))
        self.addColor("no", QtGui.QColor(255, 0, 0))
        
        self.addColor("green", QtGui.QColor(0, 255, 0))
        self.addColor(1, QtGui.QColor(0, 255, 0))
        self.addColor("on", QtGui.QColor(0, 255, 0))
        self.addColor("yes", QtGui.QColor(0, 255, 0))
        
        self.addColor("yellow", QtGui.QColor(255, 255, 0))
        self.addColor(2, QtGui.QColor(255, 255, 0))
        
        self.addColor("blank", QtGui.QColor(225, 225, 225))
        self.addColor("gray", QtGui.QColor(225, 225, 225))
        self.addColor("grey", QtGui.QColor(225, 225, 225))
        self.addColor("colorless", QtGui.QColor(225, 225, 225))
        self.addColor(3, QtGui.QColor(225, 225, 225))
        
        self.addColor("blue", QtGui.QColor(65, 65, 255))
        self.addColor(4, QtGui.QColor(65, 65, 255))
        
        self.addColor("orange", QtGui.QColor(255, 153, 0))
        self.addColor(5, QtGui.QColor(255, 153, 0))

        # self.setButtonSequence([0, 1])
        self.setState(state)
    # end Constructor
    
    def state(self):
        """Return the current state identifier of the LED."""
        return self._state
    # end state
    
    def activeColor(self):
        """Return the active QColor of the LED."""
        return self._value
    # end activeColor
    
    def buttonSequence(self):
        """Return the button sequence list of states to change to on button click."""
        return self._btn_seq
    # end buttonSequnce
    
    def value(self):
        """Gets the state. This method was made to be an interchangeable 
        method with TextIndicator.
        """
        return self.state()
    # end value
    
    def setValue(self, value):
        """Sets the LED State. This method was made to be an interchangeable 
        method with TextIndicator.
        
        Args:
            value(key): Color key state to set the LED color.
        """
        self.setState(value)
    # end setValue
    
    def setColor(self, value):
        self.setState(value)
    # end setColor

    def setColors(self, colors):
        """A dictionary or list of colors.
        
        Args:
            colors(list):list of strings (rgb, rgba, or hex) or a list of QtGui.QColor's.
        """
        for color in colors:
            color = self.checkColor(color)
        self._colors = colors
        
        self.setState(self._state)
    # end setColors
    
    def addColor(self, state, color):
        """Add a color to the color changing dictionary."""
        color = self.checkColor(color)
        self._colors[state] = color
    # end addColor
    
    def setState(self, state):
        """Set the state of the LED and show the color for that state."""
        self._state = state
        try:
            color = self._colors[state]
        except KeyError:
            try:
                state = int(state)
            except(ValueError, TypeError):
                state = str(state)
            try:
                color = self._colors[state]
            except KeyError:
                color = self._colors["blank"]
            
        self._value = color
        self.update()
    # end
    
    @staticmethod
    def checkColor(color):
        """Check the given color and return a valid color."""
        valid_color = None
        if isinstance(color, str) and "," in color:
            valid_color = QtGui.QColor(color)
            
        elif isinstance(color, list):
            if len(color) == 4:
                valid_color = QtGui.QColor(color[0], color[1], color[2], color[3])
            else:
                valid_color = QtGui.QColor(color[0], color[1], color[2])
                
        elif isinstance(color, QtGui.QColor):
            valid_color = color
            
        return valid_color
    # end checkColor
    
    def setButtonSequence(self, sequence):
        """States for the color of the sequence. Allows button presses to cycle through a sequence.
        
        Args:
            sequence(iterable): Sequence of states when pressing the button.
        """
        self._btn_seq = sequence
        self._seq_iter = iter(self._btn_seq)

        self.clicked.connect(self.cycle_colors)
    # end setButtonSequence
    
    def alert(self, timeout=None, color="red", timeout_color="blank"):
        """Change the color for a given time then change back to the timeout_color.
        
        Args:
            timeout (int)[None]: Time in seconds. If None use alert_time property
            color (str)["red"]: Color to immediately change to.
            timeout_color (str)["blank"]: Color to reset the LED to after the timeout.
        """
        if timeout is None:
            timeout = self.alert_time
        self.setColor(color)
        self._timer_arg = timeout_color
        
        self._alert_timer.stop()
        self._alert_timer.start(timeout)
    # end alert
    
    def alert_timeout(self):
        """Method to run after the alert time to clear the alert LED."""
        self.setState(self._timer_arg)

    def cycle_colors(self):
        """Cycle Colors."""
        try:
            next_state = next(self._seq_iter)
        except StopIteration:
            self._seq_iter = iter(self._btn_seq)
            next_state = next(self._seq_iter)
        # end
        
        self.setState(next_state)
    # end cycle_colors

    def mousePressEvent(self, event):
        """Override to activate button click and change to the next state."""
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
    # end mousePressEvent
    
    def paintEvent(self, event):
        """Overrides the default paintEvent method to create the widget's 
        display.
        
        Args:
            event: needed for paintEvent super class method override
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.Antialiasing, True)
        
        # Get Black Background
        rect_back = self.getBackgroundRect()
        center = rect_back.center()
        radius = rect_back.width() + 0.0
        
        # Draw Black Background
        grad = QtGui.QRadialGradient(center, radius)
        grad.setColorAt(0.0, QtGui.QColor(255, 255, 255, 10))
        grad.setColorAt(0.90, QtGui.QColor(0, 0, 0, 255))
        grad.setColorAt(0.98, QtGui.QColor(0, 0, 0, 100))
        grad.setColorAt(1.0, QtGui.QColor(0, 0, 0, 255))
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setBrush(grad)
        painter.drawEllipse(center, radius, radius)
        
        # Get LED
        rect_val = self.getValueRect()
        center = rect_val.center()
        radius = rect_val.width() + 0.0
        
        # Draw LED
        red = self._value.red()
        green = self._value.green()
        blue = self._value.blue()
        grad = QtGui.QRadialGradient(center, radius)
        grad.setColorAt(0.0, QtGui.QColor(red, green, blue, 100))
        grad.setColorAt(0.95, QtGui.QColor(red, green, blue, 255))
        grad.setColorAt(1.0, QtGui.QColor(red, green, blue, 100))
        painter.setPen(self._value)
        painter.setBrush(grad)
        painter.drawEllipse(center, radius, radius)

        painter.end()
    # end paintEvent
    
    def getValueRect(self):
        """Return the value rectangel container."""
        width = self.width()
        height = self.height()
        
        radius = min(width/2, height/2)
        center = QtCore.QPoint(width/2, height/2)
        back_r = radius - radius/50
        led_r = back_r - back_r/10
        rect_val = self.rect()
        
        # Set the LED
        rect_val.setWidth(led_r)
        rect_val.setHeight(led_r)
        rect_val.moveCenter(center)
        
        return rect_val
    # end getValueRect
    
    def getBackgroundRect(self):
        """Return the background rectangel container."""
        width = self.width()
        height = self.height()
        
        radius = min(width/2, height/2)
        center = QtCore.QPoint(width/2, height/2)
        back_r = radius - radius/50
        rect_back = self.rect()
        
        # Set the LED
        rect_back.setWidth(back_r)
        rect_back.setHeight(back_r)
        rect_back.moveCenter(center)
        
        return rect_back
    # end getBackgroundRect
# end class LED


if __name__ == "__main__":
    import sys
    from pyjoystick import ThreadEventManager, ButtonHatRepeater
    from pyjoystick.sdl2 import Joystick, run_event_loop

    app = QtWidgets.QApplication([])

    w = JoystickKeyMapper(event_mngr=ThreadEventManager(run_event_loop, button_repeater=ButtonHatRepeater()))  # , activity_timeout=0.02))
    w.show()

    sys.exit(app.exec_())
