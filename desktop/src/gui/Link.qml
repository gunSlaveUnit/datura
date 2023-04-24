import QtQuick 2.15
import QtQuick.Controls 2.15

Span {
  id: text

  property string message: ""

  function handler() {}

  property var notHoveredColor: "#ddd"
  property var hoveredColor: "#fff"

  text: message
  font.underline: true
  font.bold: true

  MouseArea {
    anchors.fill: parent
    cursorShape: Qt.PointingHandCursor
    hoverEnabled: true
    onClicked: handler()
    onEntered: parent.color = text.hoveredColor
    onExited: parent.color = text.notHoveredColor
  }
}