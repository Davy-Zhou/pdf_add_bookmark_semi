[toc]

# 半自动化给PDF加书签-Python实现-可双击执行-上篇

![PDF直接加书签](https://s2.loli.net/2022/12/14/ZQipAXE7gWyhbu2.gif)

**下载链接**：https://github.com/Davy-Zhou/pdf_add_bookmark_semi/releases/download/v0.60/pdf_add_bookmark_semi.v0.60.zip

## 零、功能更新&Bug修复

`Bug或新功能，最好在Github里的issue里面提,要提新功能代码，欢迎提PR,其它平台不一定能及时看到，github 有邮件通知`:handshake:



- [x] **2022-11-22**

  - [x] 针对页偏移无法识别时，**增加页偏移输入选项**，无需重开程序

    ![](https://s1.ax1x.com/2022/11/22/z1ovVg.png)

  - [x] 针对**多个PDF要加书签**情况，完成一个PDF加书签后，无需重开，回车即可给下一个PDF加书签

    ![image-20221122005132356](https://s1.ax1x.com/2022/11/22/z1oxaQ.png)

  - [x] **书签格式化库规则更新**

    ![image-20221122005253065](https://s1.ax1x.com/2022/11/22/z1oz5j.png)



- [x] **2022-8-17**
  - [x] **增加多级书签无前置书签和书签层级不连续提示:bug:**
  - [x] **提高容错性，非命令行下，显示报错提示**:bug:
  - [ ] **dll不单独进打包exe，提升启动速度🐎**

- [x] **2022-8-15**

  - [x] **新的打包方式，依赖有问题，改用旧的打包方式:bug:**

    ![Snipaste_2022-08-15_08-31-43](https://img2022.cnblogs.com/blog/1431291/202208/1431291-20220815083720793-482995602.png)

- [x] **2022-8-14** 

  - [x] **完成书签获取自动化:sparkles:**
  - [x] **可自动识别部分PDF页偏移:sparkles:**
  - [x] **改用新打包方式，exe体积更小，速度更快:sparkles:**



- [ ] **2022-8-1**

  - [x] **加书签时，增加清空原有书签选项:sparkles:**
  - [ ] **检测页码合法性，是否超出pdf页数**
  - [ ] **相关容错改进**

- [ ] **2022-8-3**

  - [ ] **bug 参数解析依赖** 

    ![image-20220803170309034](https://img2022.cnblogs.com/blog/1431291/202208/1431291-20220815083720475-761995728.png)

  - [ ] 

- [ ] **2022-8-4**

  - [ ] **所有判断做充分性测试**

    ```markdown
    ```

    

- [ ] **2022-8-9 着重新功能，性能优化，非严重容错问题暂时不修** 

  - [ ] **自动化获取书签**

    ```markdown
    # PyAutoGui or pywin 模拟点击
    
    # 读秀WEB JS逆向书签接口
    
    # 书签获取软件逆向接口
    
    ```

    

  - [ ] **加书签性能优化**

    ````markdown
    # 尝试extend()方法
    2022年8月9日02:15:59
    
    1. 
    ```python
    
    outline.root.extend([
     # Page counts are zero-based
     OutlineItem('Section One', 0),
     OutlineItem('Section Two', 2),
     OutlineItem('Section Three', 8)
     ])
    
    
    main_item = OutlineItem('Main', 0)
    outline.root.append(main_item)
    main_item.children.append(OutlineItem('A', 1))
    
    # 还落是明天弄了，想睡觉了
    2022年8月10日02:28:55
    # 这个耗时不算太多，先弄书签获取 MuPDF已完成 \学习\mupdf_add_bookmark.py
    
    ```
    
    # PyPDF2竟然更新了，试一下，额，WPS PDF差1的问题还是存在
    
    
    # 使用Mupdf，及其它PDF操作Python库
    
    
    # C pdf lib
    
    ````

    ![](https://img2022.cnblogs.com/blog/1431291/202208/1431291-20220815083719868-1780167968.png)

    

    

  - [ ] **打包exe优化**

    ```markdown
    # niutika
    
    # 
    
    # 
    ```

    

- [ ] 





## 一、PDF加书签介绍

### 1.1 不那么漂亮的话

1. ==本工具只进行**书签部分格式化和加书签操作**，**书签获取需要配合其它工具**==
2. 最终书签效果因人而异，程序只能格式化最常见的层级，毕竟是半自动的
3. ==最好了解一定正则和列操作==，不了解的话可能要多手工重复一些操作
5. ==相比现有工具，没有太大优势，最初只是个人使用==
6. 反反复复改了一星期，差不多能用了，虽然代码依然很烂

### 1.2 PDF加书签难点 

#### 1.2.1 书签获取

一般需要加书签的，大多是扫描版书籍，而市面上绝大多数扫描版书籍均出自**超星公司(读秀和全国图书参考联盟都是他家的)**，为了方便学术检索，超星有对目录进行提取，如下图。

![image-20220724190634286](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210451058-765396734.png)



![image-20220724190715119](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210450647-778903313.png)



![image-20220725153156223](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210450242-38871843.png)



​		额，然后有人分析出了超星书签的接口，做成了书签获取工具，如下图，**通过它能获取大多数书的书签**。

![image-20220727135111812](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210449906-239915737.png)



![image-20220724191423259](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210449522-1063451267.png)

但检索一本书的书签，需要知道书在超星的内部编号，上图书签获取工具填的就是那个编号

- **SSID( Super Star ID，超星英文简写)**

  书签接口是超星开发的，其中检索每本书的书签不是通过ISBN或书名，而是其内部定义的编号**SSID**,这个SSID可以**油猴脚本**获取，推荐[文献互助小帮手](https://greasyfork.org/zh-CN/scripts/435569-%E6%96%87%E7%8C%AE%E4%BA%92%E5%8A%A9%E5%B0%8F%E5%B8%AE%E6%89%8B-%E4%BB%8E%E5%9B%BE%E4%B9%A6%E9%A6%86%E5%8F%82%E8%80%83%E5%92%A8%E8%AF%A2%E8%81%94%E7%9B%9F-ucdrs-%E6%88%96%E8%AF%BB%E7%A7%80-duxiu-%E8%8E%B7%E5%8F%96ssid-dxid-%E4%BB%8E%E4%B8%AD%E7%BE%8E%E7%99%BE%E4%B8%87-cadal-%E8%8E%B7%E5%8F%96ssno-%E6%8F%90%E4%BE%9Bucdrs-duxiu-cadal%E5%88%B0%E8%B1%86%E7%93%A3%E5%9B%BE%E4%B9%A6%E7%9A%84%E9%93%BE%E6%8E%A5)这个脚本，读秀和全国图书参考联盟都可以获取SSID，但在装油猴脚本前需要装[油猴插件](https://zhuanlan.zhihu.com/p/128453110)

  ![image-20220724194106998](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210449138-1158726713.png)

  

  ![image-20220724194617355](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210448725-1630071945.png)

  装好的**油猴插件、油猴脚本**

  ![image-20220724195118825](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210448347-223706030.png)



**如果书签工具也没有那本书的书签，怎么办？**

- 这篇博客 [下载超星或读秀图书时，怎么搞定完整书签?](https://blog.csdn.net/youthlzu/article/details/24514703) 讲的可以，不重复了，主要是在~~各出版社官网，电商网站，豆瓣找~~，直接Google书签里面的内容，层级深一点的那个，实在没有就OCR书里面的目录部分再整理



**推荐阅读，上面的内容主要参考这三篇文章**

- 文献互助小帮手：https://greasyfork.org/zh-CN/scripts/435569-%E6%96%87%E7%8C%AE%E4%BA%92%E5%8A%A9%E5%B0%8F%E5%B8%AE%E6%89%8B-%E4%BB%8E%E5%9B%BE%E4%B9%A6%E9%A6%86%E5%8F%82%E8%80%83%E5%92%A8%E8%AF%A2%E8%81%94%E7%9B%9F-ucdrs-%E6%88%96%E8%AF%BB%E7%A7%80-duxiu-%E8%8E%B7%E5%8F%96ssid-dxid-%E4%BB%8E%E4%B8%AD%E7%BE%8E%E7%99%BE%E4%B8%87-cadal-%E8%8E%B7%E5%8F%96ssno-%E6%8F%90%E4%BE%9Bucdrs-duxiu-cadal%E5%88%B0%E8%B1%86%E7%93%A3%E5%9B%BE%E4%B9%A6%E7%9A%84%E9%93%BE%E6%8E%A5
- 淘宝书商为啥什么书都能找到：揭秘代找PDF背后的真相 ：https://mp.weixin.qq.com/s/7SX-Oztgx2q76AN5YpntTA
- 下载超星或读秀图书时，怎么搞定完整书签? ：https://blog.csdn.net/youthlzu/article/details/24514703



#### 1.2.2 书签格式化

​		==最初获取的书签结构化程度，很大程度决定了后期格式化用的时间。==根据经验，书签格式化有三个小点，**书签层级**、**每级书签样式**和**页码偏移**。

- **书签层级**

  ​		以《人工智能在信用债投资领域的应用 Python语言实践》(SSID: 14545152)这本书为例，见下图，这是从`书签获取小工具2015.05.05【晴天软件】`获得的初步整理的书签。另外**规定**对于书签的层级一律以`Tab`来区分，一级书签前面没有`Tab`，二级书签前面有1个`Tab`，三级书签则有2个`Tab`

  ![image-20220725214301736](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210447941-1543770321.png)

  ​		从中可以看出，除对一级书签（即按章开头的那个第*章），其它书签均格式化为二级书签，其中标注的第6行和第31行应分别为三级书签和一级书签，如下图为修正好的书签

  ![image-20220725220214872](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210447427-653240368.png)

  

- **每级书签样式**

  ​		还是以同一本书为例看书签样式问题，注意第4行，`第2章  机器学习`，标号与标题中间有两个空格;第6行，`2.1.1有监督机器学习`，标号与标题中间则没有空格;第11行，`第3章  基于TensorFlow用Keras做深度学习`，里面的英文单词是应该首字母大写还是按原样输出，后面的附录那节同第一个问题。

  ​		==这个按照每个人的审美不同，具体怎么弄，得看你们自己的选择==

  ![image-20220725224019744](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210447015-1970695985.png)

  ​		个人的审美是，标号与标题之间只留一个空格，英文单词全部统一成小写，虽然按原样输出就挺不错的，但加了这么多PDF的书签，最终还是选择统一单词的风格，结果如下图

  ![image-20220725224837208](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210446507-818680250.png)

- **页码偏移**

  ​		超星的书签应该也是从目录这部分OCR提取的，见下图，但其中的页码和实际的页码有偏移（因为目录里面的页码是从正文开始算的，而实际的书签引用页码必须是从第一开始的绝对页码），第二章在目录里是页码是`6`，而实际绝对页码是`16`，二者相差`10`，加书签时必须补上这个页码，见第二张图。

  ![image-20220725230132610](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210445956-1922657762.png)

  ​		所有正文之后的页码必须`+10`进行修正，如下图

  ![image-20220725215853920](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210445566-1460071775.png)

  



### 1.3 工具使用限制

​		在最开始已经介绍，本工具只能进行书签部分格式化，还有一部分是需要手工操作的，特别是对于从非`书签获取小工具2015.05.05【晴天软件】`获得的书签，程序处理会有很大问题，，，

- **从`书签获取小工具2015.05.05【晴天软件】`获取书签**

  ​		如下图红框，书签层级是通过数字标号来定位的，但如下图框中，书签部分前面没有标号，所以没办法分层级。**最后的处理办法是对所有不能通过其特定标识分层级的，全部默认分到二级书签。**之后就得自己去修正正确的层级。

  ![image-20220725232316741](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210445113-1319645292.png)

- **从其它处获得的书签**

  ​		如下图，一些新书是没有录入库的，只能从其它地方拿书签了。

  ![image-20220727143357521](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210444621-1396816867.png)

  ​	下面是从京东商城的商品界面，可以看到目录，

  ![image-20220727144504847](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210444238-1532342041.png)

  ​		复制到TXT文档里面，可以发现其中标签与页码之间有`点符号`，另外还有空行，如果需要用这个书签的话，这个需要把里面的点符号还有空行删了，这个需要用到正则表达式进行替换，不过注意别把书签的数字标号之间的点删除了。

  ![image-20220727145143434](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210443867-2068715120.png)

  ​		试着把这个txt格式化一下，**如图，箭头所指的点没删除，后面有时间再优化这个问题了**。

  ![image-20220727145907978](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210443438-45167007.png)

  

  

## ﻿二、使用方式

### 2.1 工具介绍

1. **工具结构**

   ![image-20220730163322796](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210443089-1018768952.png)

   ```yaml
   #目录树
   .
   ├── Config 
   │   └── config.yaml  #配置文件
   ├── Notepad3
   │   ├── Notepad3.exe  #协同工具-文本编辑器
   │   ├── Notepad3.ini
   │   └── lng
   │       ├── np3lng.dll
   │       └── zh-CN
   │           └── np3lng.dll.mui
   ├── format_bookmark.py  #代码-格式化书签
   ├── pdf_add_bookmark_semi.exe #代码-打包的exe
   ├── pdf_add_bookmark_semi.py  #代码-加书签
   └── 书签获取小工具2015.05.05【晴天软件】.exe  #协同工具-书签获取工具
   ```

   **主要是三部分：代码（`format_bookmark.py`、`pdf_add_bookmark_semi.py`、`pdf_add_bookmark_semi.exe`）、配置文件（`Config/config.yaml`）、以及协同工具（`Notepad3/Notepad3.exe`、`书签获取小工具2015.05.05【晴天软件】.exe`）**

   - **代码**

     一个用来格式化书签`format_bookmark.py`，另一个用来加书签`pdf_add_bookmark_semi.py`，最终打包成`pdf_add_bookmark_semi.exe`，具体分析见第三节

     **主要实现功能**

     1. 可加4级书签
     2. 书签格式化规则可自己配置

   - **配置文件**

     `Config/config.yaml`，里面用于配置编辑器的启用、使用哪个编辑器、首字母是否小写、以及最重要的书签格式化规则，具体的看配置文件吧

     ![image-20220730180818636](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210442702-663009690.png)

   - **协同工具**

     协同工具一个是文本编辑器`Notepad3`也就是上图所示的软件，另一个是`书签获取小工具2015.05.05【晴天软件】.exe`），第一节也介绍了，**不过这个软件会报毒**，加了**VMP**的壳，这软件我也不知道是谁写的，，，应该没毒吧，15年开发的，很多人也用了很久了。如果被杀软杀了，记得加信任区。

     ![image-20220730192924607](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210442268-203418426.png)

### 2.2 半个图形化界面---可双击执行



1. **SS号**

   ​		上面有介绍通过油猴脚本获取的方式，这里再介绍一个网站：http://115.159.153.83:19777/index.html  

   在上面直接搜索书名，可获得ss号。

   ![image-20220730193756002](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210441916-1734843923.png)

2. **书签获取**

   务必保存到要加书签的pdf的那个文件夹，**另外txt文件名要与pdf相同**

   ![image-20220730194321458](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210441553-1878416254.png)

   

   ![image-20220730194615700](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210441236-896408062.png)

   

   

3. **加书签**

   双击`pdf_add_bookmark_semi.exe`,会弹出控制台界面

   ![image-20220730194837484](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210440924-63990559.png)

   用法，上面也提了，要输入书签文件名（txt那个文件）、正文页偏移以及目录页码（这个参数可选）

   

   ![image-20220730195144581](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210440607-1029220533.png)

   直接将txt书签文件拖到控制台界面，然后填好页偏移10

   

   ![image-20220730195806963](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210440065-267644952.png)

   书签和页偏移之间要留空格

   ![image-20220730195846800](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210439653-1782062262.png)

   回车，会进行初步格式化，然后弹出书签编辑页面，之后进行修正

   ![image-20220730200052567](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210439302-1858777941.png)

   附录那要改成一级书签，并去掉多余空格，书签规定看`1.2.2书签格式化`那节

   ![image-20220730200243287](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210438780-16612749.png)

   

   

   ![image-20220730200355030](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210438411-1520359829.png)

   按上图改完之后，记得关闭编辑器，然后到了加书签界面，输入`y`是加，`n`是不加书签

   ![image-20220730200526540](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210437506-1213106371.png)

   输入`y`，回车加书签（记得加书签的时候，pdf不能被其它应用使用）

   ![image-20220730200830749](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210437114-940869735.png)

   按回车，退出，一切OK

4. **加书签的程序也能发送到桌面，创建快捷方式，直接双击**

   ![image-20220730202845354](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210436732-436451913.png)

   

   ![image-20220730202936398](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210436253-1703725880.png)

   



### 2.3 命令行

和上面一样的，只是前面多了执行的解释器和py文件，另外注意安装Python模块pikepdf、colorama

```bash
python pdf_add_bookmark_semi.py "C:\Users\acer\Desktop\Notes\安全\Blog\test\人工智
能在信用债投资领域的应用 Python语言实践.txt" 10
```

![image-20220730201303959](https://img2022.cnblogs.com/blog/1431291/202207/1431291-20220730210434825-247303699.png)

****



### 2.4 下载链接

Github：https://github.com/Davy-Zhou/pdf_add_bookmark_semi/releases

## 三、代码实现

**下次吧，写文档也累了**

1. 

   

2. 

   

3. 



## 四、TODO

- [x] **书签获取有点花时间，争取下次自动化获取**
- [x] **书签页码偏移部分可自动识别**
- [ ] **界面美化**
- [ ] **书签格式化规则更新**

