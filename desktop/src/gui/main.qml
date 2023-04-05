import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

Window {
  id: window
  width: 1000
  height: 500
  visible: true
  title: qsTr("foggie")
  color: "#0c0c0c"

  property int defaultMargin: 8
  property int textFieldWidth: 240

  minimumWidth: signUpForm.implicitWidth + 2 * defaultMargin
  minimumHeight: signUpForm.implicitHeight + 2 * defaultMargin

	StackLayout {
		id: authStackLayout

		anchors.fill: parent

    property int signInFormIndex: 0
    property int signUpFormIndex: 1

		ColumnLayout {
			id: signInForm
			anchors.margins: 8
			anchors.centerIn: parent

			Text {
				text: qsTr("ACCOUNT NAME")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: textFieldWidth
				text: auth_logic.account_name
        onTextChanged: auth_logic.account_name = text
			}

			Text {
				text: qsTr("PASSWORD")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: textFieldWidth
				echoMode: TextInput.Password
				text: auth_logic.password
        onTextChanged: auth_logic.password = text
			}

			Button {
				Layout.alignment: Qt.AlignHCenter
				text: qsTr("Sign in")
				onClicked: auth_logic.sign_in()
			}

			RowLayout {
				Layout.alignment: Qt.AlignHCenter

				Text {
          text: qsTr("Need an account?")
          color: "white"
        }

        Text {
          text: qsTr("Sign up")
          font.underline: true
          font.bold: true
          color: "white"

          MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            hoverEnabled: true
            onClicked: authStackLayout.currentIndex = authStackLayout.signUpFormIndex
          }
        }
			}
		}

		ColumnLayout {
			id: signUpForm
			anchors.margins: 8
			anchors.centerIn: parent

			Text {
				text: qsTr("EMAIL")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: textFieldWidth
				text: auth_logic.email
        onTextChanged: auth_logic.email = text
			}

			Text {
				text: qsTr("ACCOUNT NAME")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: textFieldWidth
				text: auth_logic.account_name
        onTextChanged: auth_logic.account_name = text
			}

			Text {
				text: qsTr("PASSWORD")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: textFieldWidth
				echoMode: TextInput.Password
				text: auth_logic.password
        onTextChanged: auth_logic.password = text
			}

			Button {
				Layout.alignment: Qt.AlignHCenter
				text: qsTr("Sign up")
				onClicked: auth_logic.sign_up()
			}

			RowLayout {
				Layout.alignment: Qt.AlignHCenter

				Text {
          text: qsTr("Already have an account?")
          color: "white"
        }

        Text {
          text: qsTr("Sign in")
          font.underline: true
          font.bold: true
          color: "white"

          MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            hoverEnabled: true
            onClicked: authStackLayout.currentIndex = authStackLayout.signInFormIndex
          }
        }
			}
		}
	}
}