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
  title: windowTitle
  color: backgroundWindowColor

  property string backgroundWindowColor: "#212834"
  property string highlightedTextColor: "#0079F2"
  property string windowTitle: qsTr("foggie")
  property int defaultMargin: 8

  StackLayout {
    id: mainStackLayout

    anchors.fill: parent

    property int authorizationSectionIndex: 0
    property int storeSectionIndex: 1

    StackLayout {
			id: authStackLayout

			anchors.fill: parent
			anchors.margins: 8

			Connections {
				target: auth_logic

				function onRegistered() {
					mainStackLayout.currentIndex = mainStackLayout.storeSectionIndex
				}

		    function onLogin() {
					mainStackLayout.currentIndex = mainStackLayout.storeSectionIndex
		    }
			}

	    property int signInFormIndex: 0
	    property int signUpFormIndex: 1

	    ColumnLayout {
				id: signInForm
				anchors.centerIn: parent

				FormInputLabel {
				  text: qsTr("ACCOUNT NAME")
				  color: highlightedTextColor
				}
				FormInput {
				  id: signInAccountNameInput
          focus: true
          text: auth_logic.account_name
	        onTextChanged: auth_logic.account_name = text
        }

				Indent {}

				FormInputLabel {text: qsTr("PASSWORD")}
				FormInput {
				  echoMode: TextInput.Password
				  text: auth_logic.password
	        onTextChanged: auth_logic.password = text
				}

        Indent {}

				ActionButton {
					Layout.alignment: Qt.AlignHCenter
					text: qsTr("Sign in")

					function handler() {
					  auth_logic.sign_in()
					}
				}

				Indent {}

				RowLayout {
					Layout.alignment: Qt.AlignHCenter

					Span {text: qsTr("Need an account?")}

          Link {
            message: qsTr("Sign up")

            function handler() {
              auth_logic.reset()
              signUpEmailInput.focus = true
              authStackLayout.currentIndex = authStackLayout.signUpFormIndex
            }
          }
        }
      }

      ColumnLayout {
				id: signUpForm
				anchors.centerIn: parent

        FormInputLabel {text: qsTr("EMAIL")}
				FormInput {
				  id: signUpEmailInput
				  text: auth_logic.email
	        onTextChanged: auth_logic.email = text
				}

				Indent {}

				FormInputLabel {text: qsTr("ACCOUNT NAME")}
				FormInput {
				  text: auth_logic.account_name
	        onTextChanged: auth_logic.account_name = text
				}

				Indent {}

				FormInputLabel {text: qsTr("PASSWORD")}
				FormInput {
				  echoMode: TextInput.Password
				  text: auth_logic.password
	        onTextChanged: auth_logic.password = text
				}

        Indent {}

				ActionButton {
					Layout.alignment: Qt.AlignHCenter
					text: qsTr("Sign up")

					function handler() {
					  auth_logic.sign_up()
					}
				}

				Indent {}

				RowLayout {
					Layout.alignment: Qt.AlignHCenter

					Span {text: qsTr("Already have an account?")}

          Link {
            message: qsTr("Sign in")

            function handler() {
              auth_logic.reset()
              signInAccountNameInput.focus = true
              authStackLayout.currentIndex = authStackLayout.signInFormIndex
            }
          }
        }
      }
    }

    StackLayout {
      id: storeStackLayout

      property int storeGamesIndex: 0

      Connections {
        target: auth_logic

        function onRegistered() {
          game_list_model.load_store()
        }

        function onLogin() {
          game_list_model.load_store()
        }

        function onLogout() {
          authStackLayout.currentIndex = authStackLayout.signInFormIndex
          mainStackLayout.currentIndex = mainStackLayout.authorizationSectionIndex
          storeStackLayout.currentIndex = storeStackLayout.storeGamesIndex
        }
      }

      GridView {
        id: storeGamesGridView

        property int capsuleImageWidth: 12 * 10
        property int capsuleImageHeight: 17 * 10

        Layout.preferredWidth: window.width
        Layout.preferredHeight: window.height

        cellWidth: capsuleImageWidth + defaultMargin * 2
        cellHeight: capsuleImageHeight + defaultMargin * 2.5

        clip: true

        model: game_list_model

        delegate: Rectangle {
          width: storeGamesGridView.cellWidth
          height: storeGamesGridView.cellHeight
          color: "transparent"
          radius: defaultMargin / 2

          Image {
            anchors.centerIn: parent
            width: storeGamesGridView.capsuleImageWidth
            height: storeGamesGridView.capsuleImageHeight
            source: `http://127.0.0.1:8000/api/v1/games/${id}/capsule/`
            mipmap: true
          }

          MouseArea {
            id: cell_mouse_area
            anchors.fill: parent
            hoverEnabled: true
            onEntered: parent.color = "#36373a"
            onExited: parent.color = "transparent"
            onClicked: {}
          }
        }
      }
    }
  }
}