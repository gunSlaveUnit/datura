import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt.labs.platform

Window {
  id: window
  width: 1000
  height: 500
  visible: true
  title: qsTr("foggie")
  color: "#212834"

  property int defaultMargin: 8
  property int textFieldWidth: 240
}