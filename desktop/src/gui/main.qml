import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 2.15
import QtQuick.Controls 2.15
import QtMultimedia
import Qt.labs.platform as Platform

Window {
  property int defaultMargin: 8
  property int doubleDefaultMargin: defaultMargin * 2
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
				  current_user_logic.map()
				  wallet_logic.map()
					mainStack.currentIndex = mainStack.storeIndex
				}

		    function onLogin() {
				  current_user_logic.map()
				  wallet_logic.map()
					mainStack.currentIndex = mainStack.storeIndex
		    }
			}

      ColumnLayout {
        id: signInForm

        anchors.centerIn: parent

        FormInputLabel {
          color: highlightedTextColor
          content: qsTr("ВОЙТИ, ИСПОЛЬЗУЯ ИМЯ АККАУНТА")
        }
        FormInput {
          id: signInAccountNameInput
          Layout.bottomMargin: doubleDefaultMargin
          focus: true
          text: auth_logic.account_name
          onTextChanged: auth_logic.account_name = text
        }

        FormInputLabel {content: qsTr("ПАРОЛЬ")}
        FormInput {
          Layout.bottomMargin: doubleDefaultMargin
          echoMode: TextInput.Password
          text: auth_logic.password
          onTextChanged: auth_logic.password = text
        }

        ActionButton {
          Layout.alignment: Qt.AlignHCenter
          Layout.bottomMargin: doubleDefaultMargin
          Layout.preferredWidth: 300
          Layout.preferredHeight: 40
          text: qsTr("Войти")
          function handler() {
            auth_logic.sign_in()
          }
        }

        RowLayout {
          Layout.alignment: Qt.AlignHCenter

          Span {content: qsTr("Нужен аккаунт?")}

          Link {
            content: qsTr("Создайте бесплатный аккаунт")

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

        FormInputLabel {content: qsTr("АДРЕС ЭЛЕКТРОННОЙ ПОЧТЫ")}
        FormInput {
          id: signUpEmailInput
          Layout.bottomMargin: doubleDefaultMargin
          text: auth_logic.email
          onTextChanged: auth_logic.email = text
        }

        FormInputLabel {content: qsTr("ИМЯ АККАУНТА")}
        FormInput {
          Layout.bottomMargin: doubleDefaultMargin
          text: auth_logic.account_name
          onTextChanged: auth_logic.account_name = text
        }

        FormInputLabel {content: qsTr("ПАРОЛЬ")}
        FormInput {
          Layout.bottomMargin: doubleDefaultMargin
          echoMode: TextInput.Password
          text: auth_logic.password
          onTextChanged: auth_logic.password = text
        }

        ActionButton {
          Layout.alignment: Qt.AlignHCenter
          Layout.bottomMargin: doubleDefaultMargin
          Layout.preferredWidth: 300
          Layout.preferredHeight: 40
          text: qsTr("Зарегистрироваться")

          function handler() {
            auth_logic.sign_up()
          }
        }

        RowLayout {
          Layout.alignment: Qt.AlignHCenter

          Span {content: qsTr("Уже есть аккаунт?")}

          Link {
            content: qsTr("Войти в существующий аккаунт")

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
          text: qsTr("МАГАЗИН")
          onClicked: {
            game_list_model.load_store()
            storeStack.currentIndex = storeStack.storeIndex
          }
        }

        MenuButton {
          text: qsTr("БИБЛИОТЕКА")
          onClicked: {
            game_list_model.load_library()
            storeStack.currentIndex = storeStack.libraryIndex
          }
        }

        MenuButton {
          text: qsTr("МАСТЕРСКАЯ")
          onClicked: {
            storeStack.checkCompanyRegistration()
          }
        }

        Item {Layout.fillWidth: true}

        Rectangle {
		      Layout.preferredWidth: userAccountName.contentWidth + 32 + defaultMargin * 3 + userBalance.contentWidth
		      Layout.preferredHeight: 32
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
              id: userAccountName
              content: current_user_logic.displayed_name.slice(0, 15) + (current_user_logic.displayed_name.length > 15 ? "..." : "")
              color: "#64BCEF"
            }

            Span {
              id: userBalance
              content: wallet_logic.balance + " руб."
              Layout.rightMargin: defaultMargin
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

        Connections {
          target: auth_logic

          function onRegistered() {
            wallet_logic.map()
            game_list_model.load_store()
          }

          function onLogin() {
            wallet_logic.map()
            game_list_model.load_store()
          }

          function onLogout() {
            authStack.currentIndex = authStack.signInFormIndex
            mainStack.currentIndex = mainStack.authorizationIndex
            storeStack.currentIndex = storeStack.storeIndex
          }
        }

        Scroll {
          contentHeight: gamesList.contentHeight + 2 * defaultMargin

          Item {
            width: layoutWidth - defaultMargin
            height: parent.height
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              anchors.fill: parent

              ListView {
                id: gamesList
                Layout.fillWidth: true
                Layout.fillHeight: true
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
                          store_detailed_logic.map(id)
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
                content: qsTr("To the store")

                function handler() {
                  game_list_model.load_store()
                  storeStack.currentIndex = storeStack.storeIndex
                }
              }

              Indent {}

              Header {text: "# " + store_detailed_logic.title}

              RowLayout {
                SwipeView {
                  id: game_screenshots_swipe_view

                  Layout.preferredWidth: 700
                  Layout.preferredHeight: width * 9 / 16

                  clip: true

                  Connections {
                    target: store_detailed_logic

                    function onLoaded() {
                      var component = Qt.createComponent("Screenshot.qml")
                      var game_id = store_detailed_logic.id
                      var fileNames = store_detailed_logic.screenshots
                      for (var i = 0; i < fileNames.length; i++) {
                        var imageUrl = `http://127.0.0.1:8000/api/v1/games/${game_id}/screenshots/?filename=${fileNames[i]}`
                        var image = component.createObject(game_screenshots_swipe_view, {source: imageUrl})
                        game_screenshots_swipe_view.addItem(image)
                      }
                    }
                  }
                }

                Text {
                  Layout.alignment: Qt.AlignTop
                  Layout.preferredWidth: layoutWidth - game_screenshots_swipe_view.width - defaultMargin
                  color: "#ddd"
                  wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                  text: `<p align='justify'>${store_detailed_logic.short_description}</p>`
                }
              }

              Indent {}

              Rectangle {
                width: game_screenshots_swipe_view.width
                height: 56
                radius: defaultMargin / 2
                color: "#586776"

                RowLayout {
                  visible: store_detailed_logic.location === 0
                  anchors.fill: parent
                  anchors.margins: defaultMargin

                  Text {
                    textFormat: TextEdit.MarkdownText
                    color: "#ddd"
                    text: "## Купить " + store_detailed_logic.title
                  }

                  Item {Layout.fillWidth: true}

                  Text {
                    textFormat: TextEdit.MarkdownText
                    color: "#00E589"
                    text: "## " + store_detailed_logic.price + "$"
                  }

                  BuyButton {
                    text: "В корзину"
                    function handler() {
                      cart_logic.add(store_detailed_logic.id)
                      store_detailed_logic.location = 2
                    }
                  }
                }

                Text {
                  textFormat: TextEdit.MarkdownText
                  anchors.fill: parent
                  anchors.margins: defaultMargin
                  text: "## Уже в вашей библиотеке"
                  color: "white"
                  visible: store_detailed_logic.location === 1
                }

                Text {
                  textFormat: TextEdit.MarkdownText
                  anchors.fill: parent
                  anchors.margins: defaultMargin
                  text: "## Уже в вашей корзине"
                  color: "white"
                  visible: store_detailed_logic.location === 2
                }
              }

              Indent {}

              Text {
                textFormat: TextEdit.MarkdownText
                Layout.preferredWidth: game_screenshots_swipe_view.width
                color: "#ddd"
                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                text: store_detailed_logic.long_description
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

              Button {
                visible: library_detailed_logic.app_status === 0
                text: qsTr("Install")
                onClicked:  library_detailed_logic.download()
              }

              Button {
                visible: library_detailed_logic.app_status === 1
                text: qsTr("Launch")
                onClicked: library_detailed_logic.launch()
              }

              Button {
                visible: library_detailed_logic.app_status === 2
                text: library_detailed_logic.loading_progress
              }

              Button {
                visible: library_detailed_logic.app_status === 3
                text: qsTr("Stop")
                onClicked: library_detailed_logic.shutdown()
              }

              Text {
                visible: library_detailed_logic.app_status === 4
                text: "Not available for your platform"
                color: "white"
              }
            }
          }
        }

        Scroll {
          contentHeight: profilePage.height + 2 * defaultMargin

          Item {
            width: layoutWidth
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: profilePage
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
                    cart_logic.pay()
                    game_list_model.load_cart()
                    game_list_model.recount_total_cost()
                    wallet_logic.map()
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
                        store_detailed_logic.map(id)
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

            RowLayout {
              ColumnLayout {
                id: walletPage

                Header {
                  Layout.bottomMargin: 2 * defaultMargin
                  text: "# Пополнить баланс"
                }

                BalanceAddSection {
                  content: "Добавить 50 руб."
                  amount: 50
                }
                BalanceAddSection {content: "Добавить 100 руб."}
                BalanceAddSection {content: "Добавить 300 руб."}
                BalanceAddSection {content: "Добавить 500 руб."}
                BalanceAddSection {content: "Добавить 1000 руб."}
                BalanceAddSection {content: "Добавить 3000 руб."}
                BalanceAddSection {content: "Добавить 5000 руб."}
              }

              Header {
                Layout.leftMargin: 2 * defaultMargin
                Layout.topMargin: 8 * defaultMargin
                Layout.alignment: Qt.AlignTop
                text: "# Остаток средств: " + wallet_logic.balance + " руб."
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
                  content: qsTr("To wallet")

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
                    wallet_logic.top_up(selectedValue)
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

&nbsp;
### Вы разработчик и хотите стать нашим партнером, использовать нашу платформу для распространения своих игр и программного обеспечения? Это здорово, давайте начнем.

&nbsp;

<h2 style=\"color:#64BCEF\">Чего ожидать</h2>
&nbsp;

---
### Общая процедура публикации продуктов состоит в следующем:
### 1. Заполните электронные документы:
###     * Информация о юридическом лице
###     * Банковская платежная информация
### 2. Получив доступ к Workshop, начните подготовку продукта к выпуску. Вам нужно будет создать страницу магазина, загрузить сборку и ввести желаемую цену.
### 3. Перед окончательным запуском вашей сборки игры и страницы магазина мы запустим игру и проверим страницу, чтобы убедиться в отсутствии ошибок или вредоносных элементов. Проверка обычно занимает от 1 до 5 дней.

&nbsp;

<h2 style=\"color:#64BCEF\">Информация, которая нам понадобится</h2>
&nbsp;

---
### * Юридические данные и название

### Точная юридическая информация о лице или компании, подписавших соглашение, чтобы мы понимали, кто вы и кого представляете. Это информация о вашей компании. Для работы с нами юридическое лицо желательно (для упрощения налогообложения и совершения денежных операций), но необязательно. Вы также можете представлять индивидуального предпринимателя

&nbsp;
### * Платежная информация

### Точная банковская информация о том, куда перевести выручку от продажи вашего приложения: код банка, номер банковского счета и адрес банка.

&nbsp;

<h2 style=\"color:#64BCEF\">Правила и ограничения</h2>
&nbsp;

---
### Что нельзя распространять с помощью нашей платформы:
### * Пропаганда ненависти, насилия или дискриминации в отношении групп людей по признаку этнической принадлежности, религии, пола, возраста, инвалидности или сексуальной ориентации.
### * Изображения сексуального характера с реальными людьми.
### * Контент для взрослых, который не помечен как таковой и не содержит информации о возрастном рейтинге.
### * Клеветнические высказывания или высказывания, оскорбляющие честь и достоинство. Контент, на который у вас нет прав.
### * Контент, на который у вас нет прав.
### * Контент, нарушающий законы стран, в которых он будет распространяться.
### * Контент, который является откровенно оскорбительным или намеренно шокирует или вызывает отвращение у публики.
### * Контент, который каким-либо образом связан с эксплуатацией несовершеннолетних.
### * Приложения, которые изменяют компьютер пользователя неожиданным для него образом или причиняют вред, например вирусы или вредоносное ПО.
### * Приложения, которые пытаются обманным путем получить конфиденциальную информацию (например, данные для входа) или финансовые данные (например, информацию о кредитной карте).
### * Видеоконтент, не имеющий прямого отношения к продукту, выпущенному на платформе.
### * Неинтерактивные панорамные видеоролики виртуальной реальности.
### * Приложения, созданные с использованием технологии блокчейн, которые выпускают или обменивают криптовалюты или NFT (невзаимозаменяемые токены).

&nbsp;
### Разрешенные типы контента:
### Во-первых, мы принимаем игры. Неигровое программное обеспечение может быть принято, если оно относится к одной из следующих категорий:
### * анимация и моделирование;
### * работа со звуком и видео;
### * дизайн и иллюстрации;
### * обработка фото;
### * образование и обучение;
### * Финансы и учет;
### * инструменты для игроков;

&nbsp;

<h2 style=\"color:#64BCEF\">Давайте приступим</h2>
&nbsp;

---
### Нажмите кнопку «Продолжить», чтобы перейти к вводу вашего официального имени и контактной информации.
"}
              Text{
                Layout.preferredWidth: layoutWidth - 2 * defaultMargin
                textFormat: TextEdit.MarkdownText
                text: introductionContent.text
                color: "#ddd"
                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
              }

              NeutralButton {
                text: qsTr("Продолжить")
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
                content: qsTr("К введению")

                function handler() {
                  juridicalNameInput.focus = true
                  storeStack.currentIndex = storeStack.workshopIntroductionIndex
                }
              }

              Indent {}

              Rectangle {
                width: layoutWidth - 2 * defaultMargin
                height: 312
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
                      property string text: "<h1 style=\"color:white\">Юридическое имя</h1>

### Организация, название которой вы введете ниже, должна быть юридическим лицом, которое подпишет необходимые лицензионные соглашения. Введенное здесь название компании должно совпадать с названием в официальных банковских документах и документах, предоставленных в налоговую инспекцию, или иностранных налоговых документах, если таковые имеются.

### Если у вас нет названия компании и вы являетесь единственным владельцем контента, который вы хотите опубликовать, укажите свое полное имя и почтовый адрес в полях \"Юридическое название\" и \"Улица, дом и квартира/офис Числовое поле. Если вы являетесь совладельцем игры вместе с другими людьми, вам потребуется зарегистрировать юридическое лицо, которое будет владеть контентом и принимать за него платежи.

### Указанное здесь юридическое имя используется внутри системы. Если у вас есть коммерческое или неофициальное имя, которое вы хотите использовать в своем магазине, вы можете указать его отдельно при создании страницы своего магазина.
"}
                    Text {
                      Layout.preferredWidth: layoutWidth - 4 * defaultMargin
                      textFormat: TextEdit.MarkdownText
                      text: legalNameContent.text
                      color: "orange"
                      wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                      Layout.bottomMargin: defaultMargin
                    }

                    FormInputLabel {
                      content: qsTr("ЮРИДИЧЕСКОЕ ИМЯ")
                    }
                    FormInput {
                      id: juridicalNameInput
                      focus: true
                      Layout.preferredWidth: 308
                      text: company_logic.juridical_name
                      onTextChanged: company_logic.juridical_name = text
                    }
                  }
                }
              }

              Indent {}

              Rectangle {
                width: layoutWidth - 2 * defaultMargin
                height: 190
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
                      property string text: "<h1 style=\"color:white\">Форма компании</h1>

### Организационно-правовая форма компании должна соответствовать той, что указана в документации вашей компании. Примеры того, что следует вводить в это поле: Общество с ограниченной ответственностью \"Лига\"; Публичное акционерное общество \"Сбербанк России\"; Индивидуальный предприниматель. Если вы являетесь единственным владельцем игры, используйте \"Индивидуальный предприниматель\".
"}
                    Text {
                      Layout.preferredWidth: layoutWidth - 3 * defaultMargin
                      textFormat: TextEdit.MarkdownText
                      text: companyFormContent.text
                      color: "orange"
                      wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    }

                    FormInputLabel {
                      content: qsTr("ФОРМА КОМПАНИИ")
                    }
                    FormInput {
                      text: company_logic.company_form
                      Layout.preferredWidth: 308
                      onTextChanged: company_logic.company_form = text
                    }
                  }
                }
              }

              Indent {}

              FormInputLabel {
                content: qsTr("УЛИЦА, ДОМ, НОМЕР КВАРТИРЫ / ОФИСА")
              }
              FormInput {
                text: company_logic.street_house_apartment
                Layout.preferredWidth: 308
                onTextChanged: company_logic.street_house_apartment = text
              }

              Indent {}

              FormInputLabel {
                content: qsTr("ГОРОД")
              }
              FormInput {
                text: company_logic.city
                Layout.preferredWidth: 308
                onTextChanged: company_logic.city = text
              }

              Indent {}

              FormInputLabel {
                content: qsTr("РЕГИОН / ОБЛАСТЬ")
              }
              FormInput {
                text: company_logic.region
                Layout.preferredWidth: 308
                onTextChanged: company_logic.region = text
              }

              Indent {}

              FormInputLabel {
                content: qsTr("СТРАНА")
              }
              FormInput {
                text: company_logic.country
                Layout.preferredWidth: 308
                onTextChanged: company_logic.country = text
              }

              Indent {}

              FormInputLabel {
                content: qsTr("ПОЧТОВЫЙ ИНДЕКС")
              }
              FormInput {
                text: company_logic.postal_code
                Layout.preferredWidth: 308
                onTextChanged: company_logic.postal_code = text
              }

              Indent {}

              FormInputLabel {
                  content: qsTr("ЭЛЕКТРОННЫЙ АДРЕС ДЛЯ УВЕДОМЛЕНИЙ")
              }
              FormInput {
                text: company_logic.notification_email
                Layout.preferredWidth: 308
                onTextChanged: company_logic.notification_email = text
              }

              Indent {}

              Text{
                Layout.preferredWidth: layoutWidth - 2 * defaultMargin
                textFormat: TextEdit.MarkdownText
                text: "### Нажмите кнопку «Продолжить», чтобы перейти к вводу платежной информации"
                color: "#ddd"
                wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
              }

              NeutralButton {
                text: qsTr("Продолжить")
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
                content: qsTr("К информации о компании")

                function handler() {
                  juridicalNameInput.focus = true
                  storeStack.currentIndex = storeStack.workshopRegisterCompanyInfoIndex
                }
              }

              Indent {}

              FormInputLabel {
                content: qsTr("БИК")
              }
              FormInput {
                id: bicInput
                focus: true
                text: company_logic.bic
                onTextChanged: company_logic.bic = text
              }

              Indent {}

              FormInputLabel {
                content: qsTr("АДРЕС БАНКА")
              }
              FormInput {
                text: company_logic.bank_address
                onTextChanged: company_logic.bank_address = text
              }

              Indent {}

              FormInputLabel {
                content: qsTr("БАНКОВСКИЙ НОМЕР СЧЕТА")
              }
              FormInput {
                text: company_logic.bank_account_number
                onTextChanged: company_logic.bank_account_number = text
              }

              Indent {}

              ActionButton {
                text: qsTr("Создать")
                function handler() {
                  company_logic.new()
                }
              }

              Indent {}
            }
          }
        }

        Scroll {
          contentHeight: boo.contentHeight + 2 * defaultMargin

          Item {
            width: layoutWidth - defaultMargin
            height: parent.height
            anchors.horizontalCenter: parent.horizontalCenter

            ColumnLayout {
              id: releasesAppsList

              anchors.fill: parent

              Connections {
                target: app_logic

                function onDrafted() {
                  storeStack.currentIndex = storeStack.workshopAppControlIndex
                }
              }

              Regular {
                content: qsTr("Пока информация о вашей компании не проверена, Вы не можете создавать новые релизы")
                color: "orange"
                visible: !company_logic.is_drafted_new_button_enabled
              }

              RowLayout {
                Regular {
                  content: "Выберите продукт для просмотра и редактирования"
                }

                Item {Layout.fillWidth: true}

                ActionButton {
                  Layout.rightMargin: defaultMargin
                  text: qsTr("Создать")
                  function handler() {
                    app_logic.draft_new()
                    game_list_model.load_personal()
                  }
                  visible: company_logic.is_drafted_new_button_enabled
                }
              }

              RowLayout {
                FormInputLabel {
                  Layout.preferredWidth: 250
                  content: "Название"
                }
                FormInputLabel {content: "Одобрено"}
                FormInputLabel {content: "Опубликовано"}
              }

              ListView {
                id: boo
                Layout.fillHeight: true
                model: game_list_model
                spacing: defaultMargin
                boundsBehavior: Flickable.StopAtBounds

                delegate: RowLayout {
                  Rectangle {
                    id: releaseRowBack
                    anchors.fill: parent
                    color: "transparent"
                    radius: defaultMargin / 2
                    opacity: 0.2
                  }

                  FormInputLabel {
                    content: title
                    Layout.preferredWidth: 272
                  }

                  FormInputLabel {
                    color: is_approved ? "#ddd" : "red"
                    Layout.preferredWidth: 88
                    content: is_approved ? qsTr("Да") : qsTr("Нет")
                  }

                  FormInputLabel {
                    color: is_published ? "orange" : "#ccc"
                    Layout.preferredWidth: 50
                    content: is_published ? qsTr("Да") : qsTr("Нет")
                  }

                  MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    hoverEnabled: true
                    onEntered: releaseRowBack.color = "gray"
                    onExited: releaseRowBack.color = "transparent"
                    onClicked: {
                      app_logic.map(id)
                      storeStack.currentIndex = storeStack.workshopAppControlIndex
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

              Link {
                content: qsTr("К списку приложений")

                function handler() {
                  storeStack.currentIndex = storeStack.workshopAppsListIndex
                }
              }

              RowLayout {
                NeutralButton {
                  text: qsTr("Основное")
                  function handler() {
                    gameControlStackLayout.currentIndex = gameControlStackLayout.basicInfoPageIndex
                  }
                }

                NeutralButton {
                  text: qsTr("Описания")
                  function handler() {
                    gameControlStackLayout.currentIndex = gameControlStackLayout.descriptionPageIndex
                  }
                }

                NeutralButton {
                  text: qsTr("Материалы")
                  function handler() {
                    gameControlStackLayout.currentIndex = gameControlStackLayout.assetsPageIndex
                  }
                }

                NeutralButton {
                  text: qsTr("Сборки")
                  function handler() {
                    build_logic.load_platforms()
                    build_list_model.load_for_game(app_logic.id)
                    gameControlStackLayout.currentIndex = gameControlStackLayout.buildsPageIndex
                  }
                }

                Item {Layout.fillWidth: true}

                ActionButton {
                  text: qsTr("Сохранить")
                  function handler() {
                    app_logic.update()
                    build_logic.update(app_logic.id)
                    game_list_model.load_personal()
                  }
                }

                Switcher {
                  enabled: app_logic.is_approved
                  position: app_logic.is_published
                  onToggled: app_logic.is_published = position
                  text: qsTr("Опубликовано")
                  onClicked: app_logic.publish()
                  Layout.rightMargin: defaultMargin
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
                    content: qsTr("НАЗВАНИЕ")
                  }
                  FormInput {
                    text: app_logic.title
                    onTextChanged: app_logic.title = text
                  }

                  Checking {
                    id: is_coming_soon
                    text: qsTr("СКОРО")
                    checked: app_logic.coming_soon
                    onClicked: app_logic.coming_soon = checked
                  }

                  FormInputLabel {
                    content: qsTr("ДАТА ВЫХОДА")
                    visible: !is_coming_soon.checked
                  }

                  RowLayout {
                    id: dateSection

                    visible: !is_coming_soon.checked

                    property int comboWidth: 97

                    Combo {
                      implicitWidth: parent.comboWidth
                      model: app_logic.possible_days
                      currentIndex: app_logic.day_index
                      onCurrentIndexChanged: app_logic.day_index = currentIndex
                    }

                    Combo {
                      implicitWidth: parent.comboWidth
                      model: app_logic.possible_months
                      currentIndex: app_logic.month_index
                      onCurrentIndexChanged: release_logic.month_index = currentIndex
                    }

                    Combo {
                      implicitWidth: parent.comboWidth
                      model: app_logic.possible_years
                      currentIndex: app_logic.year_index
                      onCurrentIndexChanged: app_logic.year_index = currentIndex
                    }
                  }

                  Indent {
                    visible: !is_coming_soon.checked
                  }

                  FormInputLabel {content: qsTr("РАЗРАБОТЧИК")}
                  FormInput {
                    text: app_logic.developer
                    onTextChanged: app_logic.developer = text
                  }

                  FormInputLabel {content: qsTr("ИЗДАТЕЛЬ")}
                  FormInput {
                    text: app_logic.publisher
                    onTextChanged: app_logic.publisher = text
                  }

                  FormInputLabel {
                    content: qsTr("ЦЕНА")
                  }
                  FormInput {
                    text: app_logic.price
                    onTextChanged: app_logic.price = text
                  }
                }

                ColumnLayout {
                  Regular {
                    color: "#64BCEF"
                    Layout.preferredWidth: layoutWidth
                    wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
                    content: "Развернутое описание поддерживает Markdown"
                  }

                  Indent {}

                  RowLayout {
                    FormInputLabel {
                      content: "КРАТКОЕ ОПИСАНИЕ"
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
                    FormInputLabel {
                      content: "РАЗВЕРНУТОЕ ОПИСАНИЕ"
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

                    FormInputLabel {
                      content: qsTr("ПОСТЕР ДЛЯ МАГАЗИНА (*.webp):")
                    }

                    FormInputLabel {
                      content: app_logic.displayed_header
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.header !== ""
                      text: qsTr("Unpin")
                      function handler() {
                       app_logic.header = ""
                      }
                    }
                  }

                  ActionButton {
                    text: qsTr("Прикрепить")
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

                    FormInputLabel {
                      content: qsTr("ПОСТЕР ДЛЯ БИБЛИОТЕКИ (*.webp):")
                    }

                    FormInputLabel {
                      content: app_logic.displayed_capsule
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.capsule !== ""
                      text: qsTr("Открепить")
                      function handler() {
                       app_logic.capsule = ""
                      }
                    }
                  }

                  ActionButton {
                    text: qsTr("Прикрепить")
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

                    FormInputLabel {
                      content: qsTr("СКРИНШОТЫ (*webp):")
                    }

                    FormInputLabel {
                      content: app_logic.displayed_screenshots
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.displayed_screenshots !== ""
                      text: qsTr("Открепить")
                      function handler() {
                       app_logic.screenshots = []
                      }
                    }
                  }

                  ActionButton {
                    text: qsTr("Прикрепить")
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

                    FormInputLabel {
                      content: qsTr("ТРЕЙЛЕРЫ (*.webm *.mp4):")
                    }

                    FormInputLabel {
                      content: app_logic.displayed_trailers
                      color: "orange"
                    }

                    NeutralButton {
                      visible: app_logic.displayed_trailers !== ""
                      text: qsTr("Открепить")
                      function handler() {
                       app_logic.trailers = []
                      }
                    }
                  }

                  ActionButton {
                    text: qsTr("Прикрепить")
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
                      Regular {
                        color: "#64BCEF"
                        content: "Здесь вы можете просмотреть и создать сборку приложения для конкретной платформы"
                      }

                      Item {Layout.fillWidth: true}

                      ActionButton {
                        text: qsTr("Создать")
                        Layout.rightMargin: doubleDefaultMargin
                        function handler() {
                          build_logic.draft_new(app_logic.id)
                          build_list_model.load_for_game(app_logic.id)
                        }
                      }
                    }

                    RowLayout {
                      FormInputLabel {
                        Layout.preferredWidth: 140
                        content: "ПЛАТФОРМА"
                      }
                      FormInputLabel {
                        Layout.preferredWidth: 100
                        content: "ВЕРСИЯ"
                      }
                      FormInputLabel {
                        Layout.preferredWidth: 190
                        content: "ВЫПОЛНИТЬ"
                      }
                      FormInputLabel {
                        Layout.preferredWidth: 100
                        content: "ПАРАМЕТРЫ"
                      }
                    }

                    ListView {
                      Layout.fillHeight: true
                      model: build_list_model
                      spacing: defaultMargin
                      boundsBehavior: Flickable.StopAtBounds

                      delegate: RowLayout {
                        Rectangle {
                          id: buildRowBack
                          anchors.fill: parent
                          color: "transparent"
                          radius: defaultMargin / 2
                          opacity: 0.2
                        }

                        Regular {
                          content: platform_title
                          Layout.preferredWidth: 142
                          font.underline: true
                        }

                        Regular {
                          Layout.preferredWidth: 94
                          content: version
                        }

                        Regular {
                          Layout.preferredWidth: 190
                          content: call
                        }

                        Regular {
                          Layout.preferredWidth: 80
                          content: params
                        }

                        MouseArea {
                          anchors.fill: parent
                          cursorShape: Qt.PointingHandCursor
                          hoverEnabled: true
                          onEntered: buildRowBack.color = "gray"
                          onExited: buildRowBack.color = "transparent"
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
                      content: qsTr("К списку сборок")

                      function handler() {
                        build_list_model.load_for_game(app_logic.id)
                        buildsStackLayout.currentIndex = buildsStackLayout.buildsListIndex
                      }
                    }

                    Indent {}

                    FormInputLabel {content: qsTr("ВЕРСИЯ")}
                    FormInput {
                      text: build_logic.version
                      onTextChanged: build_logic.version = text
                    }

                    Indent {}

                    FormInputLabel {content: qsTr("ИСПОЛНЯЕМЫЙ ФАЙЛ")}
                    FormInput {
                      text: build_logic.call
                      onTextChanged: build_logic.call = text
                    }

                    Indent {}

                    FormInputLabel {content: qsTr("ПАРАМЕТРЫ")}
                    FormInput {
                      text: build_logic.params
                      onTextChanged: build_logic.params = text
                    }

                    Indent {}

                    FormInputLabel {content: qsTr("ПЛАТФОРМА")}
                    Combo {
                      model: build_logic.displayed_platforms
                      currentIndex: build_logic.selected_platform_index
                      onCurrentIndexChanged: build_logic.selected_platform_index = currentIndex
                    }

                    Indent {}

                    RowLayout {
                      Platform.FolderDialog {
                        id: attach_project_archive_file_dialog
                        onAccepted: build_logic.project_archive = folder
                      }

                      FormInputLabel {
                        content: qsTr("ДИРЕКТОРИЯ:")
                      }

                      FormInputLabel {
                        content: build_logic.project_archive
                        color: "orange"
                      }
                    }

                    ActionButton {
                      text: qsTr("Выбрать")
                      function handler() {
                       attach_project_archive_file_dialog.open()
                      }
                    }

                    FormInputLabel {
                      content: build_logic.displayed_status
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