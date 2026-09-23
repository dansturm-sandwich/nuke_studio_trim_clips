import hiero.core
import hiero.ui
from PySide6 import QtCore, QtWidgets


class TrimEndOnePanel(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("com.dansturm.TrimEndOnePanel")
        self.setWindowTitle("Trim End 1")

        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.trim_button = QtWidgets.QPushButton("Trim End (1 frame)")
        self.trim_button.clicked.connect(self.trim_end_one)
        layout.addWidget(self.trim_button)

        layout.addStretch()
        self.setLayout(layout)

    def trim_end_one(self):
        frames = 1
        sequence = hiero.ui.activeSequence()
        if not sequence:
            return

        selection = hiero.ui.getTimelineEditor(sequence).selection()
        project = sequence.project()
        project.beginUndo("Trim 1 frame from end")

        try:
            by_track = {}
            for item in selection:
                if not isinstance(item, hiero.core.TrackItem):
                    continue
                by_track.setdefault(item.parentTrack(), []).append(item)

            for items in by_track.values():
                items.sort(key=lambda track_item: track_item.timelineIn())
                for index, item in enumerate(items):
                    if item.timelineOut() <= item.timelineIn():
                        continue
                    if item.sourceOut() <= item.sourceIn():
                        continue

                    in_offset = item.timelineIn()
                    out_offset = item.timelineOut() - frames
                    srcin_offset = item.sourceIn()
                    srcout_offset = item.sourceOut() - frames
                    item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)

                    if item.timelineIn() > 0:
                        try:
                            item.move(index * (-frames))
                        except Exception:
                            pass
        finally:
            project.endUndo()


panelWidget = TrimEndOnePanel()

wm = hiero.ui.windowManager()
wm.addWindow(panelWidget)
