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
      property int workshopIntroductionIndex: storeDetailedGameIndex + 1
      property int workshopRegisterCompanyInfoIndex: workshopIntroductionIndex + 1
      property int workshopRegisterPaymentInfoIndex: workshopRegisterCompanyInfoIndex + 1
      property int workshopAppsListIndex: workshopRegisterPaymentInfoIndex + 1
      property int workshopAppControlIndex: workshopAppsListIndex + 1

      function checkCompanyRegistration() {
        company_logic.check()
      }

      Connections {
        target: company_logic

        function onNotRegistered() {
          storeStackLayout.currentIndex = storeStackLayout.workshopIntroductionIndex
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
        contentHeight: introduction.height + 2 * defaultMargin

        Item {
          width: layoutWidth
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: introduction

            Indent {}

            Header {text: "Foggie Workshop"}

            Indent {}

            Span {text: "Are you a developer and want to use our platform to distribute your games and software? This is great, let's get started."}

            Indent {}

            SubHeader {text: "What to expect"}

            Divider {}

            Span {text: "General procedure for publishing products:"}
            Span {text: "1. Fill in electronic documents:"}
            Span {text: " - Information about the legal entity"}
            Span {text: " - Banking / tax information"}
            Span {
              text: "2. Once you have access to the Workshop, start preparing your product for release. You will need to create a store page, upload product builds, and enter your desired price."
            }
            Span {
              text: "3. Prior to the final launch of your build of the game and the store page, we will run a test run of the game and check the page to make sure there are no errors or malicious elements.\nThe verification usually takes 1 to 5 days."
            }

            Indent {}

            SubHeader {text: "Information to keep handy:"}

            Divider {}

            Span {text: "- Legal details and name"}
            Span {text: "Accurate legal information about the person or company signing the agreement so we understand who you are and who you represent. This is information about your company."}

            Span {text: "- Payment Information"}
            Span {text: "Accurate banking information on where to transfer the proceeds from the sales of your application: bank code, bank account number and bank address."}

            Indent {}

            SubHeader {text: "Rules and regulations"}

            Divider {}

            Span {text: "What should not be distributed using our platform:"}

            Span {text: "- Advocacy of hatred, violence or discrimination against groups of people based on ethnicity, religion, gender, age, disability or sexual orientation."}
            Span {text: "- Images of a sexual nature with real people."}
            Span {text: "- Adult content that is not labeled as such and contains no age rating information."}
            Span {text: "- Slanderous statements or statements that offend honor and dignity. Content to which you do not own the rights."}
            Span {text: "- Content to which you do not own the rights."}
            Span {text: "- Content that violates the laws of the countries in which it will be distributed."}
            Span {text: "- Content that is blatantly offensive or intentionally shocks or disgusts the public."}
            Span {text: "- Content that is in any way related to the exploitation of minors."}
            Span {text: "- Applications that change the user's computer in ways they do not expect or that cause harm, such as viruses or malware."}
            Span {text: "- Applications that attempt to fraudulently obtain sensitive information (such as login details) or financial data (such as credit card information)."}
            Span {text: "- Video content that is not directly related to the product released on platform."}
            Span {text: "- Non-interactive panoramic virtual reality videos."}
            Span {text: "- Applications created using blockchain technology that issue or exchange cryptocurrencies or NFTs (non-fungible tokens)."}

            Indent {}

            Span {text: "Allowed types of content"}

            Span {text: "First of all, we accept games. Non-gaming software may be accepted if it falls into one of the following categories:"}

            Span {text: "- animation and modeling;"}
            Span {text: "- work with sound and video;"}
            Span {text: "- design and illustration;"}
            Span {text: "- photo processing;"}
            Span {text: "- education and training;"}
            Span {text: "- finance and accounting;"}
            Span {text: "- tools for players;"}

            Indent {}

            SubHeader {text: "Let's get started"}

            Divider {}

            Span {text: "Click the Continue button to proceed to enter your legal name and contact information."}

            NeutralButton {
              text: qsTr("Continue")
              function handler() {
                bicInput.focus = true
                storeStackLayout.currentIndex = storeStackLayout.workshopRegisterCompanyInfoIndex
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

            Link {
              message: qsTr("To introduction")

              function handler() {
                juridicalNameInput.focus = true
                storeStackLayout.currentIndex = storeStackLayout.workshopIntroductionIndex
              }
            }

            Indent {}

            Rectangle {
              width: layoutWidth - 2 * defaultMargin
              height: legalNameExplanationLayout.height + 2 * defaultMargin
              radius: defaultMargin
              border.color: "orange"
              border.width: 1
              color: "transparent"

              Item {
                width: parent.width - 2 * defaultMargin
                anchors.horizontalCenter: parent.horizontalCenter

                ColumnLayout {
                  id: legalNameExplanationLayout

                  Indent {}

                  SubHeader {text: "Legal name"}

                  Indent {}

                  Span {
                    color: "orange"
                    lineHeight: 0.5
                    text: "The organization whose name you enter below must be the legal entity that will sign the required license agreements. The company name entered here must match the name on
\nofficial bank documents and documents provided to the tax office, or foreign tax documents, if any. If you later add bank account information, you will need to re-enter that
\nnameas the account holder and legal entity with the appropriate tax identification number."
                  }

                  Indent {}

                  Span {
                    color: "orange"
                    lineHeight: 0.5
                    text: "If you do not have a company name and are the sole owner of the content you wish to post, please enter your full name and mailing address in the \"Legal Name\" and \"Street,
\nHouse and Apartment/Office Number\" fields. If you co-own the game along with other people, you will need to register a legal entity that will own the content and accept
\npayments for it."
                  }

                  Indent {}

                  Span {
                    color: "orange"
                    lineHeight: 0.5
                    text: "The legal name specified here is used internally by the system. If you have a commercial or informal name that you want to use in your store, you can specify it separately when
\nyou create your store page."
                  }

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
                }
              }
            }

            Indent {}

            Rectangle {
              width: layoutWidth - 2 * defaultMargin
              height: companyFormExplanationLayout.height + 2 * defaultMargin
              radius: defaultMargin
              border.color: "orange"
              border.width: 1
              color: "transparent"

              Item {
                width: parent.width - 2 * defaultMargin
                anchors.horizontalCenter: parent.horizontalCenter

                ColumnLayout {
                  id: companyFormExplanationLayout

                  Indent {}

                  SubHeader {text: "Company form"}

                  Indent {}

                  Span {
                    color: "orange"
                    lineHeight: 0.5
                    text: "The legal form of the company must match the one indicated in the documentation of your company. Examples of what should be entered in this field: \"A Quebec limited liability
\npartnership\"; \"A Washington State corporation\"; \"A Sole Proprietorship\". If you are the sole owner of the game, please use \"Sole Proprietorship\"."
                  }

                  Indent {}

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
                storeStackLayout.currentIndex = storeStackLayout.workshopRegisterPaymentInfoIndex
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
        contentHeight: releasesAppsList.height + 2 * defaultMargin

        Item {
          width: layoutWidth
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: releasesAppsList

            Connections {
              target: app_logic

              function onDrafted() {
                storeStackLayout.currentIndex = storeStackLayout.workshopAppControlIndex
              }
            }

            Indent {}

            ActionButton {
              text: qsTr("Draft new")
              function handler() {
                app_logic.draft_new()
              }
              visible: company_logic.is_drafted_new_button_enabled
            }

            Span {
              text: qsTr("Until your company data is not approved, you cannot make new releases")
              color: "orange"
              visible: !company_logic.is_drafted_new_button_enabled
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

      Scroll {
        contentHeight: appControl.height + 2 * defaultMargin

        Item {
          width: layoutWidth
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: appControl

            Indent {}

            Link {
              message: qsTr("To apps list")

              function handler() {
                storeStackLayout.currentIndex = storeStackLayout.workshopAppsListIndex
              }
            }

            Indent {}

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
                Indent {}

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
                Indent {}

                FormInputLabel {
                  text: qsTr("Short description")
                }
                TextArea {
                  background: Rectangle {
                    color: Qt.darker("#212834", 1.2)

                    radius: 4

                    MouseArea {
                      anchors.fill: parent
                      hoverEnabled: true
                      cursorShape: Qt.IBeamCursor
                      onEntered: parent.color = Qt.darker("#212834", 1.5)
                      onExited: parent.color = Qt.darker("#212834", 2)
                    }
                  }
                  font.pointSize: 12
                  Layout.preferredWidth: layoutWidth / 4
                  Layout.preferredHeight: 150
                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                  text: app_logic.short_description
                  onTextChanged: app_logic.short_description = text
                }

                Indent {}

                FormInputLabel {
                  text: qsTr("Long description")
                }
                TextArea {
                  background: Rectangle {
                    color: Qt.darker("#212834", 1.2)

                    radius: 4

                    MouseArea {
                      anchors.fill: parent
                      hoverEnabled: true
                      cursorShape: Qt.IBeamCursor
                      onEntered: parent.color = Qt.darker("#212834", 1.5)
                      onExited: parent.color = Qt.darker("#212834", 2)
                    }
                  }
                  font.pointSize: 12
                  Layout.preferredWidth: layoutWidth / 2
                  Layout.preferredHeight: 250
                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                  text: app_logic.long_description
                  onTextChanged: app_logic.long_description = text
                }
              }

              ColumnLayout {
                Indent {}

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
                  Indent {}

                  ActionButton {
                    text: qsTr("Draft new")
                    function handler() {
                      build_logic.draft_new(app_logic.id)
                    }
                  }

                  ListView {
                    Layout.fillHeight: true

                    model: build_list_model

                    delegate: RowLayout {
                      Text {
                        text: platform_title
                        color: "white"
                        font.underline: true

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
                }

                ColumnLayout {
                  Indent {}

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
                }
              }
            }
          }
        }
      }
    }
  }
}