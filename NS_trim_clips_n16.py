import hiero.core
import hiero.ui
from PySide6 import QtCore, QtWidgets, QtGui


class TrimClipsPanel(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("com.dansturm.TrimClipsPanel.2")
        self.setWindowTitle("Trim Clips")

        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        heads_label = QtWidgets.QLabel("Heads")
        layout.addWidget(heads_label)

        self.heads = QtWidgets.QLineEdit("8")
        self.heads.setValidator(QtGui.QIntValidator(0, 9999))
        self.heads.setMinimumWidth(50)
        self.heads.setMaximumWidth(50)
        self.heads.textChanged.connect(self.on_heads_changed)
        layout.addWidget(self.heads)

        tails_label = QtWidgets.QLabel("Tails")
        layout.addWidget(tails_label)

        self.tails = QtWidgets.QLineEdit("8")
        self.tails.setValidator(QtGui.QIntValidator(0, 9999))
        self.tails.setMinimumWidth(50)
        self.tails.setMaximumWidth(50)
        self.tails.setEnabled(False)
        layout.addWidget(self.tails)

        self.asymmetrical = QtWidgets.QCheckBox("Asymmetrical")
        self.asymmetrical.toggled.connect(self.on_asymmetrical_toggled)
        layout.addWidget(self.asymmetrical)

        self.trim_button_slate = QtWidgets.QPushButton("Trim Slate (1 head frame)")
        self.trim_button_slate.clicked.connect(self.trim_clips_slate)
        layout.addWidget(self.trim_button_slate)

        self.trim_button_left = QtWidgets.QPushButton("Trim Clips (left)")
        self.trim_button_left.clicked.connect(self.trim_clips_left)
        layout.addWidget(self.trim_button_left)

        self.trim_button_center = QtWidgets.QPushButton("Trim Clips (center)")
        self.trim_button_center.clicked.connect(self.trim_clips_center)
        layout.addWidget(self.trim_button_center)
        
        self.trim_button_close = QtWidgets.QPushButton("Trim Clips (close)")
        self.trim_button_close.clicked.connect(self.trim_clips_close)
        layout.addWidget(self.trim_button_close)

        layout.addStretch()

        self.setLayout(layout)

    def on_asymmetrical_toggled(self, checked):
        self.tails.setEnabled(checked)
        if not checked:
            self.tails.setText(self.heads.text())

    def on_heads_changed(self, text):
        if not self.asymmetrical.isChecked():
            self.tails.setText(text)

    def handle_counts(self):
        heads = self.frame_count(self.heads)
        if self.asymmetrical.isChecked():
            tails = self.frame_count(self.tails)
        else:
            tails = heads
        return heads, tails

    def frame_count(self, field):
        text = field.text().strip()
        if not text:
            return 0
        return int(text)

    def trim_clips_left(self):
        heads, tails = self.handle_counts()
        removed = heads + tails
        sequence = hiero.ui.activeSequence()
        selection = hiero.ui.getTimelineEditor(sequence).selection()

        for index, item in enumerate(selection): 
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn()
                out_offset = item.timelineOut() - removed
                original_timelineOut = item.timelineOut()
                srcin_offset = item.sourceIn() + heads
                srcout_offset = item.sourceOut() - tails
                item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)

    def trim_clips_center(self):
        heads, tails = self.handle_counts()
        sequence = hiero.ui.activeSequence()
        selection = hiero.ui.getTimelineEditor(sequence).selection()

        for index, item in enumerate(selection): 
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn() + heads
                out_offset = item.timelineOut() - tails
                original_timelineOut = item.timelineOut()
                srcin_offset = item.sourceIn() + heads
                srcout_offset = item.sourceOut() - tails
                item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)    
    
    def trim_clips_slate(self):
        frames = 1
        sequence = hiero.ui.activeSequence()
        selection = hiero.ui.getTimelineEditor(sequence).selection()

        for index, item in enumerate(selection): 
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn()
                out_offset = item.timelineOut() - frames
                original_timelineOut = item.timelineOut()
                srcin_offset = item.sourceIn() + frames
                srcout_offset = item.sourceOut()
                item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)

                if item.timelineIn() > 0:
                    try:
                        item.move(index * (-frames)) 
                    except Exception:
                        pass

    def trim_clips_close(self):
        heads, tails = self.handle_counts()
        removed = heads + tails
        sequence = hiero.ui.activeSequence()
        selection = hiero.ui.getTimelineEditor(sequence).selection()

        for index, item in enumerate(selection): 
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn()
                out_offset = item.timelineOut() - removed
                original_timelineOut = item.timelineOut()
                srcin_offset = item.sourceIn() + heads
                srcout_offset = item.sourceOut() - tails
                item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)

                # Ripple clips for all tracks (currently commented out)
                # sequence.clearRange(out_offset, original_timelineOut, True)

                if item.timelineIn() > 0:
                    try:
                        item.move(index * (-removed)) 
                    except Exception:
                        pass


# Show the panel
panelWidget = TrimClipsPanel()

wm = hiero.ui.windowManager()
wm.addWindow(panelWidget)