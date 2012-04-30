<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>.:. Twiseless .:.</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link href="http://fonts.googleapis.com/css?family=Nunito" rel="stylesheet" type="text/css">
    <link rel="stylesheet" type="text/css" href="/static/css/twiseless.css" /> 
    <!--[if IE]>
    <script type="text/javascript" src="/static/js/Jit/Extras/excanvas.js"></script>
    <![endif]-->
    <script type="text/javascript" src="/static/js/jquery-1.7.2.min.js"></script> 
    <script type="text/javascript" src="/static/js/Jit/jit-yc.js"></script> 
    <script type="text/javascript" src="/static/js/twiseless.js"></script> 
    <script type="text/javascript">
      $(document).ready(function() {
        $("#viz").twiseless("render");
      });
    </script>
  </head>
  <body>
    <div id="container">
      <div id="header">
	<h1>:: Twiseless</h1>
      </div>
      <div id="content-container">
	<div id="content">
	  <div id="tweets"></div>
	</div>
	<div id="aside">
	  <div id="viz"></div>
	</div>
	<div id="footer">
	  <div id="footer-info">
	    &copy; Sylvain Hellegouarch, licensed under a <a href="https://github.com/Lawouach/Twiseless/blob/master/LICENSE">BSD license</a>.
	    Layout mostly taken from <a href="http://www.maxdesign.com.au/articles/css-layouts/two-fixed/">maxdesign</a>.
	  </div>
	</div>
      </div>
    </div>
  </body>
</html>
