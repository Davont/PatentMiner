/*本js文件负责自适应，使得网页在左右拉伸时候字体自适应*/
(function () {
    var calc =function () {
        var docElement=document.documentElement;
        var clientWidthValue = docElement.clientWidth>750?750:docElement.clientWidth;
        docElement.style.fontSize=20*(clientWidthValue/375)+'px';
    }
    calc();
    window.addEventListener('resize',calc);
})();