<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Twiseless</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="stylesheet" type="text/css" href="/static/css/twiseless.css" /> 
    <!--[if IE]>
    <script type="text/javascript" src="/static/js/Jit/Extras/excanvas.js"></script>
    <![endif]-->
    <script type="text/javascript" src="/static/js/jquery-1.5.1.min.js"></script> 
    <script type="text/javascript" src="/static/js/Jit/jit-yc.js"></script> 
    <script type="text/javascript" src="/static/js/twiseless.js"></script> 
    <script type="text/javascript">
      $(document).ready(function() {
        $("#viz").twiseless("render");
      });
    </script>
  </head>
  <body>
    <div id="tweets">
    </div>
    <div id="viz">
    </div>
  </body>
</html>