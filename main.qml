import QtQuick 2.5
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2
import QtQuick.Window 2.2
 
ApplicationWindow {
    id: window
    visible: true
    visibility: "Maximized"
    width: 800
    height: 600
    title: qsTr("notabene")

    TextArea {
        id: textarea
        focus: true
        anchors.fill: parent

        onTextChanged: textlogger.log(textarea.text)
    }
 
    Connections {
        target: textlogger
    }

    onClosing: {
        close.accepted = false
        popup.open()
    }

    Dialog {
        id: popup
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        width: 350
        height: 0
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        Rectangle {
            id: keyHandler
            focus: true
            Keys.onPressed: {
                if (event.key == Qt.Key_Q) {
                    textlogger.clean(textarea.text)
                    Qt.quit()
                }
            }
            Text {
                text: qsTr("Hit q to quit, esc to escape")
                color: "lightyellow"
            }
        }
    }
}
