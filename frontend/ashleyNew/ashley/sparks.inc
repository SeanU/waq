<!DOCTYPE html>
<html>
  
  <head>
    <title>D3 Sparklines</title>
    <meta charset="utf-8">
    <script src="//d3js.org/d3.v3.min.js" charset="utf-8"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
    <link rel="stylesheet" type="text/css" href="sparklines.css"/>
  </head>
  
  <body>

    <div id="graph-container">

      <div class="label-wrapper">
        <div id="c1-label"><a href=https://en.wikipedia.org/wiki/Phlogiston target="_blank">Phlogiston</a></div>
        <div id="c2-label"><a href=https://en.wikipedia.org/wiki/Gnosis target="_blank">Gnosis</a></div>
        <div id="c3-label"><a href=https://en.wikipedia.org/wiki/Melange_(fictional_drug) target="_blank">Melange</a></div>
        <div id="c4-label"><a href=https://en.wikipedia.org/wiki/Adamantium target="_blank">Adamantium</a></div>
        <div id="c5-label"><a href=https://en.wikipedia.org/wiki/Ectoplasm_(paranormal) target="_blank">Ectoplasm</a></div>
        <div id="c6-label"><a href=https://en.wikipedia.org/wiki/Luminiferous_aether target="_blank">Luminiferous Aether</a></div>
        <div id="c7-label"><a href=https://en.wikipedia.org/wiki/Iocane target="_blank">Iocane Powder</a></div>
        <div id="c8-label"><a href=https://en.wikipedia.org/wiki/Kryptonite target="_blank">Kryptonite</a></div>
        <div id="c9-label"><a href=https://en.wikipedia.org/wiki/Philosophical_Mercury target="_blank">Philosophical Mercury</a></div>
        <div id="c10-label"><a href=https://en.wikipedia.org/wiki/Dilithium target="_blank">Dilithium</a></div>
      </div>

      <div class="col-wrapper" id="a-info-wrapper">
        <div class="title">Contaminants</div>
        <div class="sparkline-wrapper" id="sparkline-a-c1"></div>
        <div class="sparkline-wrapper" id="sparkline-a-c2"></div>
        <div class="sparkline-wrapper" id="sparkline-a-c3"></div>
        <div class="sparkline-wrapper" id="sparkline-a-c4"></div>
        <div class="sparkline-wrapper" id="sparkline-a-c5"></div>
        <div class="sparkline-wrapper" id="sparkline-b-c1"></div>
        <div class="sparkline-wrapper" id="sparkline-b-c2"></div>
        <div class="sparkline-wrapper" id="sparkline-b-c3"></div>
        <div class="sparkline-wrapper" id="sparkline-b-c4"></div>
        <div class="sparkline-wrapper" id="sparkline-b-c5"></div>
      </div>

    </div>
  </body>

  <script type="text/javascript" src="sparklines.js"></script>

</html>