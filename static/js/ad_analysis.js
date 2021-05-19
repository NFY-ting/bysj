layui.use(['layer', 'echarts'], function () {
    var $ = layui.jquery,
        echarts = layui.echarts;
    $(document).ready(function () {
        /**
       * 实验统计
       */
        // 基于准备好的dom，初始化echarts实例
        var echartsRecords = echarts.init(document.getElementById('echarts-records'), 'walden');
        var optionRecords = {
            // 统计图标题
            title: {
                text: '实验统计',
                subtext: '完成率'
            },
            // 提示框组件
            tooltip: {
                // 是否显示提示框组件：坐标轴触发
                trigger: 'axis'
            },
            // 展现了不同系列的标记，颜色和名字。可以通过点击图例控制哪些系列不显示
            legend: {
                data: [],
                show: true
            },
            // 直角坐标系底板
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            // 工具栏组件
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            // X 轴
            xAxis: {
                // 数组每项表示一个组件实例，用 type 描述“子类型”
                type: 'category',
                boundaryGap: true,
                data: []
            },
            // Y轴
            yAxis: {
                type: 'value',
                name: '完成率'
            },
            // series是指：一组数值以及他们映射成的图
            // echarts 里series.type就是图表类型。line（折线图）
            series: [
                {
                    type: 'bar',
                    data: [],
                    showBackground: true,
                    // barWidth:'10%',
                    barWidth: 30, //柱图宽度

                }
            ]
        };
        // 获取数据
        $.ajax({
            type: 'get',
            data: '',
            contentType: 'application/json',
            dataType: 'json',
            url: 'analysis_lab',
            success: function (resp) {
                if (resp.status) {      //登录成功
                    optionRecords.legend.data = resp.legend;
                    optionRecords.xAxis.data = resp.legend;
                    // optionRecords.series[0].name = resp.legend;
                    optionRecords.series[0].data = resp.data;
                }
                console.log(optionRecords);
                // 调用 setOption 将 option 输入 echarts，然后 echarts 渲染图表。
                echartsRecords.setOption(optionRecords);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                // 状态码
                console.log(XMLHttpRequest.status);
                // 状态
                console.log(XMLHttpRequest.readyState);
                // 错误信息
                alert(textStatus);
            }
        });


        // echarts 窗口缩放自适应
        window.onresize = function () {
            echartsRecords.resize();
        }
    });
});
