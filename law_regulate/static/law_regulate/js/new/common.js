$(function(){
	// 搜索条款
	$("#arrowLeft").click(function(){
		$(".wrapZLeft").hide();
		$(".wrapZLeft-sm").show();
		$(".wrapZCont").css({"margin-left":"80px"})
	});
	$("#arrowLeft-sm").click(function(){
		$(".wrapZLeft").show();
		$(".wrapZLeft-sm").hide();
		$(".wrapZCont").css({"margin-left":"300px"})
	});
	// 专利信息
	$("#arrowRight").click(function(){
		$(".wrapZRight").hide();
		$(".wrapZRight-sm").show();
		$(".wrapZCont2").css({"margin-right":"80px"})
	});
	$("#arrowRight-sm").click(function(){
		$(".wrapZRight").show();
		$(".wrapZRight-sm").hide();
		$(".wrapZCont2").css({"margin-right":"400px"})
	});
	// 历史记录
	// $("#arrowHistory").click(function(){
	// 	$(".wrapZHistory").hide();
	// 	$(".wrapZHistory-sm").show();
	// });
	// $("#arrowHistory-sm").click(function(){
	// 	$(".wrapZHistory-sm").hide();
	// 	$(".wrapZHistory").show();
	// });

	$("#arrowHistory").click(function(){
		$(".wrapZHistory").hide();
		$(".wrapZHistory-sm").show();
		$(".wrapZCont").css({"margin-right":"80px"})
	});
	$("#arrowHistory-sm").click(function(){
		$(".wrapZHistory").show();
		$(".wrapZHistory-sm").hide();
		$(".wrapZCont").css({"margin-right":"340px"})
	});

	$(".search_tab a").off("click").on("click",function(){
       var index = $(this).index();
       $(this).addClass("on").siblings().removeClass("on");
       $(".search-cont .search-pane").eq(index).addClass("active").siblings().removeClass("active");
    });

    $(".shengbox2>.search_tab>a").off("click").on("click",function(){
       var index = $(this).index();
       $(this).addClass("on").siblings().removeClass("on");
       $(".shengbox2 .search-cont>.search-pane").eq(index).addClass("active").siblings().removeClass("active");
    });

    $("#serTab>a").off("click").on("click",function(){
       var index = $(this).index();
       $(this).addClass("on").siblings().removeClass("on");
       $("#serTab-cont>.search-pane").eq(index).addClass("active").siblings().removeClass("active");
    });

    $(".admininfo").on("click", function(e){
        if($(this).next().is(":hidden")){
            $(this).next().show();
        }else{
            $(this).next().hide();
        }

        $(document).one("click", function(){
            $(".dropdown-menu").hide();
        });

        e.stopPropagation();
    });
    $(".dropdown-menu").on("click", function(e){
        e.stopPropagation();
    });


    $(".dropdown-menu li").click(function(event){
    	$(".dropdown-menu").hide();
    });


    $(".topSearch>input").focus(function(){
	    $(this).parent().css("border","1px solid #1baf9a");
	});
	$(".topSearch>input").blur(function(){
		$(this).parent().css("border","1px solid #f3f3f3");
	});

	$(".searchbar>input").focus(function(){
	    $(this).parent().css("border","1px solid #1baf9a");
	});
	$(".searchbar>input").blur(function(){
		$(this).parent().css("border","1px solid #f3f3f3");
	});


	// 语言
	$(".language li").click(function(event){
    	$(this).addClass('active').siblings().removeClass('active');
    });
    // 折叠
    $(".Toggle .ToggleBtn").click(function(event){
    	var yztable=$(this).parent().find('.yzTable');
    	var Toggle=$(this).parent();
    	if(yztable.is(":hidden")){
    		$(this).find("i").removeClass('fa-angle-double-up').addClass('fa-angle-double-down');
    	}else{
    		$(this).find("i").removeClass('fa-angle-double-down').addClass('fa-angle-double-up');

    	}
    	yztable.slideToggle("slow");
    });

    $(".btn-see").click(function(){
    	$(".btn-seed").show();
    	$(this).hide();
	})
	$("#adv-search").click(function(){
		// $(".advanced-search").css("display","block");
		// $(".advanced-search").addClass("animated");
		// $(".advanced-search").addClass("fadeInDown");
		if($(".advanced-search").css("display")=="none"){
			$(".advanced-search").css("display","block");
			$(".advanced-search").addClass("animated");
			$(".advanced-search").addClass("fadeInDown");
			$(".advanced-search").removeClass("fadeOut");
			$("#adv-logo").removeClass("fa-sort-desc");
			$("#adv-logo").addClass("fa-sort-asc");
			$("#adv-logo").removeClass("lineh-4");
			$("#adv-logo").addClass("lineh-1");
			$(".trans").removeClass("height-30");
			$(".trans").addClass("height-400");
		}
		else if($(".advanced-search").css("display")=="block"){
			$(".advanced-search").css("display","none");
			$(".advanced-search").removeClass("fadeInDown");
			$(".advanced-search").addClass("fadeOut");
			$("#adv-logo").removeClass("fa-sort-asc");
			$("#adv-logo").addClass("fa-sort-desc");
			$("#adv-logo").removeClass("lineh-1");
			$("#adv-logo").addClass("lineh-4");
			$(".trans").removeClass("height-400");
			$(".trans").addClass("height-30");
		}


		
	})
	 $("#adv-submit").click(function () {
		$(".advanced-search input").each(function () {
			// if(!$(".advanced-search div input").attr("value")){
			// 	alert(456);
			// 	$("#hiddenfg").attr("value")=0;
			// }
			// else{
			// 	alert(123);
			// 	$("#hiddenfg").attr("value")=1;
			// }
			
			 if($(this).val()==""){
	         	$("#hiddenfg").attr("value","0");
			 }
			 else{
				 $("#hiddenfg").attr("value","1");
				 return false;
			 }
			
			
		})

		
	 })
	var result1 = window.matchMedia('(min-width:1200px)');
	var result2 = window.matchMedia('(min-width:992px)');
	var result3 = window.matchMedia('(min-width:768px)');
      if(result1.matches) {
            console.log("大屏幕(>=1200)");
        }else if(result2.matches){
			$(".bg").remove();
			$(".index-logo").remove();
        }else if(result3.matches){
			$(".bg").remove();
			$(".index-logo").remove();
        }else{
			$(".bg").remove();
			$(".index-logo").remove();
        }

});


