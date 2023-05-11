import QtQuick 2.15
import QtQuick.Controls 2.15

ComboBox {
  id: combo
  font.pointSize: 14

  property var notHoveredColor: "black"
  property var hoveredColor: Qt.darker("#0E151E", 1.5)
  property var selectionColor: "#0079F2"

  delegate: ItemDelegate {
    text: modelData
    font.pointSize: 12
    width: parent.width
    background: Rectangle {
      anchors.fill: parent
      color: hovered ? selectionColor : notHoveredColor
    }
  }

  background: Rectangle {
    anchors.fill: parent
    color: notHoveredColor
    implicitWidth: 100
    implicitHeight: 30
    radius: 4

    MouseArea {
      anchors.fill: parent
      cursorShape: Qt.PointingHandCursor
      hoverEnabled: true
      onEntered: parent.color = combo.hoveredColor
      onExited: parent.color = combo.notHoveredColor
    }
  }
}