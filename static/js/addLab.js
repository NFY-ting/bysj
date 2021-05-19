$(document).ready(function () {
  imgUrl = '';
  // 初始化上传图片插件
  $("#zyupload").zyUpload({
    width: "650px",                 // 宽度
    height: "200px",                 // 宽度
    itemWidth: "140px",                 // 文件项的宽度
    itemHeight: "115px",                 // 文件项的高度
    url: "uploadImg",  // 上传文件的路径
    fileType: ['png', 'jpg', 'JPG', 'PNG', 'bmp', "jpeg"],// 上传文件的类型
    fileSize: 51200000,                // 上传文件的大小
    multiple: false,                    // 是否可以多个文件上传
    dragDrop: false,                    // 是否可以拖动上传文件
    tailor: false,                    // 是否可以裁剪图片
    del: true,                    // 是否可以删除文件
    finishDel: false,  				  // 是否在上传文件完成后删除预览
    /* 外部获得的回调接口 */
    onSelect: function (selectFiles) {    // 选择文件的回调方法  selectFile:当前选中的文件  allFiles:还没上传的全部文件
      console.info("当前选择了以下文件：");
      console.info(selectFiles);
    },
    onDelete: function (file) {              // 删除一个文件的回调方法 file:当前删除的文件  files:删除之后的文件
      console.info("当前删除了此文件：");
      console.info(file.name);
    },
    onSuccess: function (file, response) {          // 文件上传成功的回调方法
      // if (response.status) {
      layer.msg("上传成功", { icon: 1 });
      imgUrl = response;
      console.log(imgUrl);
    },
    onFailure: function (file, response) {          // 文件上传失败的回调方法
      layer.msg("上传失败", { icon: 5 });
      console.info(file.name);
    },
    onComplete: function (response) {           	  // 上传完成的回调方法
      console.info("文件上传完成");
      console.info(response);
    }
  });
  layui.use(['form', 'layedit', 'laydate'], function () {
    var form = layui.form,
      layer = layui.layer;
    //监听提交
    form.on('submit(addForm)', function (data) {
      if (imgUrl == '') {
        layer.msg("请先上传封面图片！", { icon: 5 });
      } else {
        data.field.lab_img = imgUrl;
        $.ajax({
          url: 'addLab',
          type: 'post',
          data: JSON.stringify(data.field),
          contentType: 'application/json',
          dataType: 'json',
          success: function (data) {
            if (data.status) {
              layer.msg("添加成功", { icon: 1 });
              $("#addFOrm")[0].reset();
              layui.form.render();
              $(".file_del").trigger('click');
            } else {
              layer.msg(data.info, { icon: 5 });
            }
          },
          error: function (er) {
            layer.msg(er, { icon: 5 });
          }
        });

      }
      return false;
    });
  });

});