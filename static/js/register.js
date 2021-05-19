//验证码的计时timer处理函数
var InterValObj; //timer变量，控制时间
var count = 60; //间隔函数，1秒执行
var curCount;//当前剩余秒数
function SetRemainTime() {
  if (curCount == 0) {
    window.clearInterval(InterValObj);//停止计时器
    $("#getCode").removeAttr("disabled");//启用按钮
    $("#getCode").text("重新发送");
  }
  else {
    curCount--;
    $("#getCode").attr("disabled", true);
    $("#getCode").text("重新发送(" + curCount + ")");
  }
}
//发送验证码
$("#getCode").click(function (e) {
  var pwd_email = $("input[name=email]").val();
  curCount = count;               //时间
  InterValObj = window.setInterval(SetRemainTime, 1000); //启动计时器，1秒执行一次
  document.getElementById("getCode").style.fontSize = 12 + 'px';
  var user = {
    "mail": pwd_email
  };
  $.ajax({
    type: 'POST',

    data: JSON.stringify(user),

    contentType: 'application/json',

    dataType: 'json',

    url: '/user/mailSend',

    success: function (data) {
      if (data.status) {      //登录成功
        alert("验证码发送成功，请注意查收！");
      } else {
        alert(data.msg);
      }

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
});

