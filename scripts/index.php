<?php
$path = $_SERVER['DOCUMENT_ROOT']."/../files/"; // change the path to fit your websites document structure
$id = $path.$_GET['id'];
$name = $_GET['name'];

if ($fd = fopen ($id, "r")) {
    $fsize = filesize($id);
    $path_parts = pathinfo($id);
    if(isset($path_parts["extension"])) {
        $ext = strtolower($path_parts["extension"]);
    }
    else {
        $ext = "";
    }
    switch ($ext) {
        case "pdf":
        header("Content-type: application/pdf"); // add here more headers for diff. extensions
        header("Content-Disposition: attachment; filename=\"".$name."\""); // use 'attachment' to force a download
        break;
        default;
        header("Content-type: application/octet-stream");
        header("Content-Disposition: filename=\"".$name."\"");
    }
    header("Content-length: $fsize");
    header("Cache-control: private"); //use this to open files directly
    while(!feof($fd)) {
        $buffer = fread($fd, 2048);
        echo $buffer;
    }
}
fclose ($fd);
exit;
?>
