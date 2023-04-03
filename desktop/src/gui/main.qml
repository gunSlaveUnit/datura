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

  property int defaultMargin: 8

  Rectangle {
    anchors.fill: parent
    radius: defaultMargin
    color: "#1c1e28"

    Rectangle {
      z: 1
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

    Item {
      id: titleBar
      height: 30
      anchors.left: parent.left
      anchors.right: parent.right
      anchors.top: parent.top

      Text {
        id: appTitle
        anchors.left: parent.left
        anchors.leftMargin: defaultMargin
        anchors.verticalCenter: parent.verticalCenter
        text: "foggie"
        color: "white"
      }

      Rectangle {
        anchors.left: appTitle.right
        anchors.right: minimizeWindowButton.left
        anchors.top: parent.top
        height: parent.height

		    color: "transparent"

		    MouseArea {
		      anchors.fill: parent
		      onPressed: window.startSystemMove()
		    }
		  }

      Rectangle {
        id: minimizeWindowButton
        anchors.top: parent.top
        anchors.right: maximizeWindowButton.left
        width: 30
        height: parent.height
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
        id: maximizeWindowButton
        anchors.top: parent.top
        anchors.right: closeWindowButton.left
        width: 30
        height: parent.height
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
        id: closeWindowButton
        anchors.top: parent.top
        anchors.right: parent.right
        width: 30
        radius: defaultMargin
        height: parent.height
        color: "transparent"

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
	        height: parent.height
	        color: "transparent"
	        clip: true

	        Rectangle {
            id: clipped
            anchors.right: parent.right
            width: parent.width + radius
            height: parent.height + radius
            radius: closeWindowButton.radius
            color: "transparent"
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

    Item {
      id: topMenuBar
      anchors.margins: defaultMargin
      anchors.left: parent.left
      anchors.right: parent.right
      anchors.top: titleBar.bottom
      height: 30

      Rectangle {
        id: libraryButton
        anchors.left: parent.left
        width: 80
        height: parent.height
        color: "transparent"
        radius: defaultMargin / 2

				Text {
					anchors.centerIn: parent
					text: qsTr("Library")
					color: "white"
					font.pointSize: 12
				}

				MouseArea {
					anchors.fill: parent
					hoverEnabled: true
					onEntered: parent.color = "gray"
					onExited: parent.color = "transparent"
				}
      }

      Rectangle {
        id: storeButton
        anchors.left: libraryButton.right
        width: 80
        height: parent.height
        color: "transparent"
        radius: defaultMargin / 2

				Text {
					anchors.centerIn: parent
					text: qsTr("Store")
					color: "white"
					font.pointSize: 12
				}

				MouseArea {
					anchors.fill: parent
					hoverEnabled: true
					onEntered: parent.color = "gray"
					onExited: parent.color = "transparent"
				}
      }

      Rectangle {
        anchors.left: storeButton.right
        width: 80
        height: parent.height
        color: "transparent"
        radius: defaultMargin / 2

				Text {
					anchors.centerIn: parent
					text: qsTr("Workshop")
					color: "white"
					font.pointSize: 12
				}

				MouseArea {
					anchors.fill: parent
					hoverEnabled: true
					onEntered: parent.color = "gray"
					onExited: parent.color = "transparent"
				}
      }
    }

    ScrollView {
      anchors.top: topMenuBar.bottom
      anchors.left: parent.left
      anchors.right: parent.right
      anchors.bottom: parent.bottom
      clip: true
      ScrollBar.vertical.policy: ScrollBar.AlwaysOn
      ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

      Item {
        id: wrapper
        anchors.fill: parent
        anchors.margins: defaultMargin

        Text {
	        id: gameTitle
	        anchors.top: parent.top
	        anchors.left: parent.left
	        text: qsTr("Guardians of the galaxy")
	        font.pointSize: 20
	        font.bold: true
	        color: "white"
	      }

	      Rectangle {
	        id: leftSwipeViewButton
	        z: 1
          anchors.top: game_screenshots_swipe_view.top
          anchors.bottom: game_screenshots_swipe_view.bottom
          anchors.left: game_screenshots_swipe_view.left
          width: game_screenshots_swipe_view.width / 10
          visible: game_screenshots_swipe_view.hovered

          Text {
            anchors.centerIn: parent
            color: game_screenshots_swipe_view.currentIndex > 0 ? "white" : "gray"
            text: qsTr("<")
            font.pointSize: 24
            font.bold: true
          }

			    gradient: Gradient {
			      orientation: Gradient.Horizontal
		        GradientStop { position: 1.0; color: "transparent" }
		        GradientStop { position: -0.5; color: "black" }
			    }

			    MouseArea {
			      anchors.fill: parent
			      cursorShape: Qt.PointingHandCursor
			      onClicked: game_screenshots_swipe_view.decrementCurrentIndex()
			    }
        }

        SwipeView {
          id: game_screenshots_swipe_view
          anchors.margins: defaultMargin
          anchors.top: gameTitle.bottom
          anchors.left: parent.left
          anchors.right: parent.right
          height: width * 9 / 16
          clip: true

          Repeater {
            model: 6

            Image {
              source: "./resources/16x9_placeholder.jpg"
              mipmap: true
            }
          }
        }

        Rectangle {
	        id: rightSwipeViewButton
	        z: 1
          anchors.top: game_screenshots_swipe_view.top
          anchors.bottom: game_screenshots_swipe_view.bottom
          anchors.right: game_screenshots_swipe_view.right
          width: game_screenshots_swipe_view.width / 10
          visible: game_screenshots_swipe_view.hovered

          Text {
            anchors.centerIn: parent
            color: game_screenshots_swipe_view.currentIndex < game_screenshots_swipe_view.count - 1 ? "white" : "gray"
            text: qsTr(">")
            font.pointSize: 24
            font.bold: true
          }

			    gradient: Gradient {
              orientation: Gradient.Horizontal
              GradientStop { position: 0.0; color: "transparent" }
              GradientStop { position: 1.5; color: "black" }
          }

			    MouseArea {
			      anchors.fill: parent
			      cursorShape: Qt.PointingHandCursor
			      onClicked: game_screenshots_swipe_view.incrementCurrentIndex()
			    }
        }
      }
    }
  }
}