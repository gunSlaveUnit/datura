import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt.labs.platform as Platform

ApplicationWindow {
  id: window
  property int layoutWidth: 960
  property int layoutHeight: 500
  minimumWidth: layoutWidth + 2 * defaultMargin
  minimumHeight: layoutHeight

  visible: true
  title: windowTitle
  color: backgroundWindowColor

  property string backgroundWindowColor: "#212834"
  property string highlightedTextColor: "#0079F2"
  property string windowTitle: qsTr("foggie")
  property int defaultMargin: 8

  menuBar: TopMenuBar {
    id: menu
    visible: false
  }

  StackLayout {
    id: mainStackLayout

    anchors.fill: parent

    property int authorizationSectionIndex: 0
    property int storeSectionIndex: 1

    StackLayout {
			id: authStackLayout

      anchors.fill: parent

			Connections {
				target: auth_logic

				function onRegistered() {
					mainStackLayout.currentIndex = mainStackLayout.storeSectionIndex
					menu.visible = true
				}

		    function onLogin() {
					mainStackLayout.currentIndex = mainStackLayout.storeSectionIndex
					menu.visible = true
		    }
			}

	    property int signInFormIndex: 0
	    property int signUpFormIndex: 1

	    Item {
	      anchors.margins: defaultMargin
	      Layout.preferredWidth: window.width
	      Layout.preferredHeight: window.height

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
	    }

      Item {
        anchors.margins: defaultMargin
	      Layout.preferredWidth: window.width
	      Layout.preferredHeight: window.height

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
    }

    StackLayout {
      id: storeStackLayout

      property int storeGamesIndex: 0
      property int storeDetailedGameIndex: storeGamesIndex + 1
      property int workshopRegisterCompanyInfoIndex: storeDetailedGameIndex + 1
      property int workshopRegisterPaymentInfoIndex: workshopRegisterCompanyInfoIndex + 1
      property int workshopAppsListIndex: workshopRegisterPaymentInfoIndex + 1
      property int workshopAppControlIndex: workshopAppsListIndex + 1

      function checkCompanyRegistration() {
        company_logic.check()
      }

      Connections {
        target: company_logic

        function onNotRegistered() {
          storeStackLayout.currentIndex = storeStackLayout.workshopRegisterCompanyInfoIndex
        }

        function onRegistered() {
          game_list_model.load_personal()
          storeStackLayout.currentIndex = storeStackLayout.workshopAppsListIndex
        }
      }

      Connections {
        target: auth_logic

        function onRegistered() {
          game_list_model.load_store()
        }

        function onLogin() {
          game_list_model.load_store()
        }

        function onLogout() {
          menu.visible = false

          authStackLayout.currentIndex = authStackLayout.signInFormIndex
          mainStackLayout.currentIndex = mainStackLayout.authorizationSectionIndex
          storeStackLayout.currentIndex = storeStackLayout.storeGamesIndex
        }
      }

      GridView {
        id: storeGamesGridView

        anchors.fill: parent
        anchors.margins: defaultMargin

        boundsBehavior: Flickable.StopAtBounds

        property int capsuleImageWidth: 12 * 10
        property int capsuleImageHeight: capsuleImageWidth * 16 / 9

        property int idealWidth: capsuleImageWidth + defaultMargin * 2
        property int itemsPerRow: storeGamesGridView.width / idealWidth
        property double additionalCellWidth: (storeGamesGridView.width - itemsPerRow * idealWidth) / itemsPerRow
        cellWidth: idealWidth + additionalCellWidth
        cellHeight: capsuleImageHeight + defaultMargin * 2

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
            cursorShape: Qt.PointingHandCursor
            hoverEnabled: true
            onEntered: parent.color = "#36373a"
            onExited: parent.color = "transparent"
            onClicked: {
              store_detailed_logic.load(id)
              storeStackLayout.currentIndex = storeStackLayout.storeDetailedGameIndex
            }
          }
        }
      }

      Scroll {
        contentHeight: storeGameDetailedPage.height

        Item {
          width: parent.width * 0.8
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: storeGameDetailedPage

            Link {
              message: qsTr("To the store")

              function handler() {
                game_list_model.load_store()
                storeStackLayout.currentIndex = storeStackLayout.storeGamesIndex
              }
            }
          }
        }
      }

      Scroll {
        contentHeight: companyInfoForm.height + 2 * defaultMargin

        Item {
          width: layoutWidth
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: companyInfoForm

            Indent {}

            FormInputLabel {
              text: qsTr("Juridical name")
            }
            FormInput {
              id: juridicalNameInput
              focus: true
              text: company_logic.juridical_name
              onTextChanged: company_logic.juridical_name = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Company form")
            }
            FormInput {
              text: company_logic.company_form
              onTextChanged: company_logic.company_form = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Street, house and apartment/office number")
            }
            FormInput {
              text: company_logic.street_house_apartment
              onTextChanged: company_logic.street_house_apartment = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("City")
            }
            FormInput {
              text: company_logic.city
              onTextChanged: company_logic.city = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Region")
            }
            FormInput {
              text: company_logic.region
              onTextChanged: company_logic.region = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Country")
            }
            FormInput {
              text: company_logic.country
              onTextChanged: company_logic.country = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Postal code")
            }
            FormInput {
              text: company_logic.postal_code
              onTextChanged: company_logic.postal_code = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Notification email")
            }
            FormInput {
              text: company_logic.notification_email
              onTextChanged: company_logic.notification_email = text
            }

            Indent {}

            NeutralButton {
              text: qsTr("Next")
              function handler() {
                bicInput.focus = true
                storeStackLayout.currentIndex = storeStackLayout.workshopRegisterPaymentInfoIndex
              }
            }
          }
        }
      }

      Scroll {
        contentHeight: companyPayInfoForm.height

        Item {
          width: parent.width * 0.8
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: companyPayInfoForm

            Indent {}

            Link {
              message: qsTr("To company information")

              function handler() {
                juridicalNameInput.focus = true
                storeStackLayout.currentIndex = storeStackLayout.workshopRegisterCompanyInfoIndex
              }
            }

            Indent {}

            FormInputLabel {
              text: qsTr("BIC")
            }
            FormInput {
              id: bicInput
              focus: true
              text: company_logic.bic
              onTextChanged: company_logic.bic = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Bank address")
            }
            FormInput {
              text: company_logic.bank_address
              onTextChanged: company_logic.bank_address = text
            }

            Indent {}

            FormInputLabel {
              text: qsTr("Bank account number")
            }
            FormInput {
              text: company_logic.bank_account_number
              onTextChanged: company_logic.bank_account_number = text
            }

            Indent {}

            ActionButton {
              text: qsTr("Finish")
              function handler() {
                company_logic.new()
              }
            }

            Indent {}
          }
        }
      }

      Scroll {
        contentHeight: releasesAppsList.height

        Item {
          width: parent.width * 0.8
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: releasesAppsList

            Connections {
              target: app_logic

              function onDrafted() {
                storeStackLayout.currentIndex = storeStackLayout.workshopAppControlIndex
              }
            }

            ActionButton {
              text: qsTr("Draft new")
              function handler() {
                app_logic.draft_new()
              }
              visible: company_logic.is_drafted_new_button_enabled
            }

            ListView {
              Layout.fillHeight: true

              model: game_list_model

              delegate: RowLayout {
                Text {
                  text: title
                  color: "white"
                  font.underline: true

                  MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true
                    onClicked: {
                      app_logic.map(id)
                      storeStackLayout.currentIndex = storeStackLayout.workshopAppControlIndex
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}