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

    ColumnLayout {
      Text {
        text: ""
      }
    }
  }
}