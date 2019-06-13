#include "widget.h"
#include "ui_widget.h"

using namespace std;

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    this->setWindowTitle("Dashboard");
    this->setWindowState(Qt::WindowMaximized);
    setStyleSheet("QWidget{background-color : black}");
    

    QLabel *label = new QLabel(this);
    label->setStyleSheet("color : white");
    

    // double progressBarWidthScale = 1.1;
    // bool progressBarTextState = false;
    int motorTemperatureMinimum = -20;
    int motorTemperatureMaximum = 235;
    int totalTemperatureDifference = motorTemperatureMaximum - motorTemperatureMinimum;

    // int id = QFontDatabase::addApplicationFont("font/DS-DIGI.TTF");
    // QString family = QFontDatabase::applicationFontFamilies(id).at(0);
    // QFont digital(family);

    // label->setFont(digital);

    label->setNum(totalTemperatureDifference);

    
}

Widget::~Widget()
{
    delete ui;
}
