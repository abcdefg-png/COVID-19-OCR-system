<?php
header("Content-type: text/html; charset=utf-8");
$upload_file = $_FILES["file"];
$upload_name = $_POST["name"];
$store_dir = 'hesuan/Xinan/';  // 改！！！！！1
if($upload_file["error"]>0){
    // echo "错误：".$file["error"];
    if($upload_file["error"]==4){
        echo "<script>alert('请选择图片提交');
        location='hesuan.html'
                </script>";
    }         
    }// 链接改！！！！！！
if($upload_name==null)
    {
        echo "<script>alert('请输入学号');
        location='hesuan.html'
                </script>";
    }
else{
        $arr = ".jpg";
        $new_name ="{$upload_name}{$arr}";
        $upload_file["name"] = $new_name;
        $name = iconv('utf-8','gbk',"hesuan/Xinan/".$upload_file["name"]); // 改！！！！！
        if(move_uploaded_file($upload_file['tmp_name'],$name)){
             move_uploaded_file($upload_file['tmp_name'],$store_dir.$new_name);
             echo "<script>alert('提交成功');
                    location='hesuan.html';
                </script>";
        }                                       
        else{
             echo "<script>alert('提交失败');
                 location='hesuan.html';
             </script>";
        }

  
}
?>