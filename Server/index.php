<?php
// Version: 1.0

// Prerequisite:
//apt install php-gd -y

define("SITE_URL", "https://raytonne.com/");
define("ADMIN_PASSWORD", "YOUR_PASSWORD_HERE");

function variableExists($variableName) {
	if (!empty ($variableName) && !is_null ($variableName)) {
		return true;
	} else {
		return false;
	}
}

function png2jpg($filePath, $newFile) {
	if (exif_imagetype($filePath)) {
		$image = imagecreatefrompng($filePath);
		$bg = imagecreatetruecolor(imagesx($image), imagesy($image));
		imagefill($bg, 0, 0, imagecolorallocate($bg, 255, 255, 255));
		imagealphablending($bg, TRUE);
		imagecopy($bg, $image, 0, 0, 0, 0, imagesx($image), imagesy($image));
		imagedestroy($image);
		$quality = 50;
		imagejpeg($bg, $newFile, $quality);
		imagedestroy($bg);
		return true;
	} else {
		return false;
	}
}

if (isset($_POST["pwd"]) && $_POST["pwd"] === ADMIN_PASSWORD && isset($_POST["productID"]) && variableExists($_POST["productID"]) && isset($_POST["productImg"]) && isset($_POST["productPrice"]) && variableExists($_POST["productPrice"])) {
	if (substr($_POST["productImg"], -4) === ".jpg" || substr($_POST["productImg"], -4) === ".png") {
		if (file_exists($_POST["productID"] . ".jpg")) {
			exit("ERR");
		}
		$desiredImg = @file_get_contents($_POST["productImg"]);
		if ($desiredImg === false) {
			exit("ERR");
		} else {
			if (substr($_POST["productImg"], -4) === ".jpg") {
				file_put_contents($_POST["productID"] . ".jpg", $desiredImg);
			} else {
				file_put_contents($_POST["productID"] . ".png", $desiredImg);
				if (png2jpg($_POST["productID"] . ".png", $_POST["productID"] . ".jpg")) {
					unlink($_POST["productID"] . ".png");
				} else {
					exec("rm -R " . $_POST["productID"] . "*");
					exit("ERR");
				}
			}
		}
		$desiredImg = "./main.py -O new -I " . $_POST["productID"] . " -p " . $_POST["productPrice"];
		if (isset($_POST["productDesc"]) && variableExists($_POST["productDesc"])) {
			$desiredImg .= " -d '" . base64_encode(explode("productDesc=", file_get_contents("php://input"), 2)[1]) . "'";
		}
		if (exec($desiredImg) === "OK") {
			echo "OK";
			rename($_POST["productID"] . ".jpg", "/PATH/TO/YOUR/STATICFILES/" . $_POST["productID"] . ".jpg");
		} else {
			echo "ERR";
			unlink($_POST["productID"] . ".jpg");
		}
	} else {
		echo "ERR";
	}
} elseif (isset($_POST["pwd"]) && $_POST["pwd"] === ADMIN_PASSWORD && isset($_POST["delete"]) && $_POST["delete"] === "yes" && isset($_POST["productURL"])) {
	$desiredProduct = @file_get_contents($_POST["productURL"]);
	if ($desiredProduct === false || strpos($desiredProduct, "rel='shortlink' href='" . SITE_URL . "?p=") === false || strpos($desiredProduct, 'rel="canonical" href="' . SITE_URL . 'shop/') === false) {
		exit("ERR");
	} else {
		list($deleteID, $deleteid) = explode("rel='shortlink' href='" . SITE_URL . "?p=", explode('rel="canonical" href="' . SITE_URL . 'shop/', $desiredProduct, 2)[1], 2);
		$deleteID = explode("/\"", $deleteID, 2)[0];
		$deleteid = explode("'", $deleteid, 2)[0];
		if (variableExists($deleteID) && variableExists($deleteid)) {
			if (exec("./main.py -O delete -i " . $deleteid) === "OK") {
				echo "OK";
				unlink("/PATH/TO/YOUR/STATICFILES/" . $deleteID . ".jpg");
			} else {
				echo "ERR";
			}
		} else {
			echo "ERR";
		}
	}
} else {
	echo "ERR";
}
?>
