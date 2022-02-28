from cProfile import label
from datetime import datetime
from turtle import up
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
# Only needed for access to command line arguments
import sys


upNextModel = QStandardItemModel()
absentModel = QStandardItemModel()

done = []
absent = []


scrumMaster = ""
productOwner = ""


numberRoster = 0


############################Load the model###############################################3

lines = []
with open('roster.txt') as f:
    lines = f.readlines()

scrumMaster = lines.pop(0).rstrip()
productOwner = lines.pop(0).rstrip()
for person in lines:
    item = QStandardItem()
    item.setText(person.rstrip())
    upNextModel.appendRow(item)
f.close()
po = QStandardItem(productOwner)
upNextModel.appendRow(po) 

numberRoster = upNextModel.rowCount()+1

############Load Lists###############################################################

##################################GUI################################################

app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = QWidget()
window.setWindowTitle("Random Selector")
layout = QGridLayout()
upNextList = QListView()





#Add widgets.
upNextList.setModel(upNextModel)
upNextList.setDragEnabled(True)
upNextList.setAcceptDrops(True)
upNextList.setDefaultDropAction(Qt.MoveAction)



doneListView  = QListView()
doneListModel = QStandardItemModel(doneListView)
doneListView.setModel(doneListModel)
doneListView.setDragEnabled(True)
doneListView.setAcceptDrops(True)
doneListView.setDefaultDropAction(Qt.MoveAction)


absentList = QListView()
absentList.setModel(absentModel)
absentList.setAcceptDrops(True)
absentList.setDragEnabled(True)
absentList.setDefaultDropAction(Qt.MoveAction)

#Create the button group.
buttonGroup = QGridLayout()
nextButton = QPushButton("Next")
undoButton = QPushButton("Undo")
upNowNameLabel = QLabel()

#Create the labels and set the text and font
upLabel = QLabel()
nextLabel = QLabel()
goneLabel = QLabel()
absentLabel = QLabel()

nextLabel.setText("Hasn't gone:")
goneLabel.setText("Gone:")
absentLabel.setText("Absent:")

upNowNameLabel.setFont(QFont("Times", 25))
upLabel.setFont(QFont("Times", 25))

#Add the buttons to the button group
buttonGroup.addWidget(nextButton)
buttonGroup.addWidget(undoButton)

###add widgets to layout####

## Add all the widgets to the 
upNowNameLabel.setText(scrumMaster)## the scrum master begins the meeting
upLabel.setText("Up: ")
layout.addWidget(upLabel,0,0,1,1, Qt.AlignRight)
layout.addWidget(upNowNameLabel, 0,1, 1,2, Qt.AlignVCenter)

layout.addWidget(nextLabel, 1,0)
layout.addWidget(goneLabel,1,1)
layout.addWidget(absentLabel, 1, 2)

layout.addWidget(upNextList, 2,0)
layout.addWidget(doneListView, 2, 1)
layout.addWidget(absentList,2, 2)
layout.addLayout(buttonGroup,3,2)

window.setLayout(layout)
##Startup:




window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.


############################BACKEND/controllers##################################################

#Create the lists.


#Uses microseconds
def randomSelect(numElements)->int:
    dt = datetime.now()
    ms = dt.microsecond
    
    return ms % numElements
    
#This is connected to the next button.
def nextFunc():
    

    if(upNextModel.rowCount() > 1):     
        randIndex = randomSelect(upNextModel.rowCount() - 1)
        nextItem = upNextModel.takeItem(randIndex, 0)


        upNextModel.removeRow(randIndex)

        doneListModel.insertRow(doneListModel.rowCount(), QStandardItem(upNowNameLabel.text()))
        upNowNameLabel.setText(nextItem.text())

    elif(upNextModel.rowCount()== 1):
        nextItem = upNextModel.takeItem(0,0)
        upNextModel.removeRow(0)
        doneListModel.insertRow(doneListModel.rowCount(), QStandardItem(upNowNameLabel.text()))
        upNowNameLabel.setText(nextItem.text())
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Any Go Backs?")

        retval = msg.exec_()
        

def undoFunc():
    doneCount=doneListModel.rowCount()
    print(str(doneCount))
    if(doneCount < numberRoster):
        doneItem = doneListModel.takeItem(doneListModel.rowCount()-1,0)
        
        if(doneItem is not None):
            doneListModel.removeRow(doneListModel.rowCount()-1)
            if(doneItem.text() != productOwner):
                upNextModel.insertRow(0, QStandardItem(upNowNameLabel.text()))
                upNowNameLabel.setText(doneItem.text())

            else:
                upNextModel.insertRow(upNextModel.rowCount()+1, QStandardItem(upNowNameLabel.text()))
                upNowNameLabel.setText(doneItem.text())

    elif(doneCount == numberRoster):
        upNowNameLabel.setText(doneListModel.takeItem(doneListModel.rowCount()-1,0).text())
        doneListModel.removeRow(doneListModel.rowCount()-1)


        


    
    

############################connect the buttons###############################################
nextButton.clicked.connect(nextFunc)
undoButton.clicked.connect(undoFunc)



app.exec()