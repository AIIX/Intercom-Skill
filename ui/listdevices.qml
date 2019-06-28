import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.2
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft


Mycroft.ScrollableDelegate {
    id: root
    property int uiWidth: parent.width
    property var deviceModel: JSON.parse(sessionData.deviceScan)
    skillBackgroundSource: "https://source.unsplash.com/1920x1080/?+call"
    
    Kirigami.CardsListView {
        id: uiGridView
        model: deviceModel.Devices
        delegate: Kirigami.AbstractListItem {
            contentItem: Item {
            implicitWidth: delegateLayout.implicitWidth;
            implicitHeight: delegateLayout.implicitHeight;
    
                ColumnLayout {
                    id: delegateLayout
                    anchors {
                        left: parent.left;
                        top: parent.top;
                        right: parent.right;
                    }
                
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: Math.round(Kirigami.Units.gridUnit / 2)
            
                        Kirigami.Icon {
                            id: exampleMenuItemIcon
                            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                            Layout.preferredHeight: Kirigami.Units.iconSizes.medium
                            Layout.preferredWidth: Kirigami.Units.iconSizes.medium
                            source: "similarartists-amarok"
                        }

                        
                        Kirigami.Heading {
                            id: exampleMenuItemLabel
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignHCenter
                            height: paintedHeight
                            elide: Text.ElideRight
                            font.weight: Font.DemiBold
                            text: modelData.devicename
                            textFormat: Text.PlainText
                            level: 2
                        }
                        
                        Button {
                            Layout.alignment: Qt.AlignRight
                            Layout.fillHeight: true
                            Layout.preferredWidth: paintedWidth
                            text: "Connect"
                            enabled: true
                            
                            onClicked: {
                                triggerGuiEvent("IntercomSkill.handleClientConnect", {"address": modelData.address})
                                console.log("inConnect")
                            }
                        }
                        Button {
                            Layout.alignment: Qt.AlignRight
                            Layout.fillHeight: true
                            Layout.preferredWidth: paintedWidth
                            text: "Speak"
                            enabled: true
                            
                            onClicked: {
                                triggerGuiEvent("IntercomSkill.handleSpeakStart", {})
                                console.log("inSpeakStart")
                            }
                        }
                        
                        Button {
                            Layout.alignment: Qt.AlignRight
                            Layout.fillHeight: true
                            Layout.preferredWidth: paintedWidth
                            text: "Stop Speak"
                            enabled: true
                            
                            onClicked: {
                                triggerGuiEvent("IntercomSkill.handleSpeakStop", {})
                                console.log("inSpeakStop")
                            }
                        }
                        
                        Button {
                            Layout.alignment: Qt.AlignRight
                            Layout.fillHeight: true
                            Layout.preferredWidth: paintedWidth
                            text: "Disconnect"
                            enabled: true
                            
                            onClicked: {
                                triggerGuiEvent("IntercomSkill.handleClientDisconnect", {})
                                console.log("inDisconnect")
                            }
                        }
                    }
                }
            }
        }
    }    
}
