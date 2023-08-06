from qtpy import QtCore


class MousePanTilt(QtCore.QObject):
    """Event Filter for handling mouse gestures and clicks to triggering actions.
    """

    pantilt = QtCore.Signal(float, float)
    zoom = QtCore.Signal(float)

    def __init__(self):
        super().__init__()

        self._mouse_pos = None
    # end Constructor

    def eventFilter(self, receiver, event):
        """Event filter for key press and release setting the key values and sending the signal."""
        etype = event.type()

        # Check for pantilt
        if etype == QtCore.QEvent.MouseButtonPress:
            self._mouse_pos = event.posF()
            return True

        elif etype == QtCore.QEvent.MouseButtonRelease and self._mouse_pos is not None:
            end_pos = event.posF()
            if self._mouse_pos == end_pos:
                # Calculate offset from center
                center_w = receiver.width() / 2
                center_h = receiver.height() / 2
                pantilt = QtCore.QPointF((self._mouse_pos.x() - center_w) / center_w,
                                         (center_h - self._mouse_pos.y()) / center_h)
            else:
                # Calculate offset dragged
                pantilt = QtCore.QPointF((end_pos.x() - self._mouse_pos.x()) / receiver.width(),
                                         (self._mouse_pos.y() - end_pos.y()) / receiver.height())

            self.pantilt.emit(pantilt.x(), pantilt.y())
            self._mouse_pos = None
            return True

        return super().eventFilter(receiver, event)
    # end eventFilter
# end class MousePanTilt


if __name__ == "__main__":
    from PySide import QtGui

    QtGui.QApplication([])

    widg = QtGui.QWidget()
    widg.show()
    mouse = MousePanTilt()
    mouse.pantilt.connect(print)
    widg.installEventFilter(mouse)

    QtGui.qApp.exec_()
