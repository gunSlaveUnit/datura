import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

Button {
  id: button

  function handler() {}
  hoverEnabled: false

  font.pointSize: 14
  font.bold: true

  property string notHoveredColor: "#0053A6"
  property string hoveredColor: "#0079F2"

  onClicked: handler()
  Keys.onReturnPressed: handler()
  Keys.onEnterPressed: handler()

  background: Rectangle {
    color: parent.visualFocus ? button.hoveredColor : button.notHoveredColor

    implicitWidth: parent.text.contentWidth

    radius: 4

    MouseArea {
      anchors.fill: parent
      hoverEnabled: true
      cursorShape: Qt.PointingHandCursor
      onEntered: parent.color = button.hoveredColor
      onExited: parent.color = button.notHoveredColor
    }
  }
}