import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Button {
    property string text_color: "#ededed"

    Material.theme: Material.Dark
    Material.foreground: text_color
    flat: true
    font.bold: true
    font.pointSize: 14
}