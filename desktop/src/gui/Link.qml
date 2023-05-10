import QtQuick 2.15
import QtQuick.Controls 2.15

Span {
  id: element

  function handler() {}

  property var notHoveredColor: "#B1B5BC"
  property var hoveredColor: "#ddd"

  font.underline: true
  font.bold: true

  MouseArea {
    anchors.fill: parent
    cursorShape: Qt.PointingHandCursor
    hoverEnabled: true
    onClicked: handler()
    onEntered: parent.color = element.hoveredColor
    onExited: parent.color = element.notHoveredColor
  }
}