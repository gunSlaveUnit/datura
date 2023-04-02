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
    anchors.topMargin: defaultMargin * 4

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: ScrollBar.AlwaysOn

    ColumnLayout {
      anchors.fill: parent

      RowLayout {
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