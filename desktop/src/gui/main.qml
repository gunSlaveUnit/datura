import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

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

    RowLayout {
      height: 20
      z: 1

      anchors.left: parent.left
      anchors.leftMargin: 8
      anchors.right: parent.right

      Text {
        text: "foggie$gunSlaveUnit"
        color: "white"
      }

      Text {
        text: "11.57$"
        color: "white"
      }

			Rectangle {
		    Layout.fillWidth: true
		    Layout.fillHeight: true
		    color: "transparent"

		    MouseArea {
		      anchors.fill: parent
		      onPressed: window.startSystemMove()
		    }
		  }

			Rectangle {
				implicitWidth: 30
				Layout.fillHeight: true
				color: "transparent"

				Text {
					anchors.centerIn: parent
					text: String.fromCodePoint("0x1F5D5")
					color: "white"
				}

				MouseArea {
					anchors.fill: parent
					hoverEnabled: true
					onEntered: parent.color = "gray"
					onClicked: window.showMinimized()
					onExited: parent.color = "transparent"
				}
			}

			Rectangle {
				implicitWidth: 30
				Layout.fillHeight: true
				color: "transparent"

				Text {
					anchors.centerIn: parent
					text: String.fromCodePoint("0x1F5D6")
					color: "white"
				}

				MouseArea {
					anchors.fill: parent
					hoverEnabled: true
					onEntered: parent.color = "gray"
					onClicked: window.showMaximized()
					onExited: parent.color = "transparent"
				}
			}

			Rectangle {
		    id: root
		    radius: 8
		    implicitWidth: 30
				Layout.fillHeight: true
				color: 'transparent'

				Text {
					z: 1
					anchors.centerIn: parent
					text: String.fromCodePoint("0x2A32")
					font.pointSize: 14
					color: "white"
				}

		    Rectangle {
	        id: clipper
	        width: 30
	        height: 20
	        color: 'transparent'
	        clip: true

	        Rectangle {
            id: clipped
            anchors.right: parent.right
            width: parent.width + radius
            height: parent.height + radius
            radius: root.radius
            color: 'transparent'
	        }
		    }

		    MouseArea {
	        anchors.fill: parent
					hoverEnabled: true
					onEntered: clipped.color = "gray"
					onClicked: window.close()
					onExited: clipped.color = "transparent"
		    }
			}
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