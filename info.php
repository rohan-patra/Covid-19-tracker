<?php
	exec("./check ".$_GET['code']."",$o);
	echo "<pre>" . json_encode($o) . "</pre>";
?>
