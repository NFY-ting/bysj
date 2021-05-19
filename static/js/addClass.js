
layui.use(['table', 'treetable', 'layer'], function () {
  var $ = layui.jquery;
  var table = layui.table;
  var treetable = layui.treetable;
  var layer = layui.layer;
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
        url: '/addClass',
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
  });
  // 渲染表格
  layer.load(2);
  treetable.render({
    treeColIndex: 1,
    treeSpid: -1,
    treeIdName: 'stu_id',
    treePidName: 'parentId',
    elem: '#munu-table',
    url: '/forClass',
    page: false,
    cols: [[
      { type: 'numbers' },
      { field: 'stu_id', minWidth: 120, title: '学号' },
      { field: 'stu_name', title: '姓名' },
      { field: 'email', minWidth: 120, title: '电子邮箱' },
      {
        field: 'sex', templet: function (data) {
          if (data.sex == 'female') {
            return '女';
          } else if (data.sex == 'male') {
            return '男';
          } else {
            return ''
          }
        }, title: '性别'
      },
      { templet: '#auth-state', width: 120, align: 'center', title: '操作' }
    ]],
    done: function () {
      layer.closeAll('loading');
    }
  });

  $('#btn-fold').click(function () {
    treetable.foldAll('#munu-table');
  });

  //监听操作
  table.on('tool(munu-table)', function (obj) {
    var data = obj.data;
    var layEvent = obj.event;
    if (layEvent === 'check') {
      info = {
        "stu_id": data.stu_id,
        "class_id": data.parentId
      };
      $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        url: "stuScore",
        data: JSON.stringify(info),
        success: function (response) {
          if (response.status) {
            if (response.code == '1') {
              complete = [];
              for (const i in response.complete) {
                complete[i] = "实验" + response.complete[i].lab_id;
              }
              not_complete = [];
              for (const i in response.not_complete) {
                not_complete[i] = "实验" + response.not_complete[i].lab_id;
              }
              html_str = '已完成实验：' + complete.join("、") + '<br><br>未完成实验：' + not_complete.join("、")
            } else {  
              // console.log(response.class_socre);
              var tbody = ''  
              // console.log(response.class_socre);
              response.class_socre.forEach(item => {
                  tbody += '<tr>'+
                    '<td>实验'+item.lab_id+'</td>'+
                    '<td>'+item.num+'</td>'+
                    '<td>'+item.rate+'%</td>'+
                  '</tr>'
                  // console.log(tbody);
              });
              html_str = '<table class="layui-table">'+
              '<colgroup> <col> <col> <col> </colgroup>'+
              '<thead> <tr> <th>实验</th> <th>完成人数</th> <th>完成率</th> </tr> </thead>'+
              '<tbody>'+tbody+'</tbody> </table>'          
            }
            
            //示范一个公告层
            layer.open({
              type: 0,
              title: false,
              closeBtn: false,
              area: '300px;',
              shade: 0.8,
              id: 'LAY_layuipro', //设定一个id，防止重复弹出
              btn: ['确定'],
              content: html_str
            });
          } else {

          }
        }
      });
    }
  });
});