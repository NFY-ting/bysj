$(document).ready(function () {
  $("#choose").click(function (e) {
    $("#fileInp").trigger('click');
  });
  // 文件改变时 将文件名称显示到p元素中
  $('#fileInp').on('change', function (event) {
    if (event.target.files[0]) {
      fileName = event.target.files[0].name;
      $('#file-name').val(fileName);
    } else {
      $('#file-name').val('');
    }
  });
  $("#commit").click(function (e) {
    var data = new FormData($('#file_form')[0]);
    if ($('#file-name').val() == '') {
      layer.msg("请先选择文件", { icon: 5 });
      return '';
    }
    // 上传文件
    $.ajax({
      url: '/addTeacher',
      type: 'post',
      data: data,
      processData: false,  //表示不处理数据
      contentType: false,  //不设置数据类型
      dataType: 'json',
      success: function (data) {
        if (data.status) {
          layer.msg(data.info, { icon: 1 });
        } else {
          layer.msg(data.info, { icon: 5 });
        }
        $('#file-name').val('');
      }
    });
  });
  layui.use(['form', 'table'], function () {
    var $ = layui.jquery,
      form = layui.form,
      table = layui.table;

    table.render({
      elem: '#currentTableId',
      url: '/forTeacher',
      toolbar: '#toolbarDemo',
      defaultToolbar: ['exports', 'print'],
      cols: [[
        { type: "numbers", width: 70 },
        { field: 'tec_id', width: 120, title: '职工号', sort: true },
        { field: 'tec_name', width: 120, title: '姓名' },
        {
          field: 'sex', width: 120, title: '性别', templet: function (data) {
            if (data.sex == 'female') {
              return '女';
            } else if (data.sex == 'male') {
              return '男';
            } else {
              return ''
            }
          }
        },
        { field: 'email', minWidth: 120, title: '邮箱' },
        { title: '操作', width: 120, toolbar: '#currentTableBar', align: "center" }
      ]],
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
          url: '/forTeacher',
          page: {
            curr: 1       ////重新从第 1 页开始
          }
        });
      }
    });
// 查看教师授课情况
    table.on('tool(currentTableFilter)', function (obj) {
      var data = obj.data;
      if (obj.event === 'info') {
        info = {
          "tec_id": data.tec_id,
        };
        $.ajax({
          type: "POST",
          contentType: "application/json; charset=utf-8",
          dataType:'json',
          url: "classScore",
          data: JSON.stringify(info),
          success: function (response) {
            var tbody = ''
            for (const item of response.class_name) {
              tbody += '<tr>'+
              '<td>'+item.class_id+'</td>'+
              '<td>实验'+item.lab_id+'</td>'+
              '<td>'+item.rate+'</td>'+
            '</tr>'
            }
            if (response.status) {
              //示范一个公告层
              layer.open({
                type: 0,
                title: false,
                closeBtn: false,
                area: '400px;',
                shade: 0.8,
                id: 'LAY_layuipro', //设定一个id，防止重复弹出
                btn: ['确定'],
                content: '<table class="layui-table">'+
                '<colgroup> <col> <col> <col> </colgroup>'+
                '<thead> <tr> <th>班级</th> <th>实验</th> <th>完成率</th> </tr> </thead>'+
                '<tbody>'+tbody+'</tbody> </table>'
              });
            }
          }
        });
      }
    });

  });

});
