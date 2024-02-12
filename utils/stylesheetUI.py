from PyQt5.QtGui import QFont

black = False

#fonts
fontInput = QFont('Montserrat', 10, 10)
fontColor = "white"
Background1 = [114, 116, 118]
Background2 = [70, 72, 74]
Background3 = [0, 30, 0]
StrBackground1 = "#1e1f1c"
StrBackground2 = "#292a28"
StrBackground3 = "#272822"
StrBackground4 = "#34352f"
StrBackground5 = "#414339"
StrBackgroundButtonPress = "#75715e"
colorDonutPositive = "#88d829"
colorDonutNegative = "#cc5621"

strStyleSheetsBlack = f"""
*{{
    border: none;
    background-color: transparent;
    background: transparent;
    padding: 0;
    margin: 0;
    color: white;
    }} 

    a {{
    color:white
    }}

     QMainWindow {{
                border: none;
                border-radius: 10px;
                padding: 40px;             
                background: {StrBackground1};
            }}

    #MainWindow {{
        border: none;
        border-radius: 10px;
        padding: 40px;             
        background = {StrBackground2}: 
    }}

    .QLabel{{
    color:{fontColor};
    }}

    #centralwidget{{
    background-color:{StrBackground1}; 
    padding: 40px
    }} 
    
    #header, #body, #footer{{
    background-color:{StrBackground2};
    border-radius: 8px;
    }}
    
    .QPushButton{{
    color: {fontColor};
    margin: 0px 20px;
    padding: 8px;
    border-radius: 10px;
    margin: 0px;
    background-color:{StrBackground1};
    
    }}
    #ButtonTable{{
        background-color: {StrBackground3};
    }}
    #ButtonGrid{{
        background-color: {StrBackground3};

    }}
    #bugButton{{
    background-color:rgb(144, 219, 58);
    
    }}
    
    #colaborateButton{{
    background-color: rgb(92,107,192);
    }}

    #labelError{{
    color:red;
    }}

    #InfoContainer, #logginContainer{{
    background-color:{StrBackground1};
    border-radius: 8px;
    }}
    
    .QLineEdit{{
    background-color:{StrBackground2};
;
    border-radius: 8px;
    
    }}


    
    #logginPush{{
    background-color: rgb(80,100,180);
    font-weight:bold;
    }}

    #logginPush:hover{{
    background-color: rgb(92,107,192);
    font-weight:bold;
    }}

    #ButtonWindow{{
        border-radius: 0px;
        background-color: {StrBackground2};


    }}
    #ButtonWindow:hover{{
        border-radius: 0px;  
        background-color: {StrBackground3};
    }}

    #Group{{
        background-color:   {StrBackground3};
        padding: 8px;
        border-radius: 0px;
        }}
        
    #groupContainer{{
        background-color:{StrBackground3};
        border-radius: 8px;
        margin: 5px;
        
        }}

       
    #labeNameGroup{{
        color: white;
        height: 20px;
        background-color: {StrBackground2};
        border-radius: 6px;
        font-weight:bold;
        font-size: 12px;
        }}        

    #wcontainerBoxVinfoGroup{{
        background-color: {StrBackground4};
        border-radius: 6px;
    }}

    #labelTitleDescriptionGroup{{
        background-color: {StrBackground3};
        font-weight:bold;
    }}
    
    #nameGroup{{
        color: white;
        height: 20px;
        padding: 5px;
        background-color: {StrBackground2};
        border-radius: 4px;
        margin-bottom: -4px;
        }}


    #menu{{
        background-color: {StrBackground1};
        }}
        
    #homeContainer, #body{{
        background-color:{StrBackground4};
        border-radius: 8px;
        }}
        

    #homeContainer > QGroupBox{{
        background-color: {StrBackground5};
        margin: 4px;
        border-radius: 4px;

        }}
    #gridLayout{{
        width:500px
        
        }}

    #centralwidgetHome{{
    background-color: white;
    }} 

    #ButtonMetrics:hover{{ 
        background-color: {colorDonutPositive};
    }}
    #BarBottom{{
        background-color: {StrBackground5};
    }}

    #HomeON{{
        background-color: {StrBackground1};
        border-raduis 0px;
        color: {fontColor}M
    }}
    #HomeON:hover{{ 
        background-color: {StrBackground3};
    }}

    #HomeOFF{{
        background-color: {StrBackground2};
        border-raduis 0px;
        color: {fontColor}
    }}

    #HomeOFF:hover{{ 
        background-color: {StrBackground3};
    }}


    #ButtonMetrics{{ 
        border-radius: 3px;
        color: white;
        padding: 1px;
        background-color: {StrBackground5};
    }}

    #labelHeader{{
        background-color: {StrBackground2};
        padding: 2px;
        margin-bottom: 4px;
    }}

    #LabelContend1{{
        background-color: {StrBackground5};
    }}

    #LabelContend0{{
        background-color: {StrBackground4};
    }}

    #barBottom,  #barTop, #LabelBar{{
        font-size: 12px;
        color: white;
    }}
    #barBottom::chunk{{
        background-color: red;
        font-size: 5px;
        border-radius: 4px;
    }}

    #barTop::chunk{{
        background-color: green;
        font-size: 5px;
        border-radius: 4px;
    }}

    #LabelBar{{
        padding-right: 4px;
    }}

    #ComboBoxSortBy {{
        background-color: {StrBackground2};
        border: 2px solid {StrBackground4};
        border-radius: 4px;
        padding: 1px 8px 1px 3px;
        min-width: 6em;
        color: white;
        margin-right: 32px;

    }}

    #ComboBoxSortBy::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;

        border-left-width: 1px;
        border-left-color: {StrBackground4};
        border-left-style: solid;
    }}

    #ComboBoxSortBy QAbstractItemView {{
                background-color: {StrBackground2};
                border: 2px solid {StrBackground4};
                selection-background-color:  {StrBackground1};
            }}

    #infolistOrdeGroup{{       
        font-size: 12px;
        color: white;
    }}    

    #nameGroupText{{
        font-size: 12px;
        color: white;
        padding-left: 4px;
    }}       

    #LayoutHInfoGroupContainer{{
        background-color: {StrBackground4};
        border-radius: 4px;
    }}

    #toggle_button, #sidebarChild{{
        background-color: {StrBackground3};
    }}

    #infoNews{{
        color:white;
        font-size: 10px;
    }}

   #labelStatus{{
        Background-color:{StrBackground5}; 
        border-radius: 4px; 
        font-weight:bold;
   }}

   #sidebarChild, #toggle_button{{
        background-color: {StrBackground1};
    }}

   #contentItemsNews{{
    background-color:{StrBackground3}; 
    border-radius: 8px;
   }}

    #ButtonWindowTheme{{
   margin-left: 22px;
   background-color:white;
   border-radius: 10px;
   margin-top:4px;
   margin-right:2px;
   }}
   #SpiderChart{{
        background-color: {StrBackground3};
    }}
   #buttoThemeWidget{{
        background-color:{StrBackground3};
        border-radius: 12px;
   }}

    QScrollBar:vertical {{
        width: 10px;
        background-color: {StrBackground3};
    }}

    QScrollBar::handle:vertical {{
        background-color: {StrBackground1};
        border-radius: 5px;
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}


"""



