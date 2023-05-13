import QtQuick 2.15
import QtQuick.Layouts 2.15
import QtQuick.Controls 2.15

Image {
  mipmap: true

  MouseArea {
    id: image_mouse_area
    anchors.fill: parent
    hoverEnabled: true

    RowLayout {
      anchors.fill: parent

      Button {
        Layout.fillHeight: true
        Layout.preferredWidth: 60
        text: "<"
        flat: true
        font.bold: true
        font.pointSize: 32
        visible: image_mouse_area.containsMouse
        enabled: game_screenshots_swipe_view.currentIndex > 0
        onClicked: game_screenshots_swipe_view.decrementCurrentIndex()
        background: Rectangle {
          gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: -3.0; color: "black" }
            GradientStop { position: 1.0; color: "transparent" }
          }
        }
      }

      Item {Layout.fillWidth: true}

      Button {
        Layout.fillHeight: true
        Layout.preferredWidth: 60
        text: ">"
        flat: true
        font.bold: true
        font.pointSize: 32
        visible: image_mouse_area.containsMouse
        enabled: game_screenshots_swipe_view.currentIndex < game_screenshots_swipe_view.count - 1
        onClicked: game_screenshots_swipe_view.incrementCurrentIndex()
        background: Rectangle {
          gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "transparent" }
            GradientStop { position: 4.0; color: "black" }
          }
        }
      }
    }
  }
}