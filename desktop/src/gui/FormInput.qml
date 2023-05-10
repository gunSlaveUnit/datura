import QtQuick 2.15
import QtQuick.Controls 2.15

TextField {
  id: input

  implicitWidth: 300
  font.pointSize: 14

  selectionColor: "#0053A6"

  property var notHoveredColor: "black"
  property var hoveredColor: Qt.darker("#0E151E", 1.5)

  background: Rectangle {
    color: input.notHoveredColor
    radius: 4

    MouseArea {
      anchors.fill: parent
      cursorShape: Qt.IBeamCursor
      hoverEnabled: true
      onEntered: parent.color = input.hoveredColor
      onExited: parent.color = input.notHoveredColor
    }
  }
}