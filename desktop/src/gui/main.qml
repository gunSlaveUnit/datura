import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 2.15

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
        NeutralButton {
          text: qsTr("Store")

          function handler() {
            game_list_model.load_store()
            storeStack.currentIndex = storeStackLayout.storeIndex
          }
        }

        NeutralButton {
          text: qsTr("Library")
        }

        NeutralButton {
          text: qsTr("Workroom")
          function handler() {
            storeStack.checkCompanyRegistration()
          }
        }
      }

      StackLayout {
        id: storeStack

        property int storeIndex: 0
        property int storeDetailedIndex: storeIndex + 1
        property int workshopIntroductionIndex: storeDetailedIndex + 1
        property int workshopRegisterCompanyInfoIndex: workshopIntroductionIndex + 1
        property int workshopRegisterPaymentInfoIndex: workshopRegisterCompanyInfoIndex + 1
        property int workshopAppsListIndex: workshopRegisterPaymentInfoIndex + 1
        property int workshopAppControlIndex: workshopAppsListIndex + 1

        function checkCompanyRegistration() { company_logic.check() }

        Connections {
          target: company_logic

          function onNotRegistered() {
            storeStack.currentIndex = storeStack.workshopIntroductionIndex
          }

          function onRegistered() {
            game_list_model.load_personal()
            storeStack.currentIndex = storeStack.workshopAppsListIndex
          }
        }

        Connections {
          target: auth_logic

          function onRegistered() { game_list_model.load_store() }
          function onLogin() { game_list_model.load_store() }

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
      }
    }
  }
}