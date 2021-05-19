$(document).ready(function () {
  layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form,
      layer = layui.layer,
      layedit = layui.layedit,
      laydate = layui.laydate;
    let preMali;              //存储旧邮箱
    $.ajax({
      type: 'POST',
      data: '',
      url: "/tec_info",
      success: function (data) {
        if (data.status) {                        //加载成功
          if (data.sex == 'female')
            $('input[name="sex"]').val('女');
          else
            $('input[name="sex"]').val('男');
          $('input[name="tec_id"]').val(data.tec_id);
          $('form input[name="tec_name"]').val(data.tec_name);
          $('input[name="email"]').val(data.email);
          for (const cla of data.class_name) {    // 渲染授课班级的下拉框
            var str = '<option value=' + cla + '>' + cla + '</option>';
            $('select').append(str);
          }
          form.render();
          // $('input[name="class_name"]').val();

          preMali = data.email;
        } else {
          layer.msg(data.info, { icon: 5 });
        }
      }
    });
    $("#fixE").click(function () {
      if ($("#thisMali").attr("readonly")) {        //如果是不可编辑
        $("#thisMali").attr("readonly", false);
        $("#thisMali").val('');
      } else {                      //如果是可编辑
        $("#thisMali").attr("readonly", true);
        content = {
          'mail': $("#thisMali").val()
        };
        $.ajax({
          type: 'POST',
          data: content,
          url: "/fix_tecemail",
          success: function (data) {
            if (data.status) {                        //加载成功
              preMali = $("#thisMali").val();
              layer.msg(data.info, { icon: 1 });
            } else {
              $("#thisMali").val(preMali);
              layer.msg(data.info, { icon: 5 });
            }
          }
        });
      }
    });
  });
});