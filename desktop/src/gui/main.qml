import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt.labs.platform as Platform

ApplicationWindow {
  id: window
  width: 1000
  height: 800
  visible: true
  title: windowTitle
  color: backgroundWindowColor

  property string backgroundWindowColor: "#212834"
  property string highlightedTextColor: "#0079F2"
  property string windowTitle: qsTr("foggie")
  property int defaultMargin: 8

  menuBar: MenuBar {
  }

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
      property int storeDetailedGameIndex: storeGamesIndex + 1

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

        anchors.fill: parent
        anchors.margins: defaultMargin

        boundsBehavior: Flickable.StopAtBounds

        property int capsuleImageWidth: 12 * 10
        property int capsuleImageHeight: 17 * 10

        cellWidth: capsuleImageWidth + defaultMargin * 2
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
        ColumnLayout {
          anchors.fill: parent
          anchors.margins: defaultMargin

          Link {
            message: qsTr("To the store")

            function handler() {
              game_list_model.load_store()
              storeStackLayout.currentIndex = storeStackLayout.storeGamesIndex
            }
          }

          Header {
            text: store_detailed_logic.title
            Layout.preferredWidth: parent.width
            wrapMode: TextEdit.WrapAtWordBoundaryOrAnywhere
          }

          Indent {}

          SwipeView {
	          id: game_screenshots_swipe_view

	          Layout.preferredWidth: 500
	          Layout.preferredHeight: width * 9 / 16

	          clip: true

	          Repeater {
	            model: 6

	            Image {
	              source: "../../resources/images/elden-ring.webp"
	              mipmap: true

	              MouseArea {
                  id: image_mouse_area
                  anchors.fill: parent
                  hoverEnabled: true

                  RowLayout {
                    anchors.fill: parent

                    Rectangle {
                      Layout.fillHeight: true
                      Layout.preferredWidth: 40
                      visible: image_mouse_area.containsMouse

                      Image {
                        width: parent.width - 2 * defaultMargin
                        height: width
                        anchors.centerIn: parent
                        source: "../../resources/icons/left_arrow.png"

                        MouseArea {
                          anchors.fill: parent
                          enabled: game_screenshots_swipe_view.currentIndex > 0
                          cursorShape: Qt.PointingHandCursor
                          hoverEnabled: true
                          onClicked: game_screenshots_swipe_view.decrementCurrentIndex()
                        }
                      }

                      gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: -2.0; color: "black" }
                        GradientStop { position: 1.0; color: "transparent" }
                      }
                    }

                    Item {Layout.fillWidth: true}

                    Rectangle {
                      Layout.fillHeight: true
                      Layout.preferredWidth: 40
                      visible: image_mouse_area.containsMouse

                      Image {
                        width: parent.width - 2 * defaultMargin
                        height: width
                        anchors.centerIn: parent
                        source: "../../resources/icons/right_arrow.png"

                        MouseArea {
                          anchors.fill: parent
                          enabled: game_screenshots_swipe_view.currentIndex < game_screenshots_swipe_view.count - 1
                          cursorShape: Qt.PointingHandCursor
                          hoverEnabled: true
                          onClicked: game_screenshots_swipe_view.incrementCurrentIndex()
                        }
                      }

                      gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: "transparent" }
                        GradientStop { position: 3.0; color: "black" }
                      }
                    }
                  }
                }
	            }
	          }
	        }

	        Indent {}

	        ColumnLayout {
            id: edition

            Rectangle {
              id: editionBackground
              anchors.fill: parent
              radius: defaultMargin
              color: "#2E3E4B"
            }

            SubHeader {
              text: qsTr("Buy ") + store_detailed_logic.title
              Layout.preferredWidth: edition.width
            }

            RowLayout {
              Item {
                Layout.fillWidth: true
              }

              Price {
                text: store_detailed_logic.price + "$"
              }

              ActionButton {
                notHoveredColor: "#008E31"
                hoveredColor: "#00BC3E"
                text: qsTr("Add to cart")
              }
            }
          }
        }
      }
    }
  }
}