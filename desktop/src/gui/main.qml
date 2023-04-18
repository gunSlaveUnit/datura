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
  title: qsTr("foggie")
  color: "#0c0c0c"

  property int defaultMargin: 8
  property int textFieldWidth: 240

  minimumWidth: signUpForm.implicitWidth + 2 * defaultMargin
  minimumHeight: signUpForm.implicitHeight + 2 * defaultMargin

  StackLayout {
    id: mainStackLayout

		anchors.fill: parent

    property int authorizationSectionIndex: 0
    property int storeSectionIndex: 1

    StackLayout {
			id: authStackLayout

			Connections {
				target: auth_logic

				function onRegistered() {
					mainStackLayout.currentIndex = mainStackLayout.storeSectionIndex
				}

		    function onLogin() {
					mainStackLayout.currentIndex = mainStackLayout.storeSectionIndex
		    }
			}

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
	            onClicked: {
	              auth_logic.reset()
	              authStackLayout.currentIndex = authStackLayout.signUpFormIndex
	            }
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
	            onClicked: {
	              auth_logic.reset()
	              authStackLayout.currentIndex = authStackLayout.signInFormIndex
              }
	          }
	        }
				}
			}
		}

		ColumnLayout {
			RowLayout {
				Button {
          text: qsTr("<")
          onClicked: navigation_logic.back()
          enabled: navigation_logic.current_index > 0
        }

        Button {
          text: qsTr(">")
          onClicked: navigation_logic.forward()
          enabled: navigation_logic.current_index < navigation_logic.current_history_length - 1
        }

        Button {
		      text: qsTr("Store")
		      onClicked: {
		        navigation_logic.add(storeStackLayout.storeGamesIndex)
		        store_game_list_model.load_store()
		        storeStackLayout.currentIndex = storeStackLayout.storeGamesIndex
	        }
		    }

				Button {
		      text: qsTr("Library")
		      onClicked: {
		        navigation_logic.add(storeStackLayout.libraryGamesIndex)
		        library_game_list_model.load_library()
		        storeStackLayout.currentIndex = storeStackLayout.libraryGamesIndex
	        }
		    }

		    Button {
		      text: qsTr("Workroom")
		      onClicked: {
		        storeStackLayout.checkCompanyRegistration()
	        }
		    }

		    Item {
		      Layout.fillWidth: true
		    }

		    Button {
		      text: qsTr("Logout")
		      onClicked: auth_logic.sign_out()
		    }
			}

	    StackLayout {
				id: storeStackLayout

				currentIndex: navigation_logic.current_page

				property int storeGamesIndex: 0
		    property int storeDetailedGameIndex: storeGamesIndex + 1
		    property int libraryGamesIndex: storeDetailedGameIndex + 1
		    property int libraryDetailedGameIndex: libraryGamesIndex + 1
		    property int workshopRegisterCompanyInfoIndex: libraryDetailedGameIndex + 1
        property int workshopRegisterPaymentInfoIndex: workshopRegisterCompanyInfoIndex + 1
        property int workshopAppsListIndex: workshopRegisterPaymentInfoIndex + 1
        property int workshopAppControlIndex: workshopAppsListIndex + 1

        Connections {
					target: navigation_logic

					function onCurrent_page_changed() {
						storeStackLayout.currentIndex = navigation_logic.current_page
					}
				}

				Connections {
					target: auth_logic

					function onRegistered() {
						store_game_list_model.load_store()
					}

			    function onLogin() {
						store_game_list_model.load_store()
			    }

			    function onLogout() {
		        authStackLayout.currentIndex = authStackLayout.signInFormIndex
						mainStackLayout.currentIndex = mainStackLayout.authorizationSectionIndex
						storeStackLayout.currentIndex = storeStackLayout.storeGamesIndex

						navigation_logic.clear()
			    }
				}

	      GridView {
	        id: store_games_grid_view

	        property int capsuleImageWidth: 12 * 10
	        property int capsuleImageHeight: 17 * 10

	        Layout.preferredWidth: window.width
	        Layout.preferredHeight: window.height

	        cellWidth: capsuleImageWidth + defaultMargin * 2
	        cellHeight: capsuleImageHeight + defaultMargin * 2.5

	        clip: true

	        model: store_game_list_model

	        delegate: Rectangle {
	          width: store_games_grid_view.cellWidth
	          height: store_games_grid_view.cellHeight
	          color: "transparent"
	          radius: defaultMargin / 2

	          Image {
	            anchors.centerIn: parent
	            width: store_games_grid_view.capsuleImageWidth
	            height: store_games_grid_view.capsuleImageHeight
	            source: `http://localhost:8000/games/${id}/assets/capsule/`
	            mipmap: true
	          }

	          MouseArea {
	            id: cell_mouse_area
	            anchors.fill: parent
	            hoverEnabled: true
	            onEntered: parent.color = "#36373a"
	            onExited: parent.color = "transparent"
	            onClicked: {
	              navigation_logic.add(storeStackLayout.storeDetailedGameIndex)
	              store_detailed_logic.load(id)
	              storeStackLayout.currentIndex = storeStackLayout.storeDetailedGameIndex
	            }
	          }
	        }
	      }

	      ColumnLayout {
	        Text {
		        text: store_detailed_logic.game_title
		        color: "white"
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

	        Button {
	          text: "Buy"
	        }
	      }

	      ListView {
	        model: library_game_list_model

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
		              navigation_logic.add(storeStackLayout.libraryDetailedGameIndex)
		              library_detailed_logic.load(id)
		              storeStackLayout.currentIndex = storeStackLayout.libraryDetailedGameIndex
		            }
		          }
            }
          }
	      }

	      ColumnLayout {
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
  }
}