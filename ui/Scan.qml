import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.2
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.4 as Kirigami
import Mycroft 1.0 as Mycroft

PlasmaCore.ColorScope {
    anchors.fill: parent
    colorGroup: PlasmaCore.Theme.ComplementaryColorGroup
    Kirigami.Theme.colorSet: Kirigami.Theme.Complementary

    ColumnLayout {
        spacing: 0
        anchors {
            fill: parent
            margins: Kirigami.Units.largeSpacing
        }

        Kirigami.Heading {
                id: scanPgTextHeading
                level: 1
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
                text: i18n("Nearby Devices")
                color: Kirigami.Theme.highlightColor
        }
        
        Item {
            Layout.preferredHeight: Kirigami.Units.largeSpacing
        }
        
        Kirigami.Separator {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
        }
        
        Kirigami.ScrollablePage {
            id: page
            supportsRefreshing: true
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            onRefreshingChanged: {
                if (refreshing) {
                    refreshTimer.restart()
                }
            }
            
            Timer {
                id: refreshTimer
                interval: 3000
                onTriggered: page.refreshing = false
            }
            
            ListView {
                id: networkView
                model: intercomLoaderView.devicesList.Devices
                currentIndex: -1
                delegate: Kirigami.AbstractListItem {
                        id: deviceItem
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
                                spacing: Math.round(units.gridUnit / 2)

                                Kirigami.Icon {
                                    id: deviceSvgIcon
                                    Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                                    Layout.preferredHeight: units.iconSizes.medium
                                    Layout.preferredWidth: units.iconSizes.medium
                                    color: Kirigami.Theme.textColor
                                    source: "similarartists-amarok"
                                }

                                ColumnLayout {
                                    Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

                                    Kirigami.Heading {
                                        id: deviceNameLabel
                                        Layout.alignment: Qt.AlignLeft
                                        level: 2
                                        elide: Text.ElideRight
                                        text: modelData.devicename
                                        textFormat: Text.PlainText
                                    }
                                }
                            }
                        }
                    }
                    
                    onClicked: {
                        triggerGuiEvent("IntercomSkill.handleClientConnect", {"address": modelData.address})
                    }
                }
            }
        }
    }
}
