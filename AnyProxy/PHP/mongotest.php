<?php

$conn = new Mongo("mongodb://liujunshi:zzz520ikicker@103.235.224.224:27017/upload");
$db = $conn->selectDB("upload");

$collection2 = $db->UGCSourceSet;
$content_url = "http://mp.weixin.qq.com/s?__biz=MzA5MDE1ODM4OA==&mid=2650644499&idx=1&sn=f62d1bf7021029583daabafed506dfb5&chksm=8806e448bf716d5e220517e2a9fc8c37a5cf9d912d14559502f83906a8f48022f530a1a31597&scene=27#wechat_redirect";

$num = $collection2->count(array("content_url"=>$content_url));
if($num<=0){
    echo "hello1";
}



?>