fontInput = QFont('Montserrat', 10, 10)
fontColorLight = "#222230"
Background1Light = [114, 116, 118]
Background2Light = [70, 72, 74]
Background3Light = [0, 30, 0]
StrBackground1Light = "#dedee3"
StrBackground2Light = "#f6f1f6"
StrBackground3Light = "#ffffff"
StrBackground4Light = "#fff"
StrBackground5Light = "#c7c8bc"
StrBackground6Light = "#b5b6aa"
StrBackground7Light = "#0e72ed"
StrBackgroundButtonPressLight = "rgb(100, 100, 100)"
colorDonutPositiveLight = "rgb(144, 219, 58)"
colorDonutNegativeLight = "red"



strStyleSheetsLight = f"""
*{{
    border: none;
    background-color: transparent;
    background: transparent;
    padding: 0;
    margin: 0;
    color: {StrBackground5Light};
    }} 

    QMainWindow {{
    border: none;
    border-radius: 10px;
    padding: 40px;             
    background: {StrBackground1Light};
    }}


    .QLabel{{
    color:{fontColorLight};
    }}

    #centralwidget{{
    background-color:{StrBackground1Light}; 
    padding: 40px
    }} 
    
    #header, #body, #footer{{
    background-color:{StrBackground2Light};
    border-radius: 8px;
    }}
    
    .QPushButton{{
    color: {fontColorLight};
    margin: 0px 20px;
    padding: 8px;
    border-radius: 10px;
    margin: 0px;
    background-color:{StrBackground1Light};
    
    }}
    
    #bugButton{{
    background-color:rgb(144, 219, 58);
    
    }}
    #HomeON{{
        background-color: {StrBackground1Light};
        border-raduis 0px: 
        margin: 0px;
        padding: 0px;
        color: {fontColorLight};
    }}

    #HomeON:hover{{ 
        background-color: {StrBackground3Light};
    }}

    #HomeOFF{{
        background-color: {StrBackground2Light};
        border-raduis 0px: 
        margin: 0px;
        padding: 0px;
        color: {fontColorLight}
    }}

    #HomeOFF:hover{{ 
        background-color: {StrBackground3Light};
    }}


    
    #colaborateButton{{
    background-color: rgb(92,107,192);
    }}
    
    #InfoContainer, #logginContainer{{
    background-color:{StrBackground2Light};
    border-radius: 8px;
    border: 1.5px solid {StrBackground6Light}; 
    }}
    
    .QLineEdit{{
    background-color:{StrBackground1Light};
    border-radius: 8px;
    color: {fontColorLight}}}

    #Remember{{
        color:black;
        font-weight:bold;
        }}

    #labeNameGroup{{
    height: 20px;
    background-color: {StrBackground2Light};
    border-radius: 4px;
    font-weight:bold;
    font-size: 12px;
    }}        

    #containerDescriptionGroup{{
        background-color: {StrBackground3Light};
        border-radius: 4px;
    }}

    #labelTitleDescriptionGroup{{
        background-color: {StrBackground3Light};
        font-weight:bold;
    }}

    #Remember::indicator {{ 
            
        border: 2px solid #999; 
        border-radius: 4px; 
        color:white}}

    #Remember::indicator:checked {{ 
        background-color: rgb(92,107,192); 
        border: 2px solid black; }}


    
    #logginPush{{
    background-color: {StrBackground7Light};
    font-weight:bold;
    color: white;
    }}


    #ButtonWindow{{
        border-radius: 0px;
        background-color: {StrBackground1Light};


    }}
    #ButtonWindow:hover{{
        border-radius: 0px;  
        background-color: {StrBackground5Light};
    }}

    #labelError{{
    color:red;
    }}

    #Group{{
        background-color:   {StrBackground3Light};
        padding: 8px;
        border-radius: 0px;
        color: {fontColorLight};
        }}

    #sidebarChild{{
        background-color: {StrBackground1Light};
    }}
        
    #groupContainer{{
        background-color:{StrBackground3Light};
        border-radius: 8px;
        margin: 5px;
        border: 1.5px solid {StrBackground5Light}; 
        
        }}
        
    #nameGroup{{
        color: {fontColorLight};
        height: 20px;
        padding: 5px;
        background-color: {StrBackground1Light};
        border-radius: 4px;
        margin-bottom: -4px;
        
        }}

    metricGroup{{
        border-top: 1.5px solid {StrBackground5Light}; 
    }}

    #menu{{
        background-color: {StrBackground1Light};
        border-right: 2px solid {StrBackground3Light}; 
        
        }}
        
    #homeContainer, #body{{
        background-color:{StrBackground1Light};
        border-radius: 8px;
        
        }}
        

    #homeContainer > QGroupBox{{
        background-color: {StrBackground5Light};
        margin: 4px;
        border-radius: 4px;
        

        }}
    #gridLayout{{
        width:500px
        
        }}
    #SpiderChart{{
        background-color: green;
    }}
    #centralwidgetHome{{
    background-color: {StrBackground3Light};
    }} 

    #ButtonMetrics:hover{{ 
        
        background-color: {StrBackground1Light};
    }}
    #ButtonMetrics{{ 
        border-radius: 5px;
        color: {fontColorLight};
        padding: 1px;
        border: 1px solid {StrBackground6Light};
        background-color: {StrBackground3Light};
    }}
    #ButtonTable{{
        background-color: {StrBackground3Light};
    }}

    #ButtonGrid{{
        background-color: {StrBackground3Light};
    }}
    #labelHeader{{
        background-color: {StrBackground7Light};
        padding: 2px;
        margin-bottom: 4px;
        color: white;
    }}

    #LabelContend1{{
        background-color: {StrBackground3Light};
        color: {fontColorLight}
    }}

    #LabelContend0{{
        background-color: {StrBackground5Light};
        color: {fontColorLight}
    }}

    #barBottom,  #barTop{{
        font-size: 12px;
        color: {fontColorLight};
    }}

    #LabelBar{{
        font-size: 12px;
        color: {fontColorLight};
    }}

    #BarBottom{{
        background-color: {StrBackground5Light};
    }}

    #barBottom::chunk{{
        background-color: red;
        font-size: 5px;
        border-radius: 4px;
    }}

    #barTop::chunk{{
        background-color: green;
        font-size: 5px;
        border-radius: 4px;
    }}
    #LabelBar{{
        padding-right: 4px;
    }}

    #ComboBoxSortBy {{
        background-color: {StrBackground3Light};
        border: 2px solid {StrBackground5Light};
        border-radius: 4px;
        padding: 1px 8px 1px 3px;
        min-width: 6em;
        color: {fontColorLight};
        margin-right: 32px;

    }}

    #ComboBoxSortBy::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;

        border-left-width: 1px;
        border-left-color: {StrBackground1Light};
        border-left-style: solid;
    }}

    #ComboBoxSortBy QAbstractItemView {{
                background-color: {StrBackground5Light};
                border: 2px solid {StrBackground1Light};
                selection-background-color:  {StrBackground1Light};
            }}

    #infolistOrdeGroup{{       
        font-size: 12px;
        color: {fontColorLight};
    }}    

    #nameGroupText{{
        font-size: 12px;
        color: {fontColorLight};
        padding-left: 4px;
        text-decoration: none;
        
    }}    

    #Text{{
    color: {fontColorLight};
    }}   

    #LayoutHInfoGroupContainer{{
        background-color: {StrBackground1Light};
        border-radius: 4px;
        border: 0.5px solid {StrBackground5Light}; 
    }}

    #toggle_button, #sidebarChild{{
        background-color: {StrBackground6Light};
    }}

    #infoNews{{
        color: black;
        font-size: 10px;
    }}

   #labelStatus{{
        Background-color:{StrBackground3Light}; 
        border-radius: 4px; 
        font-weight:bold;
   }}

   #LabelInforGroup{{
    color: {fontColorLight}
   }}

   #contentItemsNews{{
    background-color:{StrBackground3Light}; 
    border-radius: 8px;
   }}
#Progressbar{{
background-color: {StrBackground4Light};

border: 0.5px solid {StrBackground1Light}; 
}}

#Progressbar::chunk {{
background-color: {StrBackground7Light};
}}


#ButtonWindowTheme{{
   margin-right: 22px;
   background-color:{StrBackground2Light};
   border-radius: 10px;
   margin-top:4px;
   margin-left:2px;
   }}
#buttoThemeWidget{{
        background-color:{StrBackground5Light};
        border-radius: 12px;
        padding: 4px;
   }}

QScrollBar:vertical {{
    width: 10px;
    background-color: {StrBackground5Light};
}}

QScrollBar::handle:vertical {{
    background-color: {StrBackground4Light};
    border-radius: 5px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

"""

