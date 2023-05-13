import QtQuick 2.15
import QtQuick.Layouts 2.15

Rectangle {
  property string content: ""
  property double amount: 0.0

  width: layoutWidth / 2
  height: 56
  radius: defaultMargin / 2
  color: "#586776"

  RowLayout {
    visible: store_detailed_logic.location === 0
    anchors.fill: parent
    anchors.margins: defaultMargin

    Text {
      textFormat: TextEdit.MarkdownText
      color: "#ddd"
      text: "## " + content
    }

    Item {Layout.fillWidth: true}

    BuyButton {
      text: "Пополнить"
      function handler() {
        walletLogic.amount = parent.parent.amount
      }
    }
  }
}