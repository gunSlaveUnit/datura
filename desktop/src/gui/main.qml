import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 2.15
import QtQuick.Controls 2.15
import Qt.labs.platform as Platform

Window {
  property int defaultMargin: 8
  property string backgroundWindowColor: "#0E151E"
  property string highlightedTextColor: "#0079F2"

  property int layoutWidth: 984

  title: qsTr("foggie")
  width: 1000
  height: 500
  visible: true
  color: backgroundWindowColor

  StackLayout {
    id: mainStack

    property int authorizationIndex: 0
    property int storeIndex: 1

    anchors.fill: parent

    StackLayout {
			id: authStack

			property int signInFormIndex: 0
	    property int signUpFormIndex: 1

	    anchors.fill: parent

			Connections {
				target: auth_logic

				function onRegistered() {
					mainStack.currentIndex = mainStack.storeIndex
				}

		    function onLogin() {
					mainStack.currentIndex = mainStack.storeIndex
		    }
			}

      ColumnLayout {
        id: signInForm

        anchors.centerIn: parent

        FormInputLabel {
          color: highlightedTextColor
          text: qsTr("ACCOUNT NAME")
        }
        FormInput {
          id: signInAccountNameInput
          Layout.bottomMargin: defaultMargin
          focus: true
          text: auth_logic.account_name
          onTextChanged: auth_logic.account_name = text
        }

        FormInputLabel {text: qsTr("PASSWORD")}
        FormInput {
          Layout.bottomMargin: defaultMargin
          echoMode: TextInput.Password
          text: auth_logic.password
          onTextChanged: auth_logic.password = text
        }

        ActionButton {
          Layout.alignment: Qt.AlignHCenter
          Layout.bottomMargin: defaultMargin
          text: qsTr("Sign in")
          function handler() {
            auth_logic.sign_in()
          }
        }

        RowLayout {
          Layout.alignment: Qt.AlignHCenter

          Span {text: qsTr("Need an account?")}

          Link {
            message: qsTr("Sign up")

            function handler() {
              auth_logic.reset()
              signUpEmailInput.focus = true
              authStack.currentIndex = authStack.signUpFormIndex
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
          Layout.bottomMargin: defaultMargin
          text: auth_logic.email
          onTextChanged: auth_logic.email = text
        }

        FormInputLabel {text: qsTr("ACCOUNT NAME")}
        FormInput {
          Layout.bottomMargin: defaultMargin
          text: auth_logic.account_name
          onTextChanged: auth_logic.account_name = text
        }

        FormInputLabel {text: qsTr("PASSWORD")}
        FormInput {
          Layout.bottomMargin: defaultMargin
          echoMode: TextInput.Password
          text: auth_logic.password
          onTextChanged: auth_logic.password = text
        }

        ActionButton {
          Layout.alignment: Qt.AlignHCenter
          Layout.bottomMargin: defaultMargin
          text: qsTr("Sign up")

          function handler() {
            auth_logic.sign_up()
          }
        }

        RowLayout {
          Layout.alignment: Qt.AlignHCenter

          Span {text: qsTr("Already have an account?")}

          Link {
            message: qsTr("Sign in")

            function handler() {
              auth_logic.reset()
              signInAccountNameInput.focus = true
              authStack.currentIndex = authStack.signInFormIndex
            }
          }
        }
      }
    }

    ColumnLayout {
      RowLayout {
        Layout.leftMargin: defaultMargin
        Layout.rightMargin: defaultMargin

        MenuButton {
          text: qsTr("Store")
          onClicked: {
            game_list_model.load_store()
            storeStack.currentIndex = storeStack.storeIndex
          }
        }

        MenuButton {
          text: qsTr("Library")
          onClicked: {
          }
        }

        MenuButton {
          text: qsTr("Workshop")
          onClicked: {
            storeStack.checkCompanyRegistration()
          }
        }

        Item {Layout.fillWidth: true}

        Rectangle {
		      Layout.preferredWidth: 150
		      Layout.preferredHeight: 28
		      color: "#274257"

		      RowLayout {
		        anchors.fill: parent

		        Image {
              id: avatar
              Layout.preferredHeight: parent.height
              Layout.preferredWidth: height
              mipmap: true
              source: `http://127.0.0.1:8000/api/v1/users/${current_user_logic.id}/avatar/`
            }

            Span {
              text: current_user_logic.displayed_name
              color: "#64BCEF"
            }

            Span {
              text: wallet_logic.balance + "$"
            }
		      }

		      Menu {
			      id: userProfileMenu

			      width: parent.width

			      y: parent.height

						MenuItem {
			        text: qsTr("Profile")
			      }

			      MenuItem {
			        text: qsTr("Cart")
			        onTriggered: {
			          game_list_model.load_cart()
                storeStack.currentIndex = storeStack.cartIndex
              }
			      }

						MenuItem {
			        text: qsTr("Wallet")
			        onTriggered: storeStack.currentIndex = storeStack.walletIndex
			      }

						MenuItem {
			        text: qsTr("Settings")
			      }

			      MenuItem {
			        text: qsTr("Logout")
			        onTriggered: auth_logic.sign_out()
			      }
			    }

		      MouseArea {
			      anchors.fill: parent
			      hoverEnabled: true
			      onEntered: parent.color = "#375D77"
			      onExited: parent.color = "#274257"
			      onClicked: userProfileMenu.open()
			    }
        }
      }

      StackLayout {
        id: storeStack

        property int storeIndex: 0
        property int storeDetailedIndex: storeIndex + 1
        property int libraryIndex: storeDetailedIndex + 1
        property int libraryDetailedIndex: libraryIndex + 1
        property int profileIndex: libraryDetailedIndex + 1
        property int cartIndex: profileIndex + 1
        property int walletIndex: cartIndex + 1
        property int walletTopUpIndex: walletIndex + 1
        property int workshopIntroductionIndex: walletTopUpIndex + 1
        property int workshopRegisterCompanyInfoIndex: workshopIntroductionIndex + 1
        property int workshopRegisterPaymentInfoIndex: workshopRegisterCompanyInfoIndex + 1
        property int workshopAppsListIndex: workshopRegisterPaymentInfoIndex + 1
        property int workshopAppControlIndex: workshopAppsListIndex + 1

        function checkCompanyRegistration() { company_logic.check(current_user_logic.id) }

        Connections {
          target: company_logic

          function onNotRegistered() {
            storeStack.currentIndex = storeStack.workshopIntroductionIndex
          }

          function onRegistered() {
            game_list_model.load_personal(current_user_logic.id)
            storeStack.currentIndex = storeStack.workshopAppsListIndex
          }
        }

        Connections {
          target: auth_logic

          function onRegistered() {
            current_user_logic.load()
            wallet_logic.load(current_user_logic.id)
            game_list_model.load_store()
          }

          function onLogin() {
            current_user_logic.load()
            wallet_logic.load(current_user_logic.id)
            game_list_model.load_store()
          }

          function onLogout() {
            authStack.currentIndex = authStack.signInFormIndex
            mainStack.currentIndex = mainStack.authorizationIndex
            storeStack.currentIndex = storeStack.storeIndex
          }
        }

        ListView {
          model: game_list_model
          spacing: defaultMargin
          boundsBehavior: Flickable.StopAtBounds

          delegate: Rectangle {
            anchors.horizontalCenter: parent.horizontalCenter
            color: "transparent"
            width: layoutWidth
            height: 180
            radius: defaultMargin / 2

            RowLayout {
              anchors.fill: parent
              anchors.margins: defaultMargin

              Image {
                Layout.preferredWidth: height * 16 / 9
                Layout.preferredHeight: parent.height
                source: `http://127.0.0.1:8000/api/v1/games/${id}/header/`
                mipmap: true
              }

              ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Layout.alignment: Qt.AlignTop

                Link {
                  Layout.alignment: Qt.AlignTop
                  text: title
                  font.pointSize: 26

                  function handler() {
                    store_detailed_logic.load(id)
                    storeStack.currentIndex = storeStack.storeDetailedIndex
                  }
                }

                Span {
                  text: release_date
                }

                Span {
                  text: short_description
                }
              }

              Item {Layout.fillWidth: true}
            }
          }
        }

        Scroll {
          contentHeight: storeGameDetailedPage.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: storeGameDetailedPage

              Link {
                message: qsTr("To the store")

                function handler() {
                  game_list_model.load_store()
                  storeStack.currentIndex = storeStack.storeIndex
                }
              }

              SwipeView {
                id: game_screenshots_swipe_view

                Layout.preferredWidth: 400
                Layout.preferredHeight: width * 9 / 16

                clip: true

                Repeater {
                  model: 6

                  Image {
                    source: "../../resources/images/16x9_placeholder.jpg"
                    mipmap: true

                    MouseArea {
                      id: image_mouse_area
                      anchors.fill: parent
                      hoverEnabled: true

                      RowLayout {
                        anchors.fill: parent

                        Button {
                          Layout.fillHeight: true
                          Layout.preferredWidth: 30
                          text: "<"
                          flat: true
                          font.bold: true
                          font.pointSize: 16
                          visible: image_mouse_area.containsMouse
                          enabled: game_screenshots_swipe_view.currentIndex > 0
                          onClicked: game_screenshots_swipe_view.decrementCurrentIndex()
                          background: Rectangle {
                            gradient: Gradient {
                              orientation: Gradient.Horizontal
                              GradientStop { position: -1.0; color: "black" }
                              GradientStop { position: 1.0; color: "transparent" }
                            }
                          }
                        }

                        Item {Layout.fillWidth: true}

                        Button {
                          Layout.fillHeight: true
                          Layout.preferredWidth: 30
                          text: ">"
                          flat: true
                          font.bold: true
                          font.pointSize: 16
                          visible: image_mouse_area.containsMouse
                          enabled: game_screenshots_swipe_view.currentIndex < game_screenshots_swipe_view.count - 1
                          onClicked: game_screenshots_swipe_view.incrementCurrentIndex()
                          background: Rectangle {
                            gradient: Gradient {
                              orientation: Gradient.Horizontal
                              GradientStop { position: 0.0; color: "transparent" }
                              GradientStop { position: 2.0; color: "black" }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }

              BuyButton {
                text: "Buy"
                visible: store_detailed_logic.location === 0
              }

              Text {
                text: "Already in library"
                color: "white"
                visible: store_detailed_logic.location === 1
              }

              Text {
                text: "Already in cart"
                color: "white"
                visible: store_detailed_logic.location === 2
              }
            }
          }
        }

        GridView {
          id: storeGamesGridView

          anchors.fill: parent
          anchors.margins: defaultMargin

          boundsBehavior: Flickable.StopAtBounds

          property int capsuleImageWidth: 12 * 10
          property int capsuleImageHeight: capsuleImageWidth * 16 / 10

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
                storeStack.currentIndex = storeStack.storeDetailedIndex
              }
            }
          }
        }

        ColumnLayout {}

        Scroll {
          contentHeight: libraryDetailedPage.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: libraryDetailedPage

              Text {
                text: library_detailed_logic.game_title
                color: "white"
              }

              Text {
                text: library_detailed_logic.last_launched
                color: "white"
              }

              Text {
                visible: library_detailed_logic.play_time !== "0"
                text: library_detailed_logic.play_time
                color: "white"
              }

              FolderDialog {
                id: installation_path_dialog

                onAccepted: {
                  library_detailed_logic.installation_path = folder
                  library_detailed_logic.download()
                }
              }

              Button {
                text: library_detailed_logic.is_game_installed ? "Launch" : "Install"
                onClicked: library_detailed_logic.is_game_installed ? library_detailed_logic.run() : installation_path_dialog.open()
              }
            }
          }
        }

        Scroll {
          contentHeight: cartPage.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: cartPage

              RowLayout {
                Text {
                  color: "white"
                  text: "Total Price: " + game_list_model.total_cost
                }

                BuyButton {
                  text: "Buy"
                  function handler() {

                  }
                }
              }

              ListView {
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
                        store_detailed_logic.load(id)
                        storeStack.currentIndex = storeStack.storeDetailedIndex
                      }
                    }
                  }

                  Checking {
                    checked: is_checked
                    onCheckedChanged: {
                      game_list_model.change_checked_state(index)
                      game_list_model.recount_total_cost()
                    }
                  }
                }
              }
            }
          }
        }

        Scroll {
          contentHeight: walletPage.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: walletPage

              Header {
                text: "# Your balance is: " + wallet_logic.balance + "$"
              }

              BuyButton {
                text: "Top up"
                function handler() {
                  storeStack.currentIndex = storeStack.walletTopUpIndex
                }
              }
            }
          }
        }

        Scroll {
          contentHeight: walletTopUpPage.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            RowLayout {
              id: walletTopUpPage
              Layout.fillWidth: true

              ColumnLayout {
                Link {
                  message: qsTr("To wallet")

                  function handler() {
                    storeStack.currentIndex = storeStack.walletIndex
                  }
                }

                Span {
                  text: qsTr("Choose a deposit method")
                }

                Combo {
                  implicitWidth: 140

                  model: [
                    "PayPal",
                    "Visa",
                    "MasterCard",
                    "American Express",
                    "Мир",
                    "Яндекс.Деньги",
                    "QIWI Wallet",
                    "Mobile payments",
                  ]
                }

                Indent {}

                Span {
                  text: qsTr("Select amount")
                }

                Combo {
                  id: paymentCost
                  implicitWidth: 140

                  model: [
                    "5",
                    "10",
                    "25",
                    "50",
                    "100",
                  ]
                  onCurrentTextChanged: {
                    text = currentText + "$"
                  }
                }

                ActionButton {
                  text: qsTr("Pay")
                  function handler() {
                    var selectedValue = paymentCost.currentText
                    selectedValue = selectedValue.replace("$", "")
                    wallet_logic.top_up(current_user_logic.id, selectedValue)
                  }
                }
              }
            }
          }
        }

        Scroll {
          contentHeight: introduction.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: introduction

              QtObject{
                id: introductionContent
                property string text: "# Foggie Workshop
Are you a developer and want to use our platform to distribute your games and software? This is great, let's get started.

&nbsp;
## What to expect
---
General procedure for publishing products:
1. Fill in electronic documents:
    * Information about the legal entity
    * Banking / tax information
2. Once you have access to the Workshop, start preparing your product for release. You will need to create a store page, upload product builds, and enter your desired price.
3. Prior to the final launch of your build of the game and the store page, we will run a test run of the game and check the page to make sure there are no errors or malicious elements. The verification usually takes 1 to 5 days.

&nbsp;
## Information to keep handy:
---
* Legal details and name

Accurate legal information about the person or company signing the agreement so we understand who you are and who you represent. This is information about your company.
* Payment Information

Accurate banking information on where to transfer the proceeds from the sales of your application: bank code, bank account number and bank address.

&nbsp;
## Rules and regulations
---
What should not be distributed using our platform:
* Advocacy of hatred, violence or discrimination against groups of people based on ethnicity, religion, gender, age, disability or sexual orientation.
* Images of a sexual nature with real people.
* Adult content that is not labeled as such and contains no age rating information.
* Slanderous statements or statements that offend honor and dignity. Content to which you do not own the rights.
* Content to which you do not own the rights.
* Content that violates the laws of the countries in which it will be distributed.
* Content that is blatantly offensive or intentionally shocks or disgusts the public.
* Content that is in any way related to the exploitation of minors.
* Applications that change the user's computer in ways they do not expect or that cause harm, such as viruses or malware.
* Applications that attempt to fraudulently obtain sensitive information (such as login details) or financial data (such as credit card information).
* Video content that is not directly related to the product released on platform.
* Non-interactive panoramic virtual reality videos.
* Applications created using blockchain technology that issue or exchange cryptocurrencies or NFTs (non-fungible tokens).

Allowed types of content

First of all, we accept games. Non-gaming software may be accepted if it falls into one of the following categories:
* animation and modeling;
* work with sound and video;
* design and illustration;
* photo processing;
* education and training;
* finance and accounting;
* tools for players;

&nbsp;
## Let's get started
---
Click the Continue button to proceed to enter your legal name and contact information.
"}
              Text{
                Layout.preferredWidth: layoutWidth - 2 * defaultMargin
                textFormat: TextEdit.MarkdownText
                text: introductionContent.text
                color: "#ddd"
                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
              }

              NeutralButton {
                text: qsTr("Continue")
                function handler() {
                  bicInput.focus = true
                  storeStack.currentIndex = storeStack.workshopRegisterCompanyInfoIndex
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

              Link {
                message: qsTr("To introduction")

                function handler() {
                  juridicalNameInput.focus = true
                  storeStack.currentIndex = storeStack.workshopIntroductionIndex
                }
              }

              Indent {}

              Rectangle {
                width: layoutWidth - 2 * defaultMargin
                height: 230
                radius: defaultMargin
                border.color: "orange"
                border.width: 1
                color: "transparent"

                Item {
                  width: parent.width - 2 * defaultMargin
                  anchors.horizontalCenter: parent.horizontalCenter

                  ColumnLayout {
                    id: legalNameExplanationLayout

                    QtObject{
                      id: legalNameContent
                      property string text: "<h1 style=\"color:white\">Legal name</h1>

The organization whose name you enter below must be the legal entity that will sign the required license agreements. The company name entered here must match the name on official bank documents and documents provided to the tax office, or foreign tax documents, if any. If you later add bank account information, you will need to re-enter that nameas the account holder and legal entity with the appropriate tax identification number.

If you do not have a company name and are the sole owner of the content you wish to post, please enter your full name and mailing address in the \"Legal Name\" and \"Street, House and Apartment/Office Number\" fields. If you co-own the game along with other people, you will need to register a legal entity that will own the content and accept payments for it.

The legal name specified here is used internally by the system. If you have a commercial or informal name that you want to use in your store, you can specify it separately when you create your store page.
"}
                    Text {
                      Layout.preferredWidth: layoutWidth - 3 * defaultMargin
                      textFormat: TextEdit.MarkdownText
                      text: legalNameContent.text
                      color: "orange"
                      wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    }

                    FormInputLabel {
                      text: qsTr("Juridical name")
                    }
                    FormInput {
                      id: juridicalNameInput
                      focus: true
                      text: company_logic.juridical_name
                      onTextChanged: company_logic.juridical_name = text
                    }
                  }
                }
              }

              Indent {}

              Rectangle {
                width: layoutWidth - 2 * defaultMargin
                height: 138
                radius: defaultMargin
                border.color: "orange"
                border.width: 1
                color: "transparent"

                Item {
                  width: parent.width - 2 * defaultMargin
                  anchors.horizontalCenter: parent.horizontalCenter

                  ColumnLayout {
                    id: companyFormExplanationLayout

                    QtObject{
                      id: companyFormContent
                      property string text: "<h1 style=\"color:white\">Company form</h1>

The legal form of the company must match the one indicated in the documentation of your company. Examples of what should be entered in this field: \"A Quebec limited liability partnership\"; \"A Washington State corporation\"; \"A Sole Proprietorship\". If you are the sole owner of the game, please use \"Sole Proprietorship\".
"}
                    Text {
                      Layout.preferredWidth: layoutWidth - 3 * defaultMargin
                      textFormat: TextEdit.MarkdownText
                      text: companyFormContent.text
                      color: "orange"
                      wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    }

                    FormInputLabel {
                      text: qsTr("Company form")
                    }
                    FormInput {
                      text: company_logic.company_form
                      onTextChanged: company_logic.company_form = text
                    }
                  }
                }
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
                text: qsTr("Continue")
                function handler() {
                  bicInput.focus = true
                  storeStack.currentIndex = storeStack.workshopRegisterPaymentInfoIndex
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
              id: companyPayInfoForm

              Link {
                message: qsTr("To company information")

                function handler() {
                  juridicalNameInput.focus = true
                  storeStack.currentIndex = storeStack.workshopRegisterCompanyInfoIndex
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

        ColumnLayout {
          id: releasesAppsList

          anchors.fill: parent
          anchors.leftMargin: defaultMargin

          Connections {
            target: app_logic

            function onDrafted() {
              storeStack.currentIndex = storeStack.workshopAppControlIndex
            }
          }

          RowLayout {
            Span {
              text: "Select a game to view and edit details"
            }

            ActionButton {
              text: qsTr("Draft new")
              function handler() {
                app_logic.draft_new()
              }
              visible: company_logic.is_drafted_new_button_enabled
            }
          }

          Span {
            text: qsTr("Until your company data is not approved, you cannot make new releases")
            color: "orange"
            visible: !company_logic.is_drafted_new_button_enabled
          }

          ListView {
            Layout.fillHeight: true
            model: game_list_model
            spacing: defaultMargin
            boundsBehavior: Flickable.StopAtBounds

            delegate: RowLayout {
              Text {
                textFormat: TextEdit.MarkdownText
                text: "## " + title
                color: "white"
                font.underline: true
              }

              Text {
                textFormat: TextEdit.MarkdownText
                color: is_approved ? "#ddd" : "red"
                text: is_approved ? qsTr("Approved") : qsTr("Not approved")
              }

              Text {
                textFormat: TextEdit.MarkdownText
                color: is_published ? "orange" : "#ccc"
                text: is_published ? qsTr("Published") : qsTr("Not published")
              }

              MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true
                onClicked: {
                  app_logic.map(id)
                  storeStack.currentIndex = storeStack.workshopAppControlIndex
                }
              }
            }
          }
        }

        Scroll {
          contentHeight: appControl.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: appControl

              Link {
                message: qsTr("To apps list")

                function handler() {
                  storeStack.currentIndex = storeStack.workshopAppsListIndex
                }
              }

              RowLayout {
                NeutralButton {
                  text: qsTr("Basic Info")
                  function handler() {
                    gameControlStackLayout.currentIndex = gameControlStackLayout.basicInfoPageIndex
                  }
                }

                NeutralButton {
                  text: qsTr("Descriptions")
                  function handler() {
                    gameControlStackLayout.currentIndex = gameControlStackLayout.descriptionPageIndex
                  }
                }

                NeutralButton {
                  text: qsTr("Assets")
                  function handler() {
                    gameControlStackLayout.currentIndex = gameControlStackLayout.assetsPageIndex
                  }
                }

                NeutralButton {
                  text: qsTr("Builds")
                  function handler() {
                    build_logic.load_platforms()
                    build_list_model.load_for_game(app_logic.id)
                    gameControlStackLayout.currentIndex = gameControlStackLayout.buildsPageIndex
                  }
                }

                ActionButton {
                  text: qsTr("Save")
                  function handler() {
                    app_logic.update()
                    build_logic.update(app_logic.id)
                  }
                }

                ActionButton {
                  text: qsTr("Verify")
                  function handler() {
                     app_logic.send_for_verification()
                  }
                }

                Switcher {
                    enabled: app_logic.approved
                    position: app_logic.is_published
                    onToggled: app_logic.is_published = position
                    text: qsTr("Published")
                    onClicked: app_logic.publish()
                }
              }

              StackLayout {
                id: gameControlStackLayout

                property int basicInfoPageIndex: 0
                property int descriptionPageIndex: basicInfoPageIndex + 1
                property int assetsPageIndex: descriptionPageIndex + 1
                property int buildsPageIndex: assetsPageIndex + 1

                ColumnLayout {
                  FormInputLabel {
                    text: qsTr("Title")
                  }
                  FormInput {
                    text: app_logic.title
                    onTextChanged: app_logic.title = text
                  }

                  Checking {
                    id: is_coming_soon
                    text: qsTr("Coming soon")
                    checked: app_logic.coming_soon
                    onClicked: app_logic.coming_soon = checked
                  }

                  FormInputLabel {
                    text: qsTr("Release date")
                    visible: !is_coming_soon.checked
                  }

                  RowLayout {
                    id: dateSection

                    visible: !is_coming_soon.checked

                    Combo {
                      implicitWidth: 76
                      model: app_logic.possible_days
                      currentIndex: app_logic.day_index
                      onCurrentIndexChanged: app_logic.day_index = currentIndex
                    }

                    Combo {
                      implicitWidth: 76
                      model: app_logic.possible_months
                      currentIndex: app_logic.month_index
                      onCurrentIndexChanged: release_logic.month_index = currentIndex
                    }

                    Combo {
                      implicitWidth: 76
                      model: app_logic.possible_years
                      currentIndex: app_logic.year_index
                      onCurrentIndexChanged: app_logic.year_index = currentIndex
                    }
                  }

                  Indent {
                    visible: !is_coming_soon.checked
                  }

                  FormInputLabel {
                    text: qsTr("Price")
                  }
                  FormInput {
                    text: app_logic.price
                    onTextChanged: app_logic.price = text
                  }
                }

                ColumnLayout {
                  Text {
                    color: highlightedTextColor
                    Layout.preferredWidth: layoutWidth
                    wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    textFormat: TextEdit.MarkdownText
                    text: "
Long description supports Markdown.
"
                  }

                  Indent {}

                  RowLayout {
                    Header {
                      text: "# Short description"
                    }

                    Span {
                      text: shortDescriptionArea.length + "/" + shortDescriptionArea.limit
                    }
                  }

                  Scroll {
                    Layout.preferredWidth: layoutWidth / 2
                    Layout.preferredHeight: 125

                    TextArea {
                      id: shortDescriptionArea
                      property int limit: 250
                      background: Rectangle {
                        color: "black"

                        radius: 4

                        MouseArea {
                          anchors.fill: parent
                          hoverEnabled: true
                          cursorShape: Qt.IBeamCursor
                          onEntered: parent.color = Qt.darker("#0E151E", 1.5)
                          onExited: parent.color =  "black"
                        }
                      }
                      font.pointSize: 12
                      Layout.preferredWidth: layoutWidth / 2
                      Layout.preferredHeight: 125
                      wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                      text: app_logic.short_description
                      onTextChanged: {
                        if (length > limit) remove(limit, length)
                        app_logic.short_description = text
                      }
                    }
                  }

                  Indent {}

                  RowLayout {
                    Header {
                      text: "# Long description"
                    }

                    Span {
                      text: longDescriptionArea.length + "/" + longDescriptionArea.limit
                    }
                  }

                  Scroll {
                    Layout.preferredWidth: layoutWidth / 2
                    Layout.preferredHeight: 350

                    TextArea {
                      id: longDescriptionArea
                      property int limit: 1000
                      background: Rectangle {
                        color:  "black"

                        radius: 4

                        MouseArea {
                          anchors.fill: parent
                          hoverEnabled: true
                          cursorShape: Qt.IBeamCursor
                          onEntered: parent.color = Qt.darker("#0E151E", 1.5)
                          onExited: parent.color =  "black"
                        }
                      }
                      font.pointSize: 12
                      Layout.preferredWidth: layoutWidth / 2
                      Layout.preferredHeight: 350
                      wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                      text: app_logic.long_description
                      onTextChanged: {
                        if (length > limit) remove(limit, length)
                        app_logic.long_description = text
                      }
                    }
                  }
                }

                ColumnLayout {
                  RowLayout {
                    Platform.FileDialog {
                      id: attach_header_image_file_dialog
                      fileMode: Platform.FileDialog.OpenFile
                      nameFilters: ["Images (*.webp)"]
                      onAccepted: app_logic.header = file
                      folder: StandardPaths.writableLocation(StandardPaths.PicturesLocation)
                    }

                    Text {
                      text: qsTr("Header image (*.webp):")
                      color: "white"
                    }

                    Text {
                      text: app_logic.displayed_header
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.header !== ""
                      text: qsTr("X")
                      function handler() {
                       app_logic.header = ""
                      }
                    }
                  }

                  NeutralButton {
                    text: qsTr("Attach")
                    function handler() {
                     attach_header_image_file_dialog.open()
                    }
                  }

                  Indent {}

                  RowLayout {
                    Platform.FileDialog {
                      id: attach_capsule_image_file_dialog
                      fileMode: Platform.FileDialog.OpenFile
                      nameFilters: ["Images (*.webp)"]
                      onAccepted: app_logic.capsule = file
                      folder: StandardPaths.writableLocation(StandardPaths.PicturesLocation)
                    }

                    Text {
                      text: qsTr("Capsule image (*.webp):")
                      color: "white"
                    }

                    Text {
                      text: app_logic.displayed_capsule
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.capsule !== ""
                      text: qsTr("X")
                      function handler() {
                       app_logic.capsule = ""
                      }
                    }
                  }

                  NeutralButton {
                    text: qsTr("Attach")
                    function handler() {
                     attach_capsule_image_file_dialog.open()
                    }
                  }

                  Indent {}

                  RowLayout {
                    Platform.FileDialog {
                      id: attach_screenshots_file_dialog
                      fileMode: Platform.FileDialog.OpenFiles
                      nameFilters: ["Images (*.webp)"]
                      onAccepted: app_logic.screenshots = files
                      folder: StandardPaths.writableLocation(StandardPaths.PicturesLocation)
                    }

                    Text {
                      text: qsTr("Screenshots (*webp):")
                      color: "white"
                    }

                    Text {
                      text: app_logic.displayed_screenshots
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.displayed_screenshots !== ""
                      text: qsTr("X")
                      function handler() {
                       app_logic.screenshots = []
                      }
                    }
                  }

                  NeutralButton {
                    text: qsTr("Attach")
                    function handler() {
                     attach_screenshots_file_dialog.open()
                    }
                  }

                  Indent {}

                  RowLayout {
                    Platform.FileDialog {
                      id: attach_trailers_file_dialog
                      fileMode: Platform.FileDialog.OpenFiles
                      nameFilters: ["Videos (*.webm *.mp4)"]
                      onAccepted: app_logic.trailers = files
                      folder: StandardPaths.writableLocation(StandardPaths.PicturesLocation)
                    }

                    Text {
                      text: qsTr("Trailers (*.webm *.mp4):")
                      color: "white"
                    }

                    Text {
                      text: app_logic.displayed_trailers
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.displayed_trailers !== ""
                      text: qsTr("X")
                      function handler() {
                       app_logic.trailers = []
                      }
                    }
                  }

                  NeutralButton {
                    text: qsTr("Attach")
                    function handler() {
                     attach_trailers_file_dialog.open()
                    }
                  }
                }

                StackLayout {
                  id: buildsStackLayout

                  property int buildsListIndex: 0
                  property int buildControlIndex: buildsListIndex + 1

                  Connections {
                    target: build_logic

                    function onDrafted() {
                      buildsStackLayout.currentIndex = buildsStackLayout.buildControlIndex
                    }
                  }

                  ColumnLayout {
                    RowLayout {
                      Text {
                        color: highlightedTextColor
                        text: "Here you can view and build your app build for a specific platform."
                      }

                      ActionButton {
                        text: qsTr("Draft new")
                        function handler() {
                          build_logic.draft_new(app_logic.id)
                        }
                      }
                    }

                    ListView {
                      Layout.fillHeight: true
                      model: build_list_model
                      spacing: defaultMargin
                      boundsBehavior: Flickable.StopAtBounds

                      delegate: RowLayout {
                        Text {
                          textFormat: TextEdit.MarkdownText
                          text: "## " + platform_title
                          color: "white"
                          font.underline: true
                        }

                        MouseArea {
                          anchors.fill: parent
                          cursorShape: Qt.PointingHandCursor
                          hoverEnabled: true
                          onClicked: {
                            build_logic.map(id)
                            buildsStackLayout.currentIndex = buildsStackLayout.buildControlIndex
                          }
                        }
                      }
                    }
                  }

                  ColumnLayout {
                    Link {
                      message: qsTr("To the builds")

                      function handler() {
                        build_list_model.load_for_game(app_logic.id)
                        buildsStackLayout.currentIndex = buildsStackLayout.buildsListIndex
                      }
                    }

                    Indent {}

                    FormInputLabel {text: qsTr("Call")}
                    FormInput {
                      text: build_logic.call
                      onTextChanged: build_logic.call = text
                    }

                    Indent {}

                    FormInputLabel {text: qsTr("Parameters")}
                    FormInput {
                      text: build_logic.params
                      onTextChanged: build_logic.params = text
                    }

                    Indent {}

                    FormInputLabel {text: qsTr("Target platform")}
                    Combo {
                      model: build_logic.displayed_platforms
                      currentIndex: build_logic.selected_platform_index
                      onCurrentIndexChanged: build_logic.selected_platform_index = currentIndex
                    }

                    Indent {}

                    RowLayout {
                      Platform.FileDialog {
                        id: attach_project_archive_file_dialog
                        fileMode: Platform.FileDialog.OpenFile
                        nameFilters: ["Archive (*.zip *.rar *.7z)"]
                        onAccepted: build_logic.project_archive = file
                        folder: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
                      }

                      Text {
                        text: qsTr("Archive (*.zip *.rar *.7z):")
                        color: "white"
                      }

                      Text {
                        text: build_logic.project_archive
                        color: "orange"
                      }
                    }

                    NeutralButton {
                      text: qsTr("Attach")
                      function handler() {
                       attach_project_archive_file_dialog.open()
                      }
                    }

                    Text {
                      text: "Please note: when unpacking the archive, you should get the root directory of your project with all the files"
                      color: "orange"
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