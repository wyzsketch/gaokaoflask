/**
 * ECharts图表逻辑
 */

let chartInstance = null;

// 初始化图表
function initChart() {
    const chartDom = document.getElementById('chartContainer');
    chartInstance = echarts.init(chartDom);

    // 默认空图表
    const option = getDefaultOption();
    chartInstance.setOption(option);

    // 响应式
    window.addEventListener('resize', function() {
        if (chartInstance) {
            chartInstance.resize();
        }
    });
}

// 获取默认配置
function getDefaultOption() {
    return {
        title: {
            text: '历年录取位次趋势与2026预测',
            left: 'center',
            textStyle: {
                fontSize: 16,
                fontWeight: 'bold',
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                let result = params[0].axisValue + '年<br/>';
                params.forEach(function(item) {
                    if (item.value !== null && item.value !== undefined && !isNaN(item.value)) {
                        result += item.marker + item.seriesName + ': ' + item.value + '位<br/>';
                    }
                });
                return result;
            }
        },
        legend: {
            data: ['历年录取位次', '趋势线', '预测中位', '预测区间'],
            top: 30
        },
        grid: {
            left: '8%',
            right: '8%',
            bottom: '10%',
            top: '18%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            name: '年份',
            nameLocation: 'middle',
            nameGap: 30,
            data: [],
            axisLine: {
                lineStyle: { color: '#666' }
            },
            axisLabel: {
                fontSize: 12
            }
        },
        yAxis: {
            type: 'value',
            name: '位次',
            nameLocation: 'middle',
            nameGap: 50,
            inverse: true, // 位次越小越好，所以反转Y轴
            axisLine: {
                lineStyle: { color: '#666' }
            },
            axisLabel: {
                fontSize: 12,
                formatter: function(value) {
                    if (value >= 10000) {
                        return (value / 10000).toFixed(1) + '万';
                    }
                    return value;
                }
            },
            splitLine: {
                lineStyle: {
                    type: 'dashed',
                    color: '#e0e0e0'
                }
            }
        },
        series: [
            {
                name: '历年录取位次',
                type: 'line',
                data: [],
                smooth: true,
                symbol: 'circle',
                symbolSize: 8,
                lineStyle: {
                    width: 3,
                    color: '#4361ee'
                },
                itemStyle: {
                    color: '#4361ee',
                    borderWidth: 2,
                    borderColor: '#fff'
                },
                label: {
                    show: true,
                    position: 'top',
                    formatter: '{c}位',
                    fontSize: 11,
                    color: '#4361ee'
                }
            },
            {
                name: '趋势线',
                type: 'line',
                data: [],
                smooth: true,
                symbol: 'none',
                lineStyle: {
                    width: 2,
                    type: 'dashed',
                    color: '#9ca3af'
                }
            },
            {
                name: '预测中位',
                type: 'line',
                data: [],
                symbol: 'diamond',
                symbolSize: 12,
                lineStyle: {
                    width: 3,
                    type: 'dashed',
                    color: '#e63946'
                },
                itemStyle: {
                    color: '#e63946',
                    borderWidth: 2,
                    borderColor: '#fff'
                },
                label: {
                    show: true,
                    position: 'right',
                    formatter: '{c}位',
                    fontSize: 12,
                    fontWeight: 'bold',
                    color: '#e63946'
                }
            },
            {
                name: '预测区间',
                type: 'line',
                data: [],
                stack: 'confidence-band',
                symbol: 'none',
                lineStyle: { opacity: 0 },
                areaStyle: {
                    color: 'rgba(46, 196, 182, 0.25)'
                },
                tooltip: { show: false }
            },
            {
                name: '预测区间上限',
                type: 'line',
                data: [],
                symbol: 'none',
                lineStyle: {
                    width: 2,
                    type: 'dotted',
                    color: '#2ec4b6'
                },
                tooltip: { show: false }
            },
            {
                name: '预测区间下限',
                type: 'line',
                data: [],
                symbol: 'none',
                lineStyle: {
                    width: 2,
                    type: 'dotted',
                    color: '#2ec4b6'
                },
                tooltip: { show: false }
            }
        ]
    };
}

// 更新图表数据
function updateChart(echartsData) {
    if (!chartInstance || !echartsData) return;

    const xData = echartsData.xAxis || [];
    const series = echartsData.series || {};

    // 计算区间填充数据
    const upBand = series.predict_up || [];
    const downBand = series.predict_down || [];

    // 区间下限到上限之间的填充（用于stack方式）
    // 这里我们用另一种方式：直接用areaStyle的上下限
    const bandData = [];
    for (let i = 0; i < xData.length; i++) {
        if (upBand[i] !== null && upBand[i] !== undefined && !isNaN(upBand[i])) {
            bandData.push(downBand[i] - upBand[i]);
        } else {
            bandData.push(null);
        }
    }

    const option = {
        xAxis: {
            data: xData
        },
        series: [
            {
                name: '历年录取位次',
                data: series.history || []
            },
            {
                name: '趋势线',
                data: series.trend || []
            },
            {
                name: '预测中位',
                data: series.predict_mid || []
            },
            {
                name: '预测区间',
                data: upBand.map(function(val, i) {
                    if (val !== null && val !== undefined && !isNaN(val)) {
                        return val;
                    }
                    return null;
                }),
                stack: 'band',
                lineStyle: { opacity: 0 },
                areaStyle: {
                    color: 'rgba(46, 196, 182, 0.2)'
                },
                symbol: 'none'
            },
            {
                name: '预测区间下限',
                data: downBand.map(function(val, i) {
                    if (val !== null && val !== undefined && !isNaN(val)) {
                        return val - (upBand[i] || 0);
                    }
                    return null;
                }),
                stack: 'band',
                lineStyle: {
                    width: 2,
                    type: 'dotted',
                    color: '#2ec4b6'
                },
                areaStyle: {
                    color: 'rgba(46, 196, 182, 0.25)'
                },
                symbol: 'none'
            }
        ]
    };

    chartInstance.setOption(option, true);

    // 重新设置完整配置以保留样式
    const fullOption = getDefaultOption();
    fullOption.xAxis.data = xData;
    fullOption.series[0].data = series.history || [];
    fullOption.series[1].data = series.trend || [];
    fullOption.series[2].data = series.predict_mid || [];

    // 区间填充 - 使用更简单的方式
    // 用两个line，一个是上边界（透明线+底部到上边界的填充），一个是下边界
    // 这里简化处理，直接展示上下限两条虚线
    fullOption.series[3].data = series.predict_up || [];
    fullOption.series[3].name = '预测上限';
    fullOption.series[3].symbol = 'none';
    fullOption.series[3].lineStyle = {
        width: 2,
        type: 'dotted',
        color: '#2ec4b6'
    };
    fullOption.series[3].areaStyle = null;
    fullOption.series[3].tooltip = { show: true };

    fullOption.series[4].data = series.predict_down || [];
    fullOption.series[4].name = '预测下限';
    fullOption.series[4].symbol = 'none';
    fullOption.series[4].lineStyle = {
        width: 2,
        type: 'dotted',
        color: '#2ec4b6'
    };
    fullOption.series[4].tooltip = { show: true };

    // 移除第5、6个
    fullOption.series = fullOption.series.slice(0, 5);

    fullOption.legend.data = ['历年录取位次', '趋势线', '预测中位', '预测上限', '预测下限'];

    chartInstance.setOption(fullOption, true);

    // 添加区间填充效果
    addConfidenceBand(series.predict_up, series.predict_down, xData.length);
}

// 添加置信区间填充（使用markArea）
function addConfidenceBand(upData, downData, xLength) {
    if (!chartInstance || !upData || !downData) return;

    // 找到预测点的索引
    let predictIndex = -1;
    for (let i = 0; i < upData.length; i++) {
        if (upData[i] !== null && upData[i] !== undefined && !isNaN(upData[i])) {
            predictIndex = i;
            break;
        }
    }

    if (predictIndex < 0) return;

    const upVal = upData[predictIndex];
    const downVal = downData[predictIndex];

    chartInstance.setOption({
        series: [{
            name: '历年录取位次',
            markArea: {
                silent: true,
                itemStyle: {
                    color: 'rgba(46, 196, 182, 0.15)'
                },
                data: [[
                    {
                        xAxis: predictIndex,
                        yAxis: upVal,
                        label: {
                            show: true,
                            position: 'insideTop',
                            formatter: '上限 ' + upVal + '位',
                            fontSize: 11,
                            color: '#2ec4b6'
                        }
                    },
                    {
                        xAxis: predictIndex,
                        yAxis: downVal,
                        label: {
                            show: true,
                            position: 'insideBottom',
                            formatter: '下限 ' + downVal + '位',
                            fontSize: 11,
                            color: '#2ec4b6'
                        }
                    }
                ]]
            }
        }]
    });
}

// 清空图表
function clearChart() {
    if (chartInstance) {
        chartInstance.clear();
        chartInstance.setOption(getDefaultOption());
    }
}
