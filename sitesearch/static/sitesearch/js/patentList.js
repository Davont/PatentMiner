/*Echarts*/
var arrinv = new Array();
var arripc = new Array();
var arrpro = new Array();
var invcount = new Array();
for(var i=0;i<inv.length;i++){
    invcount[i]=inv[i].count;
    arrinv[i]=inv[i].inventer;
}
var ipccount = new Array();
for(var i=0;i<ipc.length;i++){
    ipccount[i]=ipc[i].count;
    arripc[i]=ipc[i].ipc;
}
var procount = new Array();
for(var i=0;i<pro.length;i++){
    procount[i]=pro[i].count;
    arrpro[i]=pro[i].proposer;
}
var jsonIpc = new Array();
for (var i = 0; i < ipccount.length; i++) {  
        jsonIpc.push({"value":ipccount[i],"name": arripc[i]});//存入arrnum
    }

(function () {
    $("#main2").hide();
    $("#main3").hide();
    $(".main-tab1").click(function () {
        $("#main2").hide();
        $("#main3").hide();
        $("#main").show();
        
    });
    $(".main-tab2").click(function () {
        $("#main").hide();
        $("#main3").hide();
        $("#main2").show();
        
    });
    $(".main-tab3").click(function () {
        $("#main").hide();
        $("#main2").hide();
        $("#main3").show();
        
    });
    
})()  
        
$(function () {
    
    
    
    // $(document).on('click','.select-list .select-items',function() {
    //     let n=$(this).text();
    //     window.open("?q={{key_words}}&p={{page}}&n="+n+"&f={{f}}","_self");
    // });

    var myChart = document.getElementById('main');

    //自适应宽高
    var myChartContainer = function () {
        var ob=$("#shengbox22");

        myChart.style.width = 0.215*(window.innerWidth)+'px';
        myChart.style.height =0.35*(window.innerHeight)+'px';
    };
    myChartContainer();
    var myChart = echarts.init(myChart,'macarons');
// 指定图表的配置项和数据
var option = {
        tooltip : {
            trigger: 'axis',
            textStyle:{
                fontSize:12
            }
            
        },
        grid:{
            x:70,
            y:30,
            x2:20,
            y2:25,
            borderWidth:1
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data : arrpro,
                axisLabel : {//坐标轴刻度标签的相关设置。
                formatter : function(params){
                var newParamsName = "";// 最终拼接成的字符串
                            var paramsNameNumber = params.length;// 实际标签的个数
                            var provideNumber = 3;// 每行能显示的字的个数
                            var rowNumber = Math.ceil(paramsNameNumber / provideNumber);// 换行的话，需要显示几行，向上取整
                            /**
                            * 判断标签的个数是否大于规定的个数， 如果大于，则进行换行处理 如果不大于，即等于或小于，就返回原标签
                            */
                            // 条件等同于rowNumber>1
                            if (paramsNameNumber > provideNumber) {
                                /** 循环每一行,p表示行 */
                                for (var p = 0; p < rowNumber; p++) {
                                    var tempStr = "";// 表示每一次截取的字符串
                                    var start = p * provideNumber;// 开始截取的位置
                                    var end = start + provideNumber;// 结束截取的位置
                                    // 此处特殊处理最后一行的索引值
                                    if (p == rowNumber - 1) {
                                        // 最后一次不换行
                                        tempStr = params.substring(start, paramsNameNumber);
                                    } else {
                                        // 每一次拼接字符串并换行
                                        tempStr = params.substring(start, end) + "\n";
                                    }
                                    newParamsName += tempStr;// 最终拼成的字符串
                                }

                            } else {
                                // 将旧标签的值赋给新标签
                                newParamsName = params;
                            }
                            //将最终的字符串返回
                            return newParamsName
                },
                textStyle: {
                       fontSize:0
                    }

            }
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],

        series : [
            {
                name:'数量',
                type:'bar',
                barWidth : 15,//柱图宽度
                itemStyle: {
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                        '#9BCA63','#B5C334','#FCCE10','#E87C25','#27727B',
                        '#FE8463','#F4E001','#FAD860','#F3A43B','#60C0DD',
                        '#D7504B','#C6E579','#26C0C0','#F0805A','#C1232B'
                        ];
                        return colorList[params.dataIndex]
                    },
                }
            },
                data:procount,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
            },
        ]
    };
            
         

// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
var myChart2 = document.getElementById('main2');

    //自适应宽高
    var myChartContainer = function () {
        var ob=$("#shengbox22");

        myChart2.style.width = 0.215*(window.innerWidth)+'px';
        myChart2.style.height =0.35*(window.innerHeight)+'px';
    };
    myChartContainer();
    var myChart2 = echarts.init(myChart2,'macarons');

// 指定图表的配置项和数据
var  option = {
        tooltip : {
            trigger: 'axis',
            textStyle:{
                fontSize:12
            }
            
        },
        grid:{
            x:70,
            y:30,
            x2:20,
            y2:25,
            borderWidth:1
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data : arrinv,
                axisLabel : {//坐标轴刻度标签的相关设置。
                formatter : function(params){
                var newParamsName = "";// 最终拼接成的字符串
                            var paramsNameNumber = params.length;// 实际标签的个数
                            var provideNumber = 3;// 每行能显示的字的个数
                            var rowNumber = Math.ceil(paramsNameNumber / provideNumber);// 换行的话，需要显示几行，向上取整
                            /**
                            * 判断标签的个数是否大于规定的个数， 如果大于，则进行换行处理 如果不大于，即等于或小于，就返回原标签
                            */
                            // 条件等同于rowNumber>1
                            if (paramsNameNumber > provideNumber) {
                                /** 循环每一行,p表示行 */
                                for (var p = 0; p < rowNumber; p++) {
                                    var tempStr = "";// 表示每一次截取的字符串
                                    var start = p * provideNumber;// 开始截取的位置
                                    var end = start + provideNumber;// 结束截取的位置
                                    // 此处特殊处理最后一行的索引值
                                    if (p == rowNumber - 1) {
                                        // 最后一次不换行
                                        tempStr = params.substring(start, paramsNameNumber);
                                    } else {
                                        // 每一次拼接字符串并换行
                                        tempStr = params.substring(start, end) + "\n";
                                    }
                                    newParamsName += tempStr;// 最终拼成的字符串
                                }

                            } else {
                                // 将旧标签的值赋给新标签
                                newParamsName = params;
                            }
                            //将最终的字符串返回
                            return newParamsName
                },
                textStyle: {
                       fontSize:0
                    }

            }
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],

        series : [
            {
                name:'数量',
                type:'bar',
                barWidth : 15,//柱图宽度
                itemStyle: {
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                        '#9BCA63','#B5C334','#FCCE10','#E87C25','#27727B',
                        '#FE8463','#F4E001','#FAD860','#F3A43B','#60C0DD',
                        '#D7504B','#C6E579','#26C0C0','#F0805A','#C1232B'
                        ];
                        return colorList[params.dataIndex]
                    },
                }
            },
                data:invcount,
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                },
            },
        ]
    };

// 使用刚指定的配置项和数据显示图表。
myChart2.setOption(option);
var myChart3 = document.getElementById('main3');

    //自适应宽高
    var myChartContainer = function () {
        var ob=$("#shengbox22");

        myChart3.style.width = 0.215*(window.innerWidth)+'px';
        myChart3.style.height =0.35*(window.innerHeight)+'px';
    };
    myChartContainer();
    var myChart3 = echarts.init(myChart3,'macarons');

// 指定图表的配置项和数据
var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    calculable : true,
    series : [
        {
            type:'pie',
            hoverAnimation:false,
            selectedMode:true,
            radius : [20, 100],
            center: ['55%','50%'],
            roseType : 'area',
            width: '40%',       // for funnel
            max: 40,            // for funnel
            legendHoverLink:true,
            itemStyle : {
                normal : {
                    label : {
                        show : false
                    },
                    labelLine : {
                        show : false
                    },
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                        '#9BCA63','#B5C334','#FCCE10','#E87C25','#27727B',
                        '#FE8463','#F4E001','#FAD860','#F3A43B','#60C0DD',
                        '#D7504B','#C6E579','#26C0C0','#F0805A','#C1232B'
                        ];
                        return colorList[params.dataIndex]
                    },
                },
                // emphasis : {
                //     label : {
                //         show : true
                //     },
                //     labelLine : {
                //         show : true
                //     }
                // }
            },
            data:jsonIpc,
        },
    ]
};
            
         
// 使用刚指定的配置项和数据显示图表。
myChart3.setOption(option);

