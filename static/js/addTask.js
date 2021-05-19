$(document).ready(function () {
  // select
  layui.use(['form', 'table'], function () {
    var form = layui.form,
      table = layui.table;
    //添加任务------监听班级下拉框
    form.on('select(class)', function (data) {
      checkClass = { "class_id": data.value }
      $('#labtory').html('');           /* 清空 初始化 */
      if (data.value == null) {
        el = '<option value="">请先选择班级</option>';
        $('#labtory').append(el);
        layui.form.render('select');
        return false;
      }
      // 根据班级选择实验
      $.ajax({
        url: 'addTask',
        type: 'post',
        data: JSON.stringify(checkClass),
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
          // console.log(data);
          if (data.status) {
            for (const lab of data.data) {
              el = '<option value=' + lab.lab_id + '>' + lab.lab_name + '</option >';
              $('#labtory').append(el);
            }
            layui.form.render('select');
          } else {
            layer.msg(data.info, { icon: 5 });
          }
        }
      });
      return false;
    });
    // 添加任务------post
    form.on('submit(addForm)', function (data) {
      if (data.field.class_id == '' || data.field.lab_id == '') {
        layer.msg("请先选择班级、实验", { icon: 5 });
        return false;
      } else {
        $.ajax({
          url: 'postTask',
          type: 'post',
          data: JSON.stringify(data.field),
          contentType: 'application/json',
          dataType: 'json',
          success: function (data) {
            if (data.status) {
              layer.msg(data.info, { icon: 1 });
              $("select[name='lab_id']").val("");
              $('#labtory').html('');
              form.render('select');
              $("#refr").trigger('click');
            } else {
              layer.msg(data.info, { icon: 5 });
            }
          }
        });
      }
      return false;            /*  如果使用ajax交互，必须return false 否则会提交两次数据 */
    });
    // 查看任务-----加载表格 
    layer.load(2);
    table.render({
      elem: '#currentTableId',
      url: '/forTask',
      toolbar: '#toolbarDemo',
      defaultToolbar: ['exports', 'print'],
      cols: [[
        { type: "numbers", width: 70 },
        { field: 'class_id', width: 140, title: '班号', sort: true },
        { field: 'class_name', miniWidth: 150, title: '班级' },
        { field: 'lab_id', width: 110, title: '实验号', sort: true },
        { field: 'lab_name', miniWidth: 150, title: '实验名' },
        { field: 'num', width: 120, title: '完成人数', sort: true },
        { field: 'rate', width: 120, title: '完成比例', sort: true},
        { title: '操作', width: 100, toolbar: '#currentTableBar', align: "center" }
      ]], done: function () {
        layer.closeAll('loading');
      },
      limit: 10,
      page: true,
      skin: 'line'
    });
    /**
     * toolbar监听事件
     */
    table.on('toolbar(currentTableFilter)', function (obj) {
      if (obj.event === 'refresh') {  // 监听刷新操作
        table.reload('currentTableId', {
          url: '/forTask',
          page: {
            curr: 1       ////重新从第 1 页开始
          }
        });
      }
    });
    // 删除任务
    table.on('tool(currentTableFilter)', function (obj) {
      var data = obj.data;
      if (obj.event === 'del') {
        layer.confirm('真的删除该任务吗？', function (index) {
          $.ajax({
            url: 'delTask',
            type: 'post',
            data: JSON.stringify(obj.data),
            contentType: 'application/json',
            dataType: 'json',
            success: function (data) {
              if (data.status) {
                layer.msg(data.info, { icon: 1 });
                $("#refr").trigger('click');
              } else {
                layer.msg(data.info, { icon: 5 });
              }
            }
          });
          layer.close(index);
        });
      }
    });
  });
});