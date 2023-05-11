import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Switch {
  property string window_theme_color: "#0079F2"

  font.pointSize: 14
  font.bold: true

  Material.theme: Material.Dark
  Material.accent: window_theme_color
}