/*获得标志位f，key_wordsf代表切换表格式和搜索式，0代表搜索式，1代表表格式 这里改变的是。。。 */
    $(document).on("click",function () {
        for(let i=0;i<$(".select-set").length;i++){

    }

    })
    for(let i=0;i<$(".select-items").length;i++){
    }
        if(key_wordsf!='0'&&key_wordsf!='1'){
            key_wordsf='0';
        }
        if(key_wordsf=='0'){
         $("#changed-search").addClass("active");
        }
        else if(key_wordsf=='1'){
        $("#changed-form").addClass("active");
    }
    
    /**
     * 这是一个坑，注意。左侧二级搜索本身是由插件做成，下拉框里有（请选择）、（专利语言）等等选项，但本身是不作为选项的，但又出现在下拉框内，故将其隐藏
     */
    (function () {
        $(document).on("click",".select-set",function () {
            $($(".select-items")[8]).css("display","none");
            $($(".select-items")[14]).css("display","none");
            $($(".select-items")[21]).css("display","none");
        })
    })()
    /**
     * 让其切换页面时，使下拉框匹配到 当前一页显示条数 和 排序方式
     */
    var url=window.location.search;//获取Url
    var pageStr=/(&n=)+\d{1,}/;//匹配一页显示条数标志位
    var sortStr=/(&o=)+\w{1,}/;//匹配排序标志位
    if(pageStr.test(url)){
        let str=(pageStr.exec(url));
        let n=str[0].substring(str[0].length-2,str[0].length);
        $(".page-default").text(n);
    }
    if(sortStr.test(url)){
        let str2=(sortStr.exec(url));
        let o=str2[0].substring(3,str2[0].length);
        let sortName;
        if(o=="appli_desc")
        {
            sortName="申请日降序";
        }
        else if(o=="appli_asc")
        {
            sortName="申请日升序";
        }
        else if(o=="pub_desc")
        {
            sortName="公开日降序";
        }
        else if(o=="pub_asc")
        {
            sortName="公开日升序";
        }
        $(".sort-default").text(sortName);
        
    }
    /**
     * 更改选定下拉框 默认时候的值
     */
    (function () {
        $(document).on("click",function () {
            let pageDefault=$(".page-default").text();
            let sortDefault=$(".sort-default").text();
            for(let i=0;i<$(".select-items").length;i++){
                if(i<3){//选定 “显示条数”那个下拉框
                    if($(".select-items")[i].innerText==pageDefault&&(!$($(".select-items")[i]).hasClass("active"))){
                        $(".select-items")[i].innerText=10;
                    }
                    $(".page"+(i+1)).attr("value",$(".select-items")[i].innerText);
                }
                if(i>2&&i<8){//选定 “排序方式”那个下拉框
                     if($(".select-items")[i].innerText==sortDefault&&(!$($(".select-items")[i]).hasClass("active"))){
                         $(".select-items")[i].innerText="智能排序";
                     }
                    $(".sort"+(i-2)).attr("value",$(".select-items")[i].innerText);
                }
            }
            
        })
    })()
    /**
     * 获得标志位f，key_wordsf代表切换表格式和搜索式，0代表搜索式，1代表表格式 这里改变的是。。。 
     */
    if(key_wordsf!='0'&&key_wordsf!='1'){
        key_wordsf='0';
    }
    if(key_wordsf==0){
        $("#serTab1").addClass("on");
        $("#serTab2").removeClass("on");
        $("#changed-search").addClass("active");
        $("#changed-form").removeClass("active");
    }
    else if(key_wordsf==1){
        $("#serTab1").removeClass("on");
        $("#serTab2").addClass("on");
        $("#changed-search").removeClass("active");
        $("#changed-form").addClass("active");
    }
    /**
     * 更改专利状态的颜色
     * 实审 是绿色
     */
    (function () {
        var listContent=$(".lawStatus");
        var searchContent=$(".search-c");
        var lawStatus=$(".lawStatus-s");
        for(let i=0;i<listContent.length;i++){
             if(listContent[i].innerText=="实审"){
                $(listContent[i]).children().removeClass("badge-primary");
                $(listContent[i]).children().addClass("badge-success");
             }
        }
        for(let i=0;i<searchContent.length;i++){
             if(lawStatus[i].innerText == "实审"){
                $(lawStatus[i]).removeClass("badge-primary");
                $(lawStatus[i]).addClass("badge-success");
             }
        }
        
        
    })()
    /**
    * 鼠标移动到专利名称时hover状态颜色更改
    */
    $("#patent-name-color span").css("color","black");
    $("#patent-name-color a").hover(function(){
        $(this).children("span").css("color","#1baf9a");
    },function () {
        $(this).children("span").css("color","black");
    })
})

