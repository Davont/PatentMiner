# PatentMiner

## Environment

    pip install django==1.11.7
    pip install django-haystack==2.8.1
    pip install mysqlclient==1.3.12
    pip install Pillow==5.1.0
    pip install elasticsearch==1.7.0
    pip install xlwt==1.3.0

## 统一数据库

1. 打开 mysql Command——>输入密码
2. 创建新用户： create use 'patentuser'@'localhost' IDENTIFIED BY '123456';
3. 赋予权限： grant all on _._ to 'patentuser'@'localhost';
4. 权限生效： FLUSH PRIVILEGES;
5. 打开图形界面 ——>新建连接——>用户名改为 patentuser——>密码改为 123456——>连接

## 开启 elasticsearch 服务

1、命令行进入 elasticsearch-6.2.0 文件夹下的 bin 目录
2、运行 elasticsearch.bat

## PatentMiner 前端页面介绍

### 整体模板 templates 分类：law_regulate，sitesearch


- #### law_regulate 模板

  代表法律法规相关页面的加载模板（但实际上 law_regulate 里面的 base.html 是更改 sitesearch 里面的首页相关代码的。原因是 Django 当时 view 层定义问题，与前端不关联）
  [![iUkJ4U.md.png](https://s1.ax1x.com/2018/10/14/iUkJ4U.md.png)](https://imgchr.com/i/iUkJ4U)

- #### sitesearch 模板

  该项目的主要模板，里面分为：

  1. base.html 基础板块

  2. patent_list 专利列表

     [![iUkrE6.md.png](https://s1.ax1x.com/2018/10/14/iUkrE6.md.png)](https://imgchr.com/i/iUkrE6)

     ![iUksUK.png](https://s1.ax1x.com/2018/10/14/iUksUK.png)

     ![iUky4O.png](https://s1.ax1x.com/2018/10/14/iUky4O.png)

     3. detail 专利详情
     4. [![iUkg8e.md.png](https://s1.ax1x.com/2018/10/14/iUkg8e.md.png)](https://imgchr.com/i/iUkg8e)

     5. collection 收藏页面

### 静态资源文件夹：

> 备注：patent_list.html 和 detail.html UI 静态页面非本人设计，但现在看到的是已经加工过的

##### CSS:

1. common-new.css 存放基本上所有的页面样式 ，因为这个页面初始静态设计非本人设计，里面注释较少，我修改的，如果在中间，我加了一点注释。其余修改的在代码最后。
2. old 文件夹不要动，那是最初版里面的 css 样式，如果删除，首页样式会被去掉。
3. reset.css 浏览器统一样式

##### JS:

1. birds.js、three.min.js、renderers 文件夹 均是为了首页 Canvas 所服务
2. new 文件夹 是新版本即 UI 设计过版本 所需要的各类 JS 库，而在 new 文件夹之外的 js，最好不要动，因为我担心 UI 的 juqery、bootstrap 版本和我用的不一样。
3. new 文件夹里 的 dist 是 Echart 库所需文件
4. new 文件夹里的 laydate 是 采用 layUI 的时间组件库
5. new 文件夹里 common.js 是原 UI 的大部分 js 逻辑处理
6. select-widget-min.js 为选择框所用 js
7. macarons.js 为 echarts，相关 js 库
8. 外部的 patentList.js 为 patent_list.html 做相关动态交互。

### 模板里 HTML：

1. patent_list.html 里面的 js 代码部分已挪至 patent_list.js 里面，剩下的不太好挪动，里面涉及 django 变量引用
2. 其余的 html 里面 js 文件 因代码量较少，就未统一化
3. html 页面中的 js 代码 有的函数重复，冗余（例如 ajax），但考虑多方面因素不想贸然统一

### 总结

patentMiner 项目是个比较大的、前后端不分离的项目，本人在大二正式接触，开发经验不足，Django 知识了解不多。原先自己设计了一套 bootstrap UI 界面，后又找了专门 UI 设计，在这期间学了如何写、画，做出明确的结构框架图设计文稿给乙方。也在期间走了许多莫名的弯路，面对诸多莫名的需求，Bug，不断地修改、调试成就今天。作为该项目前端首任开发者，我很惭愧，没能做到尽善尽美，包括上学期期末考试、暑假期间失恋、本人情感波动很大，事情也较多，无法专心做好这件事，故将项目的持续开发者交给后来者。如有一些问题，欢迎交流，批评指正！
