> 一个JAVAFX程序应该是这样的，一个stage，stage里面包含一个scene，一个scene可以包含多个control。

## 开发
Java8中已经内置了javafx，如果是jdk8的话就可以直接开发javafx程序。

## UI控件
常用的UI控件如下:
* Label(标签)
* Button(按钮)
* Radio Button(单选按钮)
* Toggle Button(开关按钮)
* CheckBox(复选框)
* ChoiceBox(选择框)
* TextField(文本框)
* PasswordField(密码框)
* ScrollBar(滚动条)
* ScrollPane(滚动面板)
* ListView(列表视图)
* TableView(表格视图)
* TreeView(树视图)
* TreeTableView(树表视图)
* ComboBox(组合框)
* Separator(分隔符)
* Slider(滑块)
* Hyperlink(超链接)
* Menu(菜单)
* FileChooser(文件选择框)

## JavaFX中的Pane种类(布局种类)
> 参考 https://www.jianshu.com/p/e2f16c74c7ba 以及 https://blog.csdn.net/theonegis/article/details/50184811
* AnchorPane:最常见的种类，可以通过下列方法来设置各区域与组件之间的距离。
 
```java
//上方与组件的距离
setTopAnchor()          
//上方与组件的距离
setBottomAnchor()
//左方与组件的距离
setLeftAnchor()
//右方与组件的距离
setRightAnchor()
```
* BorderPane:分为上下左右和中央五个区域。通过以下方法来设置对应位置：
```java
setTop()
setBottom()
setLeft()
setRight()
setCenter()
```
* FlowPane:两种方向，默认水平。达到最大宽度或者最大高度就会自动换行。
* GridPane:表格式布局。