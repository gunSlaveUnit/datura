import QtQuick 2.15
import QtQuick.Controls 2.15

Text {
  property string content: ""

  textFormat: TextEdit.MarkdownText
  color: "#ddd"
  text: "### " + content
}