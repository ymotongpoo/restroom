<!-- -*- mode: html; coding:utf-8 -*- -->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
 "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns:py="http://genshi.edgewall.org/"
	  lang="ja">
  <head>
	<meta name="author" content="ymotongpoo -- http://d.hatena.ne.jp/ymotongpoo/"/>
	<link rel="stylesheet" href="style.css" type="text/css" media="screen"/>
	<title>よんだ？</title>
  </head>
  <body>
	<div class="banner">
	  <img src="Yonda.png"/>
	</div>

	<div class="ranking">
	  <h3>ホット「あとでよむ」エントリ</h3>
	  <table>
		<tr>
		  <td>タイトル</td>
		  <td>はてブ</td>
		  <td>Livedoor</td>
		  <td>Buzzurl</td>
		</tr>
		<tr py:for="bookmark in hotentry">
		  <td>
			<a href="${bookmark.url}">${bookmark.title}</a>
		  </td>
		  <td>
			<img src="http://b.hatena.ne.jp/entry/image/normal/${bookmark.url}"/>
		  </td>
		  <td>
			<img src="http://image.clip.livedoor.com/counter/${bookmark.url}"/>
		  </td>
		  <td>
			<img src="http://api.buzzurl.jp/api/counter/${bookmark.url}"/>
		  </td>
		</tr>
	  </table>
	</div>

	<div class="ranking">
	  <h3>人気「あとでよむ」エントリ</h3>
	  <table>
		<tr>
		  <td>タイトル</td>
		  <td>はてブ</td>
		  <td>Livedoor</td>
		  <td>Buzzurl</td>
		</tr>
		<tr py:for="bookmark in bookmarks">
		  <td>
			<a href="${bookmark.url}">${bookmark.title}</a>
		  </td>
		  <td>
			<img src="http://b.hatena.ne.jp/entry/image/normal/${bookmark.url}"/>
		  </td>
		  <td>
			<img src="http://image.clip.livedoor.com/counter/${bookmark.url}"/>
		  </td>
		  <td>
			<img src="http://api.buzzurl.jp/api/counter/${bookmark.url}"/>
		  </td>
		</tr>
	  </table>
	</div>
	
	<!-- Google Analytics -->
	<script type="text/javascript">
	  var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
	  document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
	</script>
	<script type="text/javascript">
	  try {
	  var pageTracker = _gat._getTracker("UA-6420772-2");
	  pageTracker._trackPageview();
	  } catch(err) {}
	</script>
  </body>
</html>
