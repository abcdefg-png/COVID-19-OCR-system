<?php
header("Content-type: text/html; charset=utf-8");
$userName='';
$passWord='';
$host='localhost';
$dataBase='homework';
$tbname='data1';
$conn=mysqli_connect($host,$userName,$passWord,$dataBase);
if (mysqli_connect_errno($conn)) 
{ 
    echo "连接 MySQL 失败: " . mysqli_connect_error(); 
} 
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
        $sql="select * from {$tbname} where username='$upload_name' ";
        $result=mysqli_query($conn,$sql);
        $row = mysqli_fetch_assoc($result);
        if ($row > 0) {
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
        else{
        echo "<script>alert('学号在数据库中不存在');

             </script>";
        }

  
?>
