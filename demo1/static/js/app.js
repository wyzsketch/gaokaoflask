/**
 * 预测页面交互逻辑
 */

// 全局状态
const state = {
    schoolId: null,
    schoolName: '',
    majorId: null,
    majorName: '',
    subjectType: 1, // 默认理科
    predictResult: null
};

// DOM元素
const $schoolInput = $('#schoolInput');
const $majorInput = $('#majorInput');
const $schoolList = $('#schoolList');
const $majorList = $('#majorList');
const $searchSchoolBtn = $('#searchSchoolBtn');
const $searchMajorBtn = $('#searchMajorBtn');
const $predictBtn = $('#predictBtn');
const $saveBtn = $('#saveBtn');
const $selectedInfo = $('#selectedInfo');
const $selectedSchoolText = $('#selectedSchoolText');
const $selectedMajorText = $('#selectedMajorText');
const $predictResultText = $('#predictResultText');
const $detailCard = $('#detailCard');

// 初始化
$(document).ready(function() {
    initEventListeners();
    initChart();
});

// 初始化事件监听
function initEventListeners() {
    // 学校搜索
    $searchSchoolBtn.on('click', searchSchools);
    $schoolInput.on('keypress', function(e) {
        if (e.which === 13) searchSchools();
    });
    $schoolInput.on('focus', function() {
        if ($schoolList.children().length > 0) {
            $schoolList.show();
        }
    });

    // 专业搜索
    $searchMajorBtn.on('click', searchMajors);
    $majorInput.on('keypress', function(e) {
        if (e.which === 13) searchMajors();
    });
    $majorInput.on('focus', function() {
        if ($majorList.children().length > 0) {
            $majorList.show();
        }
    });

    // 选科切换
    $('input[name="subjectType"]').on('change', function() {
        state.subjectType = parseInt($(this).val());
        // 切换选科后清空专业选择
        clearMajorSelection();
    });

    // 预测按钮
    $predictBtn.on('click', doPredict);

    // 保存按钮
    $saveBtn.on('click', savePredict);

    // 点击外部关闭下拉列表
    $(document).on('click', function(e) {
        if (!$(e.target).closest('#schoolInput, #schoolList').length) {
            $schoolList.hide();
        }
        if (!$(e.target).closest('#majorInput, #majorList').length) {
            $majorList.hide();
        }
    });
}

// 搜索学校
function searchSchools() {
    const name = $schoolInput.val().trim();
    if (name.length < 1) {
        alert('请输入学校名称关键词');
        return;
    }

    $.ajax({
        url: '/api/school/search',
        method: 'GET',
        data: { name: name, limit: 50 },
        success: function(res) {
            if (res.code === 0 && res.data && res.data.length > 0) {
                renderSchoolList(res.data);
                $schoolList.show();
            } else {
                alert('未找到匹配的学校');
            }
        },
        error: function() {
            alert('搜索学校失败，请检查数据库连接');
        }
    });
}

// 渲染学校列表
function renderSchoolList(schools) {
    $schoolList.empty();
    schools.forEach(function(school) {
        const $item = $('<div class="search-result-item"></div>');
        $item.text(school.name);
        $item.on('click', function() {
            selectSchool(school);
        });
        $schoolList.append($item);
    });
}

// 选择学校
function selectSchool(school) {
    state.schoolId = school.id;
    state.schoolName = school.name;
    $schoolInput.val(school.name);
    $schoolList.hide();

    // 启用专业搜索
    $majorInput.prop('disabled', false);
    $searchMajorBtn.prop('disabled', false);

    // 清空专业
    clearMajorSelection();

    // 更新已选信息
    updateSelectedInfo();
}

// 搜索专业
function searchMajors() {
    if (!state.schoolId) {
        alert('请先选择学校');
        return;
    }

    const name = $majorInput.val().trim();
    $.ajax({
        url: '/api/major/search',
        method: 'GET',
        data: {
            school_id: state.schoolId,
            type: state.subjectType,
            name: name,
            limit: 100
        },
        success: function(res) {
            if (res.code === 0 && res.data && res.data.length > 0) {
                renderMajorList(res.data);
                $majorList.show();
            } else {
                alert('未找到匹配的专业');
            }
        },
        error: function() {
            alert('搜索专业失败，请检查数据库连接');
        }
    });
}

// 渲染专业列表
function renderMajorList(majors) {
    $majorList.empty();
    majors.forEach(function(major) {
        const $item = $('<div class="search-result-item"></div>');
        $item.text(major.display_name || major.name);
        $item.on('click', function() {
            selectMajor(major);
        });
        $majorList.append($item);
    });
}

// 选择专业
function selectMajor(major) {
    state.majorId = major.id;
    state.majorName = major.name;
    $majorInput.val(major.display_name || major.name);
    $majorList.hide();

    // 启用预测和保存按钮
    $predictBtn.prop('disabled', false);
    $saveBtn.prop('disabled', false);

    // 更新已选信息
    updateSelectedInfo();

    // 自动加载已保存的预测记录
    loadPredictRecord();

    // 自动执行预测
    doPredict();
}

// 清空专业选择
function clearMajorSelection() {
    state.majorId = null;
    state.majorName = '';
    $majorInput.val('');
    $majorList.empty().hide();
    $predictBtn.prop('disabled', true);
    $saveBtn.prop('disabled', true);
    $predictResultText.text('---');
    $detailCard.hide();
    clearChart();
    updateSelectedInfo();
}

// 更新已选信息显示
function updateSelectedInfo() {
    if (state.schoolId || state.majorId) {
        $selectedInfo.show();
        $selectedSchoolText.text('🏫 ' + (state.schoolName || '未选择'));
        $selectedMajorText.text('📚 ' + (state.majorName || '未选择'));
    } else {
        $selectedInfo.hide();
    }
}

// 执行预测
function doPredict() {
    if (!state.schoolId || !state.majorId) {
        alert('请先选择学校和专业');
        return;
    }

    const adjMide = parseInt($('#adjMideInput').val()) || 0;
    const adjUp = parseInt($('#adjUpInput').val()) || 0;
    const adjDown = parseInt($('#adjDownInput').val()) || 0;

    $predictBtn.prop('disabled', true).text('预测中...');

    $.ajax({
        url: '/api/chart/get_data',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            school_id: state.schoolId,
            major_id: state.majorId,
            subject_type: state.subjectType,
            adj_mide: adjMide,
            adj_up: adjUp,
            adj_down: adjDown
        }),
        success: function(res) {
            if (res.code === 0 && res.data) {
                state.predictResult = res.data;
                renderPredictResult(res.data);
            } else {
                alert('预测失败: ' + (res.msg || '未知错误'));
            }
        },
        error: function() {
            alert('预测请求失败，请检查网络连接');
        },
        complete: function() {
            $predictBtn.prop('disabled', false).text('🔄 重新预测');
        }
    });
}

// 渲染预测结果
function renderPredictResult(data) {
    // 更新预测结果文字
    $predictResultText.text(data.predict_text || '---');

    // 更新图表
    updateChart(data.echarts);

    // 更新详细数据
    updateDetailTable(data);

    // 显示详情卡片
    $detailCard.show();
}

// 更新详细数据表
function updateDetailTable(data) {
    const predict = data.predict;

    // 历年数据
    const $tbody = $('#historyTableBody');
    $tbody.empty();
    if (predict.years && predict.history_ranks) {
        for (let i = 0; i < predict.years.length; i++) {
            const year = predict.years[i];
            const rank = predict.history_ranks[i];
            const score = predict.history_scores[i];
            const $tr = $('<tr></tr>');
            $tr.append('<td>' + year + '年</td>');
            $tr.append('<td>' + score + '分 / ' + rank + '位</td>');
            $tbody.append($tr);
        }
    }

    // 预测结果
    const subjectName = data.subject_name || '';
    $('#predictMidCell').text(predict.predict_score_mid + '分 / ' + predict.predict_mid + '位');
    $('#predictUpCell').text(predict.predict_score_up + '分 / ' + predict.predict_up + '位');
    $('#predictDownCell').text(predict.predict_score_down + '分 / ' + predict.predict_down + '位');
}

// 加载已保存的预测记录
function loadPredictRecord() {
    if (!state.schoolId || !state.majorId) return;

    $.ajax({
        url: '/api/predict/record',
        method: 'GET',
        data: {
            school_id: state.schoolId,
            major_id: state.majorId,
            subject_type: state.subjectType
        },
        success: function(res) {
            if (res.code === 0 && res.data) {
                const record = res.data;
                $('#adjMideInput').val(record.adj_mide || 0);
                $('#adjUpInput').val(record.adj_up || 0);
                $('#adjDownInput').val(record.adj_down || 0);
                $('#jhPredictInput').val(record.score_jh || 0);
            }
        }
    });
}

// 保存预测记录
function savePredict() {
    if (!state.schoolId || !state.majorId || !state.predictResult) {
        alert('请先进行预测');
        return;
    }

    const predict = state.predictResult.predict;
    const scoreJh = parseInt($('#jhPredictInput').val()) || 0;

    $.ajax({
        url: '/api/predict/save',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            school_id: state.schoolId,
            major_id: state.majorId,
            subject_type: state.subjectType,
            major_name: state.majorName,
            score_mide: predict.predict_score_mid,
            rank_mide: predict.predict_mid,
            score_up: predict.predict_score_up,
            rank_up: predict.predict_up,
            score_down: predict.predict_score_down,
            rank_down: predict.predict_down,
            score_jh: scoreJh,
            adj_mide: parseInt($('#adjMideInput').val()) || 0,
            adj_up: parseInt($('#adjUpInput').val()) || 0,
            adj_down: parseInt($('#adjDownInput').val()) || 0
        }),
        success: function(res) {
            if (res.code === 0) {
                alert('✅ 保存成功！');
            } else {
                alert('保存失败: ' + (res.msg || '未知错误'));
            }
        },
        error: function() {
            alert('保存请求失败，请检查网络连接');
        }
    });
}
