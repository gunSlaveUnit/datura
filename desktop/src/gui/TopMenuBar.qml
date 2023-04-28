import QtQuick 2.15
import QtQuick.Controls 2.15

MenuBar {
  background: Rectangle {
    color: "transparent"
  }

  Menu {
    title: qsTr('Foggie')

    Action {
      text: qsTr("Store")
      onTriggered: {
        game_list_model.load_store()
        storeStackLayout.currentIndex = storeStackLayout.storeGamesIndex
      }
    }

    Action {
      text: qsTr("Library")
    }

    Action {
      text: qsTr("Workroom")
      onTriggered: storeStackLayout.checkCompanyRegistration()
    }
  }

  Menu {
    title: qsTr('Nickname')
    Action {text: qsTr("Profile")}
    Action {text: qsTr("Wallet")}
    Action {text: qsTr("Cart")}
    Action {text: qsTr("Settings")}
    Action {
      text: qsTr("Logout")
      onTriggered: auth_logic.sign_out()
    }
  }
}