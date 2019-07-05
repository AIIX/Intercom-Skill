import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.5 as Kirigami
import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    id: intercomLoaderView

    property var pageToLoad: sessionData.pageState
    property var devicesList: JSON.parse(sessionData.deviceScan)
    property var intercomStatus: sessionData.intercomStatus
    
    contentItem: Loader {
        id: rootLoader
    }

    onPageToLoadChanged: {
        console.log(sessionData.pageState)
        rootLoader.setSource(sessionData.pageState + ".qml")
    }
} 
