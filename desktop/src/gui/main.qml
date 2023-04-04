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
				text: qsTr("EMAIL")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: 200
			}

			Text {
				text: qsTr("PASSWORD")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: 200
				echoMode: TextInput.Password
			}

			Button {
				Layout.alignment: Qt.AlignHCenter
				text: qsTr("Sign in")
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
				Layout.preferredWidth: 200
			}

			Text {
				text: qsTr("ACCOUNT NAME")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: 200
			}

			Text {
				text: qsTr("PASSWORD")
				color: "white"
			}

			TextField {
				Layout.preferredWidth: 200
				echoMode: TextInput.Password
			}

			Button {
				Layout.alignment: Qt.AlignHCenter
				text: qsTr("Sign up")
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