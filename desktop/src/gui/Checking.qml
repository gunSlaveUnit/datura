import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

CheckBox {
    property string window_theme_color: "#0053A6"

    font.pointSize: 12
    font.bold: true

    Material.theme: Material.Dark
    Material.accent: window_theme_color
}