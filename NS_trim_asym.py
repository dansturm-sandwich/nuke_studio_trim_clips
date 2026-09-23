import hiero.core
import hiero.ui
from PySide6 import QtWidgets


def ask_handles():
    dialog = QtWidgets.QDialog(hiero.ui.mainWindow())
    dialog.setWindowTitle("Trim Handles")

    layout = QtWidgets.QFormLayout(dialog)

    heads_box = QtWidgets.QSpinBox()
    heads_box.setRange(0, 9999)
    heads_box.setValue(0)

    tails_box = QtWidgets.QSpinBox()
    tails_box.setRange(0, 9999)
    tails_box.setValue(0)

    layout.addRow("Heads", heads_box)
    layout.addRow("Tails", tails_box)

    buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.StandardButton.Ok
        | QtWidgets.QDialogButtonBox.StandardButton.Cancel
    )
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setDefault(True)
    layout.addRow(buttons)

    if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
        return None
    return heads_box.value(), tails_box.value()


handles = ask_handles()
if not handles:
    print("Trim cancelled.")
else:
    heads, tails = handles
    removed = heads + tails
    sequence = hiero.ui.activeSequence()
    if not sequence:
        raise RuntimeError("No active sequence.")

    if removed == 0:
        print("Heads and tails are both 0. Nothing trimmed.")
    else:
        selection = hiero.ui.getTimelineEditor(sequence).selection()
        project = sequence.project()
        project.beginUndo("Trim handles ({0} head, {1} tail)".format(heads, tails))
        trimmed = 0

        try:
            by_track = {}
            for item in selection:
                if not isinstance(item, hiero.core.TrackItem):
                    continue
                by_track.setdefault(item.parentTrack(), []).append(item)

            for items in by_track.values():
                items.sort(key=lambda track_item: track_item.timelineIn())
                trimmed_before = 0
                for item in items:
                    if item.timelineOut() - item.timelineIn() < removed:
                        continue
                    if item.sourceOut() - item.sourceIn() < removed:
                        continue

                    in_offset = item.timelineIn()
                    out_offset = item.timelineOut() - removed
                    srcin_offset = item.sourceIn() + heads
                    srcout_offset = item.sourceOut() - tails
                    item.setTimes(in_offset, out_offset, srcin_offset, srcout_offset)
                    trimmed += 1

                    if item.timelineIn() > 0 and trimmed_before:
                        try:
                            item.move(trimmed_before * (-removed))
                        except Exception:
                            pass
                    trimmed_before += 1
        finally:
            project.endUndo()

        print("Trimmed {0} clips. Heads {1}, tails {2}.".format(trimmed, heads, tails))
