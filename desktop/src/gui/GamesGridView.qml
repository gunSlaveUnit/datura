import QtQuick 2.15
import QtQuick.Layouts 2.15

GridView {
  id: games_grid_view

  function cellOnClickHandler() {}

  property int capsuleImageWidth: 12 * 10
  property int capsuleImageHeight: 17 * 10

  Layout.preferredWidth: window.width
  Layout.preferredHeight: window.height

  cellWidth: capsuleImageWidth + defaultMargin * 2
  cellHeight: capsuleImageHeight + defaultMargin * 2.5

  clip: true

  model: game_list_model

  delegate: Rectangle {
    width: games_grid_view.cellWidth
    height: games_grid_view.cellHeight
    color: "transparent"
    radius: defaultMargin / 2

    Image {
      anchors.centerIn: parent
      width: games_grid_view.capsuleImageWidth
      height: games_grid_view.capsuleImageHeight
      source: `http://localhost:8000/games/${id}/assets/capsule/`
      mipmap: true
    }

    MouseArea {
      id: cell_mouse_area
      anchors.fill: parent
      hoverEnabled: true
      onEntered: parent.color = "#36373a"
      onExited: parent.color = "transparent"
      onClicked: games_grid_view.cellOnClickHandler
    }
  }
}