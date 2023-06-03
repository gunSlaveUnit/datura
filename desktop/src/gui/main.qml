import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import Qt.labs.platform as Platform

Window {
  id: window

  width: 900
  height: 450
  minimumWidth: signUpForm.width + 2 * defaultMargin
  minimumHeight: signUpForm.height + 2 * defaultMargin
  visible: true
  title: "Salad"

  property int defaultMargin: 8

  function humanTimestamp(timestamp) {
    var date = new Date(timestamp * 1000)
    var dateString = date.toLocaleDateString('ru-RU', "dd MMM yyyy");
    return dateString
  }

  StackLayout {
    id: authStack

    anchors.centerIn: parent

    property int signInIndex: 0
    property int signUpIndex: 1

    Connections {
      target: auth_logic

      function onRegistered() {
        loadUserRelatedData()

        game_list_model.load_store()

        authStack.visible = false
        storeSection.visible = true
      }

      function onLogin() {
        loadUserRelatedData()

        game_list_model.load_store()

        authStack.visible = false
        storeSection.visible = true
      }

      function onLogout() {
        authStack.currentIndex = authStack.signInFormIndex
        mainStack.currentIndex = mainStack.authorizationIndex
        storeStack.currentIndex = storeStack.storeIndex
      }

      function loadUserRelatedData() {
        current_user_logic.map()
        wallet_logic.map()
      }
    }

    ColumnLayout {
      Layout.alignment: Qt.AlignCenter

      GridLayout {
        columns: 2

        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("ACCOUNT NAME")
        }
        TextField {
          id: accountNameField
          Layout.fillWidth: true
          focus: true
          text: auth_logic.account_name
          onTextChanged: auth_logic.account_name = text
        }

        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("PASSWORD")
        }
        TextField {
          Layout.fillWidth: true
          echoMode: TextInput.Password
          text: auth_logic.password
          onTextChanged: auth_logic.password = text
        }
      }

      CheckBox {
        Layout.alignment: Qt.AlignHCenter
        text: qsTr("Remember me")
      }

      Button {
        id: signInButton
        Layout.alignment: Qt.AlignHCenter
        text: qsTr("Sign in")
        onClicked: auth_logic.sign_in()
      }

      Separator {}

      GridLayout {
        columns: 2
        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("Don't have a Salad account?")
        }
        Button {
          Layout.fillWidth: true
          text: qsTr("Create a new account ...")
          onClicked: {
            auth_logic.reset()
            emailAddressField.focus = true
            authStack.currentIndex = authStack.signUpIndex
          }
        }
        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("Need help with sign in?")
        }
        Button {
          Layout.fillWidth: true
          text: qsTr("I can't sign in ...")
        }
      }
    }

    ColumnLayout {
      id: signUpForm

      Layout.alignment: Qt.AlignCenter

      GridLayout {
        columns: 2

        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("EMAIL ADDRESS")
        }
        TextField {
          id: emailAddressField
          Layout.fillWidth: true
          text: auth_logic.email
          onTextChanged: auth_logic.email = text
        }

        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("ACCOUNT NAME")
        }
        TextField {
          Layout.fillWidth: true
          text: auth_logic.account_name
          onTextChanged: auth_logic.account_name = text
        }

        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("PASSWORD")
        }
        TextField {
          Layout.fillWidth: true
          echoMode: TextInput.Password
          text: auth_logic.password
          onTextChanged: auth_logic.password = text
        }

        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("COUNTRY OF RESIDENCE")
        }
        ComboBox {
          Layout.fillWidth: true
          model: [
            qsTr("Russia"),
            qsTr("USA")
          ]
        }
      }

      Button {
        id: signUpButton
        Layout.alignment: Qt.AlignHCenter
        text: qsTr("Sign up")
        onClicked: auth_logic.sign_up()
      }

      Separator {}

      GridLayout {
        columns: 2

        Text {
          Layout.alignment: Qt.AlignRight
          text: qsTr("Already have an account?")
        }
        Button {
          Layout.fillWidth: true
          text: qsTr("Login to an existing account ...")
          onClicked: {
            accountNameField.focus = true
            auth_logic.reset()
            authStack.currentIndex = authStack.signInIndex
          }
        }
      }
    }
  }

  ColumnLayout {
    id: storeSection
    visible: false

    anchors.fill: parent

    RowLayout {
      Layout.fillWidth: true
      Layout.leftMargin: defaultMargin
      Layout.rightMargin: defaultMargin

      Button {
        text: qsTr("Store")
        onClicked: {
          game_list_model.load_store()
          storeStack.currentIndex = storeStack.storeIndex
        }
      }

      Button {
        text: qsTr("Library")
        onClicked: {
          game_list_model.load_library()
          storeStack.currentIndex = storeStack.libraryIndex
        }
      }

      Button {
        text: qsTr("Workshop")
        onClicked: storeStack.checkCompanyRegistration()
      }

      Item {Layout.fillWidth: true}

      Rectangle {
        Layout.preferredWidth: userAccountName.contentWidth + 32 + defaultMargin * 3 + userBalance.contentWidth
        Layout.preferredHeight: 24
        color: "lightgray"
        radius: defaultMargin / 4

        RowLayout {
          anchors.fill: parent

          AnimatedImage {
            id: avatar
            Layout.preferredHeight: parent.height
            Layout.preferredWidth: height
            mipmap: true
            source: `http://127.0.0.1:8000/api/v1/users/${current_user_logic.id}/avatar/`
          }

          Text {
            id: userAccountName
            text: current_user_logic.displayed_name.slice(0, 15) + (current_user_logic.displayed_name.length > 15 ? "..." : "")
          }

          Text {
            id: userBalance
            text: (wallet_logic.balance).toFixed(2) + " $"
          }
        }

        Menu {
          id: userProfileMenu

          width: parent.width

          y: parent.height

          MenuItem {
            text: qsTr("Profile")
            onTriggered: storeStack.currentIndex = storeStack.profileIndex
          }

          MenuItem {
            text: qsTr("Cart")
            onTriggered: {
              game_list_model.load_cart()
              storeStack.currentIndex = storeStack.cartIndex
              game_list_model.recount_total_cost()
            }
          }

          MenuItem {
            text: qsTr("Wallet")
            onTriggered: storeStack.currentIndex = storeStack.walletIndex
          }

          MenuItem {
            text: qsTr("Logout")
            onTriggered: auth_logic.sign_out()
          }
        }

        MouseArea {
          anchors.fill: parent
          hoverEnabled: true
          onEntered: parent.color = "gray"
          onExited: parent.color = "lightgray"
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

      function checkCompanyRegistration() {
        company_logic.check()
      }

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

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: searchField.height + gamesList.contentHeight

        ColumnLayout {
          implicitWidth: window.width - 2 * defaultMargin
          height: parent.height

          TextField {
            id: searchField
            text: game_list_model.search
            onTextChanged: {
              game_list_model.search = text
              game_list_model.load_store()
            }
          }

          ListView {
            id: gamesList
            Layout.fillHeight: true
            model: game_list_model
            boundsBehavior: Flickable.StopAtBounds

            delegate: RowLayout {
              Image {
                id: storeHeaderImage
                Layout.preferredWidth: height * 16 / 9
                Layout.preferredHeight: parent.height
                source: `http://127.0.0.1:8000/api/v1/games/${id}/header/`
                mipmap: true
              }

              Text {
                text: title

                MouseArea {
                  anchors.fill: parent
                  onClicked: {
                    store_detailed_logic.map(id)
                    reviews_list_model.load(id)
                    storeStack.currentIndex = storeStack.storeDetailedIndex
                  }
                }
              }

              Text {
                text: release_date ? humanTimestamp(release_date) : "Coming soon"
              }

              Text {
                text: short_description
                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
              }
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: storeGameDetailedPage.height + reviewsList.contentHeight + defaultMargin

        ColumnLayout {
          implicitWidth: window.width - 2 * defaultMargin // FIXME: ugly
          height: parent.height

          ColumnLayout {
            id: storeGameDetailedPage
            implicitWidth: parent.width

            Button {
              text: qsTr("To the store")

              onClicked: {
                game_list_model.load_store()
                storeStack.currentIndex = storeStack.storeIndex
              }
            }

            Text {text: store_detailed_logic.title}

            RowLayout {
              width: parent.width

              ColumnLayout {
                width: parent.width * 0.3

                Text {
                  Layout.preferredWidth: parent.width
                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                  text: store_detailed_logic.short_description
                }

                RowLayout {
                  width: parent.width

                  Text {
                    Layout.preferredWidth: parent.width
                    wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    text: qsTr("Release date: ") + (store_detailed_logic.release_date ? humanTimestamp(store_detailed_logic.release_date) : "Coming soon")
                  }
                }

                RowLayout {
                  width: parent.width

                  Text {
                    Layout.preferredWidth: parent.width
                    wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    text: qsTr("Developer: ") + store_detailed_logic.developer
                  }
                }

                RowLayout {
                  width: parent.width

                  Text {
                    Layout.preferredWidth: parent.width
                    wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    text: qsTr("Publisher: ") + store_detailed_logic.publisher
                  }
                }

                RowLayout {
                  width: parent.width

                  Text {
                    Layout.preferredWidth: parent.width
                    wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    text: qsTr("Reviews: ") + (
                      reviews_list_model.rating > 0.9 ? qsTr("Very positive") :
                      reviews_list_model.rating > 0.78 ? qsTr("Positive") :
                      reviews_list_model.rating > 0.6 ? qsTr("Mostly positive") :
                      reviews_list_model.rating > 0.4 ? qsTr("Neutral") :
                      reviews_list_model.rating > 0.22 ? qsTr("Mostly negative") :
                      reviews_list_model.rating > 0.1 ? qsTr("Negative") : qsTr("Extremely negative")
                    )
                  }
                }
              }
            }

            RowLayout {
              visible: store_detailed_logic.location === 0

              Text {text: qsTr("Buy ") + store_detailed_logic.title}

              Text {text: store_detailed_logic.price + " $"}

              Button {
                text: qsTr("Add to cart")
                onClicked: {
                  cart_logic.add(store_detailed_logic.id)
                  store_detailed_logic.location = 2
                }
              }
            }

            Text {
              text: qsTr("Already in library")
              visible: store_detailed_logic.location === 1
            }

            Text {
              text: qsTr("Already in cart")
              visible: store_detailed_logic.location === 2
            }

            Text {
              textFormat: TextEdit.MarkdownText
              Layout.preferredWidth: parent.width
              wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
              text: store_detailed_logic.long_description
            }

            ColumnLayout {
              visible: store_detailed_logic.location === 1

              Text {text: qsTr("Share your opinion about this product")}

              Scroll {
                Layout.preferredWidth: parent.width / 2
                Layout.preferredHeight: 125

                TextArea {
                  property int limit: 500

                  Layout.preferredWidth: parent.width / 2
                  Layout.preferredHeight: 125

                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere

                  background: Rectangle {
                    color: "lightgray"

                    MouseArea {
                      anchors.fill: parent
                      hoverEnabled: true
                      cursorShape: Qt.IBeamCursor
                    }
                  }

                  text: review_logic.content
                  onTextChanged: {
                    if (length > limit) remove(limit, length)
                    review_logic.content = text
                  }
                }
              }

              CheckBox {
                text: qsTr("I recommend this game")
                checked: review_logic.is_recommended
                onClicked: review_logic.is_recommended = checked
              }

              Button {
                text: qsTr("Send")
                onClicked: review_logic.new(store_detailed_logic.id)
              }
            }
          }

          ListView {
            id: reviewsList
            Layout.fillHeight: true
            model: reviews_list_model
            boundsBehavior: Flickable.StopAtBounds

            delegate: RowLayout {
              Text {
                text: content
              }
            }
          }
        }
      }

      GridView {
        id: storeGamesGridView

        anchors.fill: parent
        anchors.margins: defaultMargin

        boundsBehavior: Flickable.StopAtBounds

        property int capsuleImageWidth: 12 * 11
        property int capsuleImageHeight: capsuleImageWidth * 16 / 11

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
              library_detailed_logic.map(id)
              storeStack.currentIndex = storeStack.libraryDetailedIndex
            }
          }
        }
      }

      Scroll {
        contentHeight: libraryDetailedPage.height + 2 * defaultMargin

        Item {
          width: layoutWidth - 3 * defaultMargin
          anchors.horizontalCenter: parent.horizontalCenter

          ColumnLayout {
            id: libraryDetailedPage

            Layout.preferredWidth: parent.width

            Image {
              Layout.preferredWidth: layoutWidth - 3 * defaultMargin
              Layout.preferredHeight: width * 9 / 16
              source: `http://127.0.0.1:8000/api/v1/games/${library_detailed_logic.game_id}/header/`
              mipmap: true

              Rectangle {
                anchors.fill: parent
                gradient: Gradient {
                  GradientStop { position: 0.9; color: backgroundWindowColor }
                  GradientStop { position: 0.5; color: "transparent" }
                }
              }

              RowLayout {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: defaultMargin

                Header {
                  text: "# " + library_detailed_logic.game_title
                }

                Item {
                  Layout.preferredWidth: 2 * defaultMargin
                }

                ActionButton {
                  visible: library_detailed_logic.app_status === 0
                  text: qsTr("Установить")
                  onClicked:  library_detailed_logic.download()
                }

                BuyButton {
                  visible: library_detailed_logic.app_status === 1
                  text: qsTr("Запуск")
                  onClicked: library_detailed_logic.launch()
                }

                NeutralButton {
                  visible: library_detailed_logic.app_status === 2
                  text: library_detailed_logic.loading_progress
                }

                ActionButton {
                  visible: library_detailed_logic.app_status === 3
                  text: qsTr("Остановить")
                  onClicked: library_detailed_logic.shutdown()
                }

                Text {
                  visible: library_detailed_logic.app_status === 4
                  text: "Игра находится в вашей библиотеке, но недоступна для вашей платформы"
                  color: "white"
                }

                Text {
                  visible: library_detailed_logic.app_status === 5
                  text: "Недоступно для загрузки. Попробуйте позже"
                  color: "white"
                }

                Item {
                  Layout.fillWidth: true
                }

                Item {
                  Layout.preferredWidth: 2 * defaultMargin
                }

                ColumnLayout {
                  Regular {content: "Последний запуск"}
                  Regular {
                    Layout.alignment: Qt.AlignHCenter
                    content: library_detailed_logic.last_launched
                  }
                }

                Item {
                  Layout.preferredWidth: 2 * defaultMargin
                }

                ColumnLayout {
                  visible: library_detailed_logic.play_time !== "0"
                  Regular {content: "Вы играли"}
                  Regular {
                    Layout.alignment: Qt.AlignHCenter
                    content: library_detailed_logic.play_time
                  }
                }
              }
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: profilePage.height

        ColumnLayout {
          id: profilePage

          implicitWidth: window.width - 2 * defaultMargin

          AnimatedImage {
            Layout.preferredWidth: 100
            Layout.preferredHeight: 100
            mipmap: true
            source: `http://127.0.0.1:8000/api/v1/users/${current_user_logic.id}/avatar/`
          }

          Text {text: current_user_logic.displayed_name}
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: cartList.contentHeight + paymentExplanation.height + buyButton.height

        ColumnLayout {
          implicitWidth: window.width - 2 * defaultMargin // FIXME: ugly
          height: parent.height

          Button {
            id: buyButton
            text: qsTr("Pay ") + game_list_model.total_cost + " $"
            onClicked: {
              cart_logic.pay()
              game_list_model.load_cart()
              game_list_model.recount_total_cost()
              wallet_logic.map()
            }
          }

          Text {
            id: paymentExplanation
            Layout.preferredWidth: parent.width
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
            text: qsTr("Your purchase will be debited from your Salad wallet. If there are not enough funds on it, replenish the balance")
          }

          ListView {
            id: cartList
            Layout.fillHeight: true
            model: game_list_model
            boundsBehavior: Flickable.StopAtBounds

            delegate: RowLayout {
              Text {text: title}

              Text {text: price + " $"}

              MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                  store_detailed_logic.map(id)
                  reviews_list_model.load(id)
                  storeStack.currentIndex = storeStack.storeDetailedIndex
                }
              }

              Button {
                text: qsTr("Remove")
                onClicked: {
                  cart_logic.delete(cart_record_id)
                  game_list_model.load_cart()
                  game_list_model.recount_total_cost()
                }
              }
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: walletPage.height

        ColumnLayout {
          id: walletPage
          implicitWidth: window.width - 2 * defaultMargin
          height: parent.height

          Text {text: qsTr("Balance: ") + wallet_logic.balance + " $"}

          Button {
            text: qsTr("Add 5 $")

            onClicked: {
              wallet_logic.amount = 5
              storeStack.currentIndex = storeStack.walletTopUpIndex
            }
          }

          Button {
            text: qsTr("Add 10 $")

            onClicked: {
              wallet_logic.amount = 10
              storeStack.currentIndex = storeStack.walletTopUpIndex
            }
          }

          Button {
            text: qsTr("Add 25 $")

            onClicked: {
              wallet_logic.amount = 25
              storeStack.currentIndex = storeStack.walletTopUpIndex
            }
          }

          Button {
            text: qsTr("Add 50 $")

            onClicked: {
              wallet_logic.amount = 50
              storeStack.currentIndex = storeStack.walletTopUpIndex
            }
          }

          Button {
            text: qsTr("Add 100 $")

            onClicked: {
              wallet_logic.amount = 100
              storeStack.currentIndex = storeStack.walletTopUpIndex
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: walletTopUpPage.height

        ColumnLayout {
          id: walletTopUpPage
          implicitWidth: window.width - 2 * defaultMargin
          height: parent.height

          Button {
            text: qsTr("To wallet balance")

            onClicked: storeStack.currentIndex = storeStack.walletIndex
          }

          Text {text: qsTr("Choose a payment method")}

          RowLayout {
            ComboBox {
              id: paymentMethods

              model: [
                "Bank card"
              ]
            }

            Button {
              text: qsTr("Pay")

              enabled: cvvcvc.acceptableInput && cardNumber.acceptableInput && month.acceptableInput && year.acceptableInput

              onClicked: {
                wallet_logic.top_up()
                storeStack.currentIndex = storeStack.walletIndex
              }
            }
          }

          GridLayout {
            rows: 4
            columns: 2

            Text {text: qsTr("Card number")}
            TextField {
              id: cardNumber
              validator: RegularExpressionValidator  {
                regularExpression: /^\d{16}$/
              }
            }

            Text {text: qsTr("Month")}
            TextField {
              id: month
              validator: RegularExpressionValidator  {
                regularExpression: /^\d{2}$/
              }
            }

            Text {text: qsTr("Year")}
            TextField {
              id: year
              validator: RegularExpressionValidator  {
                regularExpression: /^\d{2}$/
              }
            }

            Text {text: qsTr("CVV / CVC")}
            TextField {
              id: cvvcvc
              echoMode: TextInput.Password
              validator: RegularExpressionValidator  {
                regularExpression: /^\d{3}$/
              }
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: storePageLayout.height

        ColumnLayout {
          id: storePageLayout
          implicitWidth: window.width - 2 * defaultMargin // FIXME: ugly

          Text {
            Layout.preferredWidth: parent.width
            textFormat: TextEdit.MarkdownText
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
            text: qsTr("# Salad Workshop
Are you a developer and want to become an official partner, use the platform to distribute your games and software? That's great, let's get started.
## What to expect
---
### The general procedure for publishing products is regulated as follows:
1. Filling out electronic documents:
      * Information about the legal entity
      * Bank payment information
2. After gaining access to the workshop, start preparing products for release. You need to create a store page, upload a build, and offer an estimated price.
3. Before launching your game and store pages, we will launch the game and check the page build to ensure there are no errors or malicious elements. Verification usually takes 1 to 5 days.
## Information we need
---
### Legal details and name
Accurate legal information about the person or company signing the agreement so that we are qualified to know who you are and who you represent. This is information about your company. To work with our legal entity, it is desirable (to reduce coverage and perform monetary transactions), but not necessary. You can also become a self-employed expert
### Billing Information
Accurate banking information about where the proceeds from the sale of your application are transferred: bank code, bank account number and bank address.
## Rules and restrictions
---
### What can't be distributed using our platform:
* Promoting crime, crime, or terrorism against a group of people based on ethnicity, religion, gender, age, disability, or sexual orientation.
* Images of a sexual nature with real people.
* Adult content that is not labeled as such and has no age rating information.
* Defamatory statements or statements that offend honor and dignity. Content for which you do not have rights.
* Content for which you do not have rights.
* Content that violates the laws of the countries in which it will be distributed.
* Content that is blatantly offensive or intentionally shocking or disgusting to the public.
* Content that is in any way related to the exploitation of minors.
* Applications that are replaced by a user's computer that they don't expect or that cause harm, such as viruses or malware.
* Applications that fraudulently obtain sensitive information (such as login information) or financial data (such as credit card information).
* Video content that is not directly related to the product published on the platform.
* Non-interactive panoramic videos of realistic reality.
* Applications built using technologies that issue or exchange cryptocurrencies or NFTs (non-fungible tokens).
### Allowed types of content
First, we accept games. Non-gaming software may be accepted if it falls into one of the following categories:
* animation and modeling;
* work with sound and video;
* design and illustrations;
* photo processing;
* education and training;
* Finance and accounting;
* tools for players;
## Let's get started
---
Click the \"Continue\" button to proceed to enter your name and contact information.
")
          }

          Button {
            text: qsTr("Continue")
            onClicked: {
              juridicalNameInput.focus = true
              storeStack.currentIndex = storeStack.workshopRegisterCompanyInfoIndex
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: companyInfoForm.height

        ColumnLayout {
          id: companyInfoForm

          implicitWidth: window.width - 2 * defaultMargin

          Button {
            text: qsTr("To introduction")
            onClicked: storeStack.currentIndex = storeStack.workshopIntroductionIndex
          }

          Text {
            Layout.preferredWidth: parent.width
            textFormat: TextEdit.MarkdownText
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
            text: qsTr("# Juridical name

The organization whose name you enter below must be the legal entity that will sign the required license agreements. The company name entered here must match the name on official bank documents and documents submitted to the tax office, or foreign tax documents, if any.

If you do not have a company name and are the sole owner of the content you wish to publish, please enter your full name and postal address in the \"Legal Name\" and \"Street, Building, and Apartment/Office\" fields. If you co-own the game together with other people, you will need to register a legal entity that will own the content and accept payments for it.

The legal name specified here is used internally by the system. If you have a commercial or informal name that you want to use on your store, you can specify it separately when creating your store page.
")}

          Text {
            text: qsTr("JURIDICAL NAME")
          }
          TextField {
            id: juridicalNameInput
            text: company_logic.juridical_name
            onTextChanged: company_logic.juridical_name = text
          }

          Text {
            Layout.preferredWidth: parent.width
            textFormat: TextEdit.MarkdownText
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
            text: qsTr("# Company Form

The legal form of the company must match the one indicated in the documentation of your company. Examples of what should be entered in this field: Limited Liability Company \"League\"; Public Joint Stock Company\"Sberbank of Russia\"; Sole Proprietor. If you are the sole owner of the game, please use \"Sole Proprietor\".
")
          }

          Text {
            text: qsTr("COMPANY FORM")
          }
          TextField {
            text: company_logic.company_form
            onTextChanged: company_logic.company_form = text
          }

          Text {text: qsTr("STREET, BUILDING, APARTMENT / OFFICE NUMBER")}
          TextField {
            text: company_logic.street_house_apartment
            onTextChanged: company_logic.street_house_apartment = text
          }

          Text {text: qsTr("CITY")}
          TextField {
            text: company_logic.city
            onTextChanged: company_logic.city = text
          }

          Text {text: qsTr("REGION")}
          TextField {
            text: company_logic.region
            onTextChanged: company_logic.region = text
          }

          Text {text: qsTr("COUNTRY")}
          TextField {
            text: company_logic.country
            onTextChanged: company_logic.country = text
          }

          Text {text: qsTr("POSTCODE")}
          TextField {
            text: company_logic.postal_code
            onTextChanged: company_logic.postal_code = text
          }

          Text {text: qsTr("EMAIL ADDRESS FOR NOTIFICATIONS")}
          TextField {
            id: companyEmail
            validator: RegularExpressionValidator  {
                regularExpression: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
              }
            text: company_logic.notification_email
            onTextChanged: company_logic.notification_email = text
          }

          Text {
            Layout.preferredWidth: parent.width
            text: qsTr("Click the \"Continue\" button to proceed to enter payment information")
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
          }

          Button {
            enabled: companyEmail.acceptableInput
            text: qsTr("Continue")
            onClicked: {
              bicInput.focus = true
              storeStack.currentIndex = storeStack.workshopRegisterPaymentInfoIndex
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: companyPayInfoForm.height

        ColumnLayout {
          id: companyPayInfoForm

          implicitWidth: window.width - 2 * defaultMargin

          Button {
            text: qsTr("To company information")
            onClicked: storeStack.currentIndex = storeStack.workshopRegisterCompanyInfoIndex
          }

          Text {text: qsTr("BIC / SWIFT BANK CODE")}
          TextField {
            id: bicInput
            text: company_logic.bic
            onTextChanged: company_logic.bic = text
            validator: RegularExpressionValidator  {
              regularExpression: /^\d{9}$/
            }
          }

          Text {text: qsTr("BANK ADDRESS")}
          TextField {
            text: company_logic.bank_address
            onTextChanged: company_logic.bank_address = text
          }

          Text {text: qsTr("BANK ACCOUNT NUMBER")}
          TextField {
          id: accountNumber
            text: company_logic.bank_account_number
            onTextChanged: company_logic.bank_account_number = text
            validator: RegularExpressionValidator  {
                regularExpression: /^\d{20}$/
              }
          }

          Text {
            Layout.preferredWidth: parent.width
            text: qsTr("After clicking on the \"Yes, I want to create a company\" button, a person will be registered in the system who will be able to publish releases. Please note that the information will be immediately sent for consideration. While it is running, you will not be able to publish your products. Please double-check all the information provided.")
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
          }

          Button {
            enabled: bicInput.acceptableInput && accountNumber.acceptableInput
            text: qsTr("Yes, I want to create a company")
            onClicked: company_logic.new()
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: releasesList.contentHeight + releasesListHeader.height + newGamePublishingTools.height + defaultMargin + (unverifiedCompanyWarning.visible ? unverifiedCompanyWarning.height : 0)

        ColumnLayout {
          implicitWidth: window.width - 2 * defaultMargin
          height: parent.height

          Connections {
            target: app_logic

            function onDrafted() {
              storeStack.currentIndex = storeStack.workshopAppControlIndex
            }
          }

          Text {
            id: unverifiedCompanyWarning
            text: qsTr("Until your company information is verified, you cannot create new releases")
            visible: !company_logic.is_drafted_new_button_enabled
            Layout.preferredWidth: parent.width
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
          }

          RowLayout {
            id: newGamePublishingTools

            Text {
              text: qsTr("Select a product to view and edit")
              visible: game_list_model.rowCount() !== 0
            }

            Button {
              text: qsTr("Draft new")
              onClicked: {
                app_logic.draft_new()
                game_list_model.load_personal()
              }
              visible: company_logic.is_drafted_new_button_enabled
            }
          }

          RowLayout {
            id: releasesListHeader

            Text {
              Layout.preferredWidth: 200
              text: qsTr("Title")
            }
            Text {
              Layout.preferredWidth: 100
              text: qsTr("Is approved")
            }
            Text {text: qsTr("Is published")}
          }

          ListView {
            id: releasesList
            Layout.fillHeight: true
            model: game_list_model
            boundsBehavior: Flickable.StopAtBounds

            delegate: RowLayout {
              Text {
                Layout.preferredWidth: 200
                text: title
              }
              Text {
                Layout.preferredWidth: 100
                text: is_approved ? qsTr("Approved") : qsTr("Not approved")
              }
              Text {
                Layout.preferredWidth: 100
                text: is_published ? qsTr("Published") : qsTr("Not published")
              }

              MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                  app_logic.map(id)
                  storeStack.currentIndex = storeStack.workshopAppControlIndex
                }
              }
            }
          }
        }
      }

      Scroll {
        leftPadding: defaultMargin
        bottomPadding: defaultMargin
        contentHeight: appControlPage.height

        ColumnLayout {
          id: appControlPage

          implicitWidth: window.width - 2 * defaultMargin

          Button {
            text: qsTr("To releases list")
            onClicked: storeStack.currentIndex = storeStack.workshopAppsListIndex
          }

          RowLayout {
            TabBar {
              id: appSettingsBar

              width: parent.width

              TabButton {text: qsTr("Common")}
              TabButton {text: qsTr("Descriptions")}
              TabButton {text: qsTr("Materials")}
              TabButton {
                text: qsTr("Builds")
                onClicked: {
                  build_logic.load_platforms()
                  build_list_model.load_for_game(app_logic.id)
                }
              }
            }

            Button {
              text: qsTr("Save")
              onClicked: {
                app_logic.update()
                build_logic.update(app_logic.id)
                game_list_model.load_personal()
              }
            }

            Switch {
              enabled: app_logic.is_approved
              position: app_logic.is_published
              onToggled: {
                app_logic.is_published = position
                app_logic.publish()
              }
              text: qsTr("Is published")
            }
          }

          StackLayout {
            currentIndex: appSettingsBar.currentIndex
            implicitWidth: parent.width

            ColumnLayout {
              Text {text: qsTr("TITLE")}
              TextField {
                text: app_logic.title
                onTextChanged: app_logic.title = text
              }

              CheckBox {
                id: is_coming_soon
                text: qsTr("COMING SOON")
                checked: app_logic.coming_soon
                onClicked: app_logic.coming_soon = checked
              }

              Text {
                text: qsTr("RELEASE DATE")
                visible: !is_coming_soon.checked
              }

              RowLayout {
                id: dateSection

                visible: !is_coming_soon.checked

                ComboBox {
                  model: app_logic.possible_days
                  currentIndex: app_logic.day_index
                  onCurrentIndexChanged: app_logic.day_index = currentIndex
                }

                ComboBox {
                  model: app_logic.possible_months
                  currentIndex: app_logic.month_index
                  onCurrentIndexChanged: app_logic.month_index = currentIndex
                }

                ComboBox {
                  model: app_logic.possible_years
                  currentIndex: app_logic.year_index
                  onCurrentIndexChanged: app_logic.year_index = currentIndex
                }
              }

              Text {text: qsTr("DEVELOPER")}
              TextField {
                text: app_logic.developer
                onTextChanged: app_logic.developer = text
              }

              Text {text: qsTr("PUBLISHER")}
              TextField {
                text: app_logic.publisher
                onTextChanged: app_logic.publisher = text
              }

              Text {text: qsTr("PRICE")}
              TextField {
                text: app_logic.price
                onTextChanged: app_logic.price = text
              }
            }

            ColumnLayout {
              implicitWidth: parent.width

              Text {
                Layout.preferredWidth: parent.width
                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                text: qsTr("Short description ") + shortDescriptionArea.length + "/" + shortDescriptionArea.limit
              }

              Scroll {
                Layout.preferredWidth: parent.width / 2
                Layout.preferredHeight: 125

                TextArea {
                  id: shortDescriptionArea

                  property int limit: 500

                  Layout.preferredWidth: parent.width / 2
                  Layout.preferredHeight: 125

                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere

                  background: Rectangle {
                    color: "lightgray"

                    MouseArea {
                      anchors.fill: parent
                      hoverEnabled: true
                      cursorShape: Qt.IBeamCursor
                    }
                  }

                  text: app_logic.short_description
                  onTextChanged: {
                    if (length > limit) remove(limit, length)
                    app_logic.short_description = text
                  }
                }
              }

              Text {
                Layout.preferredWidth: parent.width
                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                text: "Long description (Markdown supported) " + longDescriptionArea.length + "/" + longDescriptionArea.limit
              }

              Scroll {
                Layout.preferredWidth: parent.width / 2
                Layout.preferredHeight: 350

                TextArea {
                  id: longDescriptionArea

                  property int limit: 2000

                  Layout.preferredWidth: parent.width / 2
                  Layout.preferredHeight: 350

                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere

                  background: Rectangle {
                    color: "lightgray"

                    MouseArea {
                      anchors.fill: parent
                      hoverEnabled: true
                      cursorShape: Qt.IBeamCursor
                    }
                  }

                  text: app_logic.long_description
                  onTextChanged: {
                    if (length > limit) remove(limit, length)
                    app_logic.long_description = text
                  }
                }
              }
            }

            ColumnLayout {
              implicitWidth: parent.width

              RowLayout {
                Platform.FileDialog {
                  id: attach_header_image_file_dialog
                  fileMode: Platform.FileDialog.OpenFile
                  nameFilters: ["Images (*.webp *jpg *png)"]
                  onAccepted: app_logic.header = file
                  folder: StandardPaths.writableLocation(StandardPaths.PicturesLocation)
                }

                Text {text: qsTr("SHOP POSTER (*.webp *jpg *png):")}

                Text {
                  text: app_logic.displayed_header === '' ?
                    (app_logic.server_header === '' ? qsTr('Not provided') :  app_logic.server_header)
                      :
                    app_logic.displayed_header
                }
              }

              RowLayout {
                Button {
                  visible: app_logic.header === ""
                  text: qsTr("Attach")
                  onClicked: attach_header_image_file_dialog.open()
                }
                Button {
                  visible: app_logic.header !== ""
                  text: qsTr("Unpin")
                  onClicked: app_logic.header = ""
                }
              }

              RowLayout {
                Platform.FileDialog {
                  id: attach_capsule_image_file_dialog
                  fileMode: Platform.FileDialog.OpenFile
                  nameFilters: ["Images (*.webp *jpg *png)"]
                  onAccepted: app_logic.capsule = file
                  folder: StandardPaths.writableLocation(StandardPaths.PicturesLocation)
                }

                Text {text: qsTr("LIBRARY POSTER (*.webp *jpg *png):")}

                Text {
                  text: app_logic.displayed_capsule === '' ?
                    (app_logic.server_capsule === '' ? qsTr('Not provided') :  app_logic.server_capsule)
                      :
                    app_logic.displayed_capsule
                }
              }

              RowLayout {
                Button {
                  visible: app_logic.capsule === ""
                  text: qsTr("Attach")
                  onClicked: attach_capsule_image_file_dialog.open()
                }

                Button {
                  visible: app_logic.capsule !== ""
                  text: qsTr("Unpin")
                  onClicked: app_logic.capsule = ""
                }
              }

              RowLayout {
                Platform.FileDialog {
                  id: attach_screenshots_file_dialog
                  fileMode: Platform.FileDialog.OpenFiles
                  nameFilters: ["Images (*.webp *jpg *png)"]
                  onAccepted: app_logic.screenshots = files
                  folder: StandardPaths.writableLocation(StandardPaths.PicturesLocation)
                }

                Text {text: qsTr("SCREENSHOTS (*.webp *jpg *png):")}

                Text {
                  text: app_logic.displayed_screenshots === '' ?
                    (app_logic.server_screenshots === '' ? qsTr('Not provided') :  app_logic.server_screenshots)
                      :
                    app_logic.displayed_screenshots
                }
              }

              RowLayout {
                Button {
                  visible: app_logic.displayed_screenshots === ""
                  text: qsTr("Attach")
                  onClicked: attach_screenshots_file_dialog.open()
                }

                Button {
                  visible: app_logic.displayed_screenshots !== ""
                  text: qsTr("Unpin")
                  onClicked: app_logic.screenshots = []
                }
              }
            }

            ColumnLayout {
               RowLayout {
                Text {
                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                  text: qsTr("Here you can view and create a build of the application for a specific platform")
                }

                Button {
                  text: qsTr("New")
                  onClicked: {
                    build_logic.draft_new(app_logic.id)
                    build_list_model.load_for_game(app_logic.id)
                  }
                }
              }

              StackLayout {
                id: buildsStackLayout
                currentIndex: buildsBar.currentIndex
                implicitWidth: parent.width

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
                    Text {text: "VERSION"}
                    Text {text: "PLATFORM"}
                    Text {text: "CALL"}
                    Text {text: "PARAMS"}
                  }

                  ListView {
                    Layout.fillHeight: true
                    model: build_list_model
                    boundsBehavior: Flickable.StopAtBounds

                    delegate: RowLayout {
                      Text {text: platform_title}
                      Text {text: version}
                      Text {text: call}
                      Text {text: params}

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
                  Button {
                    text: qsTr("To builds list")

                    onClicked: {
                      build_list_model.load_for_game(app_logic.id)
                      buildsStackLayout.currentIndex = buildsStackLayout.buildsListIndex
                    }
                  }

                  Text {text: qsTr("VERSION")}
                  TextField {
                    text: build_logic.version
                    onTextChanged: build_logic.version = text
                  }

                  Text {text: qsTr("CALL")}
                  TextField {
                    text: build_logic.call
                    onTextChanged: build_logic.call = text
                  }

                  Text {text: qsTr("PARAMETERS")}
                  TextField {
                    text: build_logic.params
                    onTextChanged: build_logic.params = text
                  }

                  Text {text: qsTr("PLATFORM")}
                  ComboBox {
                    model: build_logic.displayed_platforms
                    currentIndex: build_logic.selected_platform_index
                    onCurrentIndexChanged: build_logic.selected_platform_index = currentIndex
                  }

                  RowLayout {
                    Platform.FolderDialog {
                      id: attach_project_archive_file_dialog
                      onAccepted: build_logic.project_archive = folder
                    }

                    Text {text: qsTr("DIRECTORY:")}

                    Text {
                      text: build_logic.project_archive
                    }
                  }

                  Button {
                    text: qsTr("Attach")
                    onClicked: attach_project_archive_file_dialog.open()
                  }

                  Text {
                    text: build_logic.displayed_status
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