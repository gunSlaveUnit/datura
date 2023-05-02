import QtQuick 2.15
import QtQuick.Controls 2.15

ComboBox {
  id: combo
  font.pointSize: 12

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
    implicitWidth: 20
    implicitHeight: 20
    radius: 4

    MouseArea {
      anchors.fill: parent
      cursorShape: Qt.PointingHandCursor
      hoverEnabled: true
      onEntered: parent.color = combo.hoveredColor
      onExited: parent.color = combo.notHoveredColor
    }

    Image {
      anchors.margins: 8
      anchors.right: parent.right
      width: height * 0.8
      height: parent.height - 12
      anchors.verticalCenter: parent.verticalCenter
      mipmap: true
      source: "../../resources/icons/dropdown.png"
    }
  }
}