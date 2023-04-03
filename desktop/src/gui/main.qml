import QtQuick 2.15
import QtQuick.Window 2.15

Window {
  id: window
  flags: Qt.Window | Qt.FramelessWindowHint
  width: 1000
  height: 500
  visible: true
  color: "transparent"
  title: qsTr("foggie")

  Rectangle {
    anchors.fill: parent
    radius: 8
    color: "#1c1e28"
  }

  Rectangle {
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    color: "transparent"
    height: 20

    MouseArea {
      anchors.fill: parent
      onPressed: window.startSystemMove()
    }
  }

  Rectangle {
    anchors.right: parent.right
    anchors.bottom: parent.bottom
    color: "transparent"
    width: 10
    height: 10

    MouseArea {
      anchors.fill: parent
      cursorShape: Qt.SizeFDiagCursor
      onPressed: window.startSystemResize(Qt.RightEdge | Qt.BottomEdge)
    }
  }
}