import hiero.core
import hiero.ui
from PySide6 import QtCore, QtWidgets, QtGui


class TrimClipsPanel(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("com.dansturm.TrimClipsPanel.2")
        self.setWindowTitle("Trim Clips")

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        label = QtWidgets.QLabel("Frames")
        layout.addWidget(label)

        self.trim_frames = QtWidgets.QLineEdit("8")
        self.trim_frames.setValidator(QtGui.QIntValidator())
        self.trim_frames.setMinimumWidth(50)
        self.trim_frames.setMaximumWidth(50)
        layout.addWidget(self.trim_frames)

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

    def trim_clips_left(self):
        frames = int(self.trim_frames.text())
        sequence = hiero.ui.activeSequence()
        selection = hiero.ui.getTimelineEditor(sequence).selection()

        for index, item in enumerate(selection): 
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn()
                out_offset = item.timelineOut() - (2 * frames)
                original_timelineOut = item.timelineOut()
                srcin_offset = item.sourceIn() + frames
                srcout_offset = item.sourceOut() - frames
                item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)

    def trim_clips_center(self):
        frames = int(self.trim_frames.text())
        sequence = hiero.ui.activeSequence()
        selection = hiero.ui.getTimelineEditor(sequence).selection()

        for index, item in enumerate(selection): 
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn() + frames
                out_offset = item.timelineOut() - frames
                original_timelineOut = item.timelineOut()
                srcin_offset = item.sourceIn() + frames
                srcout_offset = item.sourceOut() - frames
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
        frames = int(self.trim_frames.text())
        sequence = hiero.ui.activeSequence()
        selection = hiero.ui.getTimelineEditor(sequence).selection()

        for index, item in enumerate(selection): 
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn()
                out_offset = item.timelineOut() - (2 * frames)
                original_timelineOut = item.timelineOut()
                srcin_offset = item.sourceIn() + frames
                srcout_offset = item.sourceOut() - frames
                item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)

                # Ripple clips for all tracks (currently commented out)
                # sequence.clearRange(out_offset, original_timelineOut, True)

                if item.timelineIn() > 0:
                    try:
                        item.move(index * (-frames * 2)) 
                    except Exception:
                        pass


# Show the panel
panelWidget = TrimClipsPanel()

wm = hiero.ui.windowManager()
wm.addWindow(panelWidget)