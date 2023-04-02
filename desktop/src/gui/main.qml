import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

Window {
  id: mainWindow
  width: 1000
  height: 500
  title: qsTr("foogie")
  color: "#474b63"
  visible: true

  property int defaultMargin: 8

  RowLayout {
    Button {text: qsTr("Test 1")}
    Button {text: qsTr("Test 2")}
    Button {text: qsTr("Test 3")}
    Button {text: qsTr("Test 4")}
  }

  ScrollView {
    anchors.fill: parent

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: ScrollBar.AlwaysOn

    ColumnLayout {
      anchors.fill: parent
      anchors.topMargin: defaultMargin * 4

      RowLayout {
        id: assetsCarousel

        Button {
          Layout.fillHeight: true
          Layout.preferredWidth: 30
          text: "<"
          flat: true
          font.bold: true
          font.pointSize: 16
          enabled: game_screenshots_swipe_view.currentIndex > 0
          onClicked: game_screenshots_swipe_view.decrementCurrentIndex()
        }

        SwipeView {
          id: game_screenshots_swipe_view
          Layout.preferredWidth: 16 * 30
          Layout.preferredHeight: 9 * 30
          clip: true

          Repeater {
            model: 6

            Image {
              source: "./resources/16x9_placeholder.jpg"
              mipmap: true
              Layout.preferredWidth: 16 * 30
              Layout.preferredHeight: 9 * 30
            }
          }
        }

        Button {
          Layout.fillHeight: true
          Layout.preferredWidth: 30
          text: ">"
          flat: true
          font.bold: true
          font.pointSize: 16
          enabled: game_screenshots_swipe_view.currentIndex < game_screenshots_swipe_view.count - 1
          onClicked: game_screenshots_swipe_view.incrementCurrentIndex()
        }
      }

      TextArea {
        readOnly: true
        Layout.preferredWidth: assetsCarousel.width
        background: Rectangle { color: "transparent" }
        wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
        textFormat: TextEdit.RichText
        text: "<p align='justify'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>"
      }

      RowLayout {
        Text {
          text: qsTr("Buy")
        }

        Text {
          text: qsTr("Elden Ring")
        }

        ColumnLayout {
					Text {
            Layout.alignment: Qt.AlignHCenter
	          text: qsTr("60 $")
					}

          Text {
            Layout.alignment: Qt.AlignHCenter
	          text: qsTr("50 $")
          }

          Text {
            Layout.alignment: Qt.AlignHCenter
	          text: qsTr("-10 %")
          }
        }

        Button {
	        id: multipleActionButton
	        text: qsTr("Add to cart")
	        hoverEnabled: false

	        background: Rectangle {
	          radius: defaultMargin / 2
	          color: "#177246"

	          MouseArea {
	            anchors.fill: parent
	            hoverEnabled: true
	            onEntered: multipleActionButton.background.color = "#00a86b"
	            onExited: multipleActionButton.background.color = "#177246"
	          }
	        }
	      }
      }
    }
  }
}