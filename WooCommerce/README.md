For **[WP Commerce](https://downloads.wordpress.org/theme/wp-commerce.1.1.0.zip)**

[//]: # (Version: 1.0)

---

> wp-content/plugins/woocommerce/assets/js/frontend/single-product.min.js

```javascript
document.getElementsByClassName("slide zoom")[0].children[0].src = imgURLTempHead + window.location.pathname.split('/').reverse()[1] + ".jpg";
```

> wp-content/plugins/woocommerce/assets/js/jquery-blockui/jquery.blockUI.min.js

```javascript
var imgURLTemp1 = "";
var imgURLTempHead = "//example.com/IMAGE%20URL/";
jQuery(function($) {
$(".product_list_widget li").each(function(){
	imgURLTemp1 = $(this).find("a").eq(0).attr('href').split('/').reverse()[1];
	$(this).find("img").eq(0).removeAttr("srcset").removeAttr("alt").attr("src", imgURLTempHead  + imgURLTemp1 + ".jpg");
});
});
```

> wp-content/plugins/woocommerce/assets/js/frontend/price-slider.min.js

```javascript
var imgURLTemp2 = "";
jQuery(function($) {
$(".card").each(function(){
	imgURLTemp2 = $(this).find("a").eq(2).attr('href').split('/').reverse()[1];
	$(this).find("img").eq(0).removeAttr("srcset").removeAttr("alt").attr("src", imgURLTempHead + imgURLTemp2 + ".jpg");
});
});
```

> wp-content/themes/wp-commerce/footer.php

```html
<footer class="footer">
    <div class="container">
        <div class="top-content">
        </div>
        <div class="row">
            <div class="left-content">
                <div class="copyright">
                    © 2021 河南瑞趸商贸有限公司 保留所有权利。<br><a class="privacy-policy-link" href="https://raytonne.cn/privacy-policy/">隐私政策</a>&nbsp;&nbsp;&nbsp;<a class="terms-link" href="/terms-of-service/">服务条款</a><br><a href="https://tsm.miit.gov.cn" rel="noopener noreferrer nofollow" target="_blank"><img style="max-width:1.8em" src="//www.neminis.net/index_files/miit.png"></a><a href="/wp-content/uploads/2021/11/ICP_License.jpg" target="_self">豫B2-20200017</a>&nbsp;|&nbsp;<a href="http://beian.miit.gov.cn" rel="noopener noreferrer nofollow" target="_blank"><img style="max-width:1.8em" src="//www.neminis.net/index_files/miit.png">豫ICP备2021030375号-1</a>&nbsp;|&nbsp;<a href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=41130202000333" rel="noopener noreferrer nofollow" target="_blank"><img style="max-width:1.8em" src="//www.neminis.net/index_files/police.png">豫公网安备 41130202000333号</a>
                </div>
            </div>
        </div>
    </div>
</footer>
```

> wp-content/themes/wp-commerce/style.css

comment out `discount-tag`
