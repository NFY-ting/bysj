$(document).ready(function () {
  layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form,
      layer = layui.layer,
      laydate = layui.laydate;
    // 初始化加载数据
    let preMali;              //存储旧邮箱
    $.ajax({
      type: 'POST',
      data: '',
      url: "/info",
      success: function (data) {
        if (data.status) {                        //加载成功
          // layer.msg(data.info, { icon: 1 });
          if (data.sex == 'female')
            $('input[name="sex"]').val('女');
          else
            $('input[name="sex"]').val('男');
          $('input[name="stu_id"]').val(data.stu_id);
          $('form input[name="stu_name"]').val(data.stu_name);
          $('input[name="class_name"]').val(data.class_name);
          $('input[name="email"]').val(data.email);
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
          url: "/fix_email",
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