Channel information
===================
    
<p style="font-family:arial">${info}</p>

#foreach ($channel in $channels)##
<div style="border:solid 2px white; padding-left:10px">
<div>
<b>${channel}</b><br/>
</div>
<div><a href="${channel}.inf.png"><img alt="${channel} steady state" src="${channel}.inf.png" height="250" width="300" style="padding:10px 35px 10px 0px"/></a>
<a href="${channel}.tau.png"><img alt="${channel} time course" src="${channel}.tau.png" height="250" width="300" style="padding:10px 10px 10px 0px"/></a>
</div>
</div>
#end## 