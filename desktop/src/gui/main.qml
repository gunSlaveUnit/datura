import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

Window {
  id: mainWindow
  width: 1000
  height: 500
  title: qsTr("foogie")
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

      Button {text: qsTr("Test 1")}
      Button {text: qsTr("Test 2")}
      Button {text: qsTr("Test 3")}
      Button {text: qsTr("Test 4")}
      Button {text: qsTr("Test 5")}
      Button {text: qsTr("Test 6")}
      Button {text: qsTr("Test 7")}
      Button {text: qsTr("Test 8")}
      Button {text: qsTr("Test 9")}
      Button {text: qsTr("Test 10")}
      Button {text: qsTr("Test 11")}
      Button {text: qsTr("Test 12")}
      Button {text: qsTr("Test 13")}
      Button {text: qsTr("Test 14")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
      Button {text: qsTr("Test 15")}
    }
  }
}