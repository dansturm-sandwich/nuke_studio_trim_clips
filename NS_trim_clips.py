import nuke
import nukescripts
import hiero.core
import hiero.ui
from PySide2 import QtCore, QtWidgets
from nukescripts import panels


class TrimClipsPanel(nukescripts.PythonPanel):

    def __init__(self, parent=None):
        super(TrimClipsPanel, self).__init__(parent)
        self.trim_frames = nuke.Int_Knob('trim_frames', 'Trim Frames')
        self.trim_frames.setValue(8)
        self.addKnob(self.trim_frames)
        self.trim_button = nuke.PyScript_Knob('trim_button', 'Trim Clips', command='')
        self.addKnob(self.trim_button)

    def knobChanged(self, knob):
        if knob is self.trim_button:
          self.trim_clips()

    def trim_clips(self):
        frames = int(self.trim_frames.getValue())
        selection = hiero.ui.getTimelineEditor(hiero.ui.activeSequence()).selection()
        for item in selection:
            if isinstance(item, hiero.core.TrackItem):
                in_offset = item.timelineIn()
                out_offset = item.timelineOut() - (2 * frames)
                srcin_offset = item.sourceIn() + frames
                srcout_offset = item.sourceOut() - frames
                item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)


panel = TrimClipsPanel()
panel.show()

