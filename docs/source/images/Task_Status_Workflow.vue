<!-- Tufts VUE 3.2.1 concept-map (Task_Status_Workflow.vue) 2014-01-18 -->
<!-- Tufts VUE: http://vue.tufts.edu/ -->
<!-- Do Not Remove: VUE mapping @version(1.1) jar:file:/usr/share/vue/VUE.jar!/tufts/vue/resources/lw_mapping_1_1.xml -->
<!-- Do Not Remove: Saved date Sat Jan 18 17:08:31 EET 2014 by eoyilmaz on platform Linux 3.12.7-300.fc20.x86_64 in JVM 1.7.0_45-b18 -->
<!-- Do Not Remove: Saving version @(#)VUE: built May 18 2013 at 1507 by tomadm on Linux 2.6.18-348.2.1.el5 i386 JVM 1.6.0_41-b02(bits=32) -->
<?xml version="1.0" encoding="US-ASCII"?>
<LW-MAP xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="none" ID="0"
    label="Task_Status_Workflow.vue" created="1388347735325" x="0.0"
    y="0.0" width="1.4E-45" height="1.4E-45" strokeWidth="0.0" autoSized="false">
    <resource referenceCreated="1390057711582" size="23748"
        spec="/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/images/Task_Status_Workflow.vue"
        type="1" xsi:type="URLResource">
        <title>Task_Status_Workflow.vue</title>
        <property key="File" value="/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/images/Task_Status_Workflow.vue"/>
    </resource>
    <fillColor>#FFFFFF</fillColor>
    <strokeColor>#404040</strokeColor>
    <textColor>#000000</textColor>
    <font>SansSerif-plain-14</font>
    <URIString>http://vue.tufts.edu/rdf/resource/400bcd2639fad37c2b0b7e545266b52a</URIString>
    <child ID="6" label="WFD" layerID="1" created="1388347755161"
        x="455.60834" y="18.66666" width="82.3916" height="79.0"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#D0D0D0</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd2939fad37c2b0b7e54a889347a</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="7" label="RTS" layerID="1" created="1388347803612"
        x="622.94165" y="121.83334" width="82.3916" height="80.83333"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#FC938D</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd2c39fad37c2b0b7e54864540f3</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="8" label="task.depends[*].approve&#xa;or no dependency"
        layerID="1" created="1388347803614" x="537.4093" y="58.52907"
        width="130.63562" height="66.67052" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd2d39fad37c2b0b7e546aff6d54</URIString>
        <point1 x="537.9093" y="59.02907"/>
        <point2 x="649.11993" y="124.699585"/>
        <ID1 xsi:type="node">6</ID1>
        <ID2 xsi:type="node">7</ID2>
        <ctrlPoint0 x="623.57526" y="60.826397" xsi:type="point"/>
    </child>
    <child ID="9" label="WIP" layerID="1" created="1388347840853"
        x="826.5" y="174.0" width="77.5" height="77.0" strokeWidth="1.0"
        autoSized="false" xsi:type="node">
        <fillColor>#FFC63B</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4239fad37c2b0b7e547fce60e4</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="11" label="PREV" layerID="1" created="1388347912335"
        x="1005.9166" y="89.25001" width="77.5" height="76.75"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#83CEFF</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4539fad37c2b0b7e543e5eb4f9</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="12" label="request_review" layerID="1"
        created="1388347928095" x="893.0264" y="134.53569"
        width="114.14453" height="52.29561" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4539fad37c2b0b7e54ddb1139f</URIString>
        <point1 x="893.5264" y="186.3313"/>
        <point2 x="1006.67096" y="135.03569"/>
        <ID1 xsi:type="node">9</ID1>
        <ID2 xsi:type="node">11</ID2>
        <ctrlPoint0 x="933.5417" y="149.29887" xsi:type="point"/>
    </child>
    <child ID="13" label="HREV" layerID="1" created="1388347930535"
        x="1004.9166" y="241.24998" width="77.5" height="75.75"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#DAA9FF</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4739fad37c2b0b7e546a650ff6</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="14" label="request_revision" layerID="1"
        created="1388347934209" x="1002.7942" y="165.45312" width="82.0"
        height="76.296875" strokeWidth="1.0" autoSized="false"
        controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4839fad37c2b0b7e549280057f</URIString>
        <point1 x="1044.1775" y="165.95312"/>
        <point2 x="1043.6665" y="241.25"/>
        <ID1 xsi:type="node">11</ID1>
        <ID2 xsi:type="node">13</ID2>
        <ctrlPoint0 x="1043.6665" y="205.99997" xsi:type="point"/>
    </child>
    <child ID="15" label="create_time_log" layerID="1"
        created="1388347943236" x="895.26306" y="235.4754"
        width="110.37891" height="41.964783" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4939fad37c2b0b7e543c642f53</URIString>
        <point1 x="1005.14197" y="276.9402"/>
        <point2 x="895.76306" y="235.9754"/>
        <ID1 xsi:type="node">13</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="944.5415" y="273.50342" xsi:type="point"/>
    </child>
    <child ID="17" label="approve" layerID="1" created="1388347947963"
        x="1082.3657" y="132.53693" width="120.855835" height="51.44342"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4a39fad37c2b0b7e54d6134912</URIString>
        <point1 x="1082.8657" y="133.03693"/>
        <point2 x="1202.7216" y="183.48035"/>
        <ID1 xsi:type="node">11</ID1>
        <ID2 xsi:type="node">18</ID2>
        <ctrlPoint0 x="1152.998" y="142.97308" xsi:type="point"/>
    </child>
    <child ID="18" label="CMPL" layerID="1" created="1388347956643"
        x="1193.9165" y="169.00002" width="77.5" height="77.75"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#8AEE95</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4b39fad37c2b0b7e54dc411cd0</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="21" label="STOP" layerID="1" created="1388347990388"
        x="818.4458" y="12.487498" width="84.66669" height="68.66667"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#EA2218</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#FFFFFF</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4d39fad37c2b0b7e5415afe5b9</URIString>
        <shape xsi:type="hexagon"/>
    </child>
    <child ID="28" label="resume" layerID="1" created="1388348620342"
        x="677.3493" y="216.67438" width="150.12494" height="62.14148"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5539fad37c2b0b7e543dfd69cc</URIString>
        <point1 x="677.8493" y="278.31586"/>
        <point2 x="826.97424" y="217.17438"/>
        <ID1 xsi:type="node">29</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="738.41797" y="227.98915" xsi:type="point"/>
    </child>
    <child ID="29" label="OH" layerID="1" created="1388348638483"
        x="612.24994" y="267.83337" width="77.5" height="65.58331"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#D0D0D0</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5739fad37c2b0b7e546148af1c</URIString>
        <shape xsi:type="hexagon"/>
    </child>
    <child ID="30" label="hold" layerID="1" created="1388348691701"
        x="685.6064" y="231.69934" width="147.0138" height="62.595337"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5739fad37c2b0b7e543634001b</URIString>
        <point1 x="832.1202" y="232.19934"/>
        <point2 x="686.1064" y="293.79468"/>
        <ID1 xsi:type="node">9</ID1>
        <ID2 xsi:type="node">29</ID2>
        <ctrlPoint0 x="749.16394" y="281.52606" xsi:type="point"/>
    </child>
    <child ID="10" label="new time_log" layerID="1"
        created="1388347840854" x="704.80865" y="161.98883"
        width="127.548645" height="31.792816" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4339fad37c2b0b7e54d84a5e4e</URIString>
        <point1 x="705.30865" y="162.48883"/>
        <point2 x="831.8573" y="193.28165"/>
        <ID1 xsi:type="node">7</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="779.09717" y="162.91687" xsi:type="point"/>
    </child>
    <child ID="22" label="stop" layerID="1" created="1388348026798"
        x="829.75464" y="80.65405" width="21.0" height="97.01965"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5339fad37c2b0b7e543f29cb47</URIString>
        <point1 x="849.8922" y="177.1737"/>
        <point2 x="849.04285" y="81.15405"/>
        <ID1 xsi:type="node">9</ID1>
        <ID2 xsi:type="node">21</ID2>
        <ctrlPoint0 x="831.04175" y="133.81372" xsi:type="point"/>
    </child>
    <child ID="36" label="hold" layerID="1" created="1388349518813"
        x="668.1963" y="200.5564" width="20.332642" height="67.77698"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/40157a5e39fad37c2b0b7e547f888462</URIString>
        <point1 x="675.0309" y="201.0564"/>
        <point2 x="668.6963" y="267.83337"/>
        <ID1 xsi:type="node">7</ID1>
        <ID2 xsi:type="node">29</ID2>
        <ctrlPoint0 x="685.1943" y="237.2622" xsi:type="point"/>
    </child>
    <child ID="39" label="resume" layerID="1" created="1388352026387"
        x="620.2645" y="198.69849" width="36.0" height="69.63501"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/403b1cc539fad37c2b0b7e54205cb7b8</URIString>
        <point1 x="641.6218" y="267.8335"/>
        <point2 x="647.55396" y="199.19849"/>
        <ID1 xsi:type="node">29</ID1>
        <ID2 xsi:type="node">7</ID2>
        <ctrlPoint0 x="631.94116" y="233.98413" xsi:type="point"/>
    </child>
    <child ID="45" label="resume" layerID="1" created="1388352320248"
        x="864.7391" y="80.65405" width="36.0" height="95.77368"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/4040cb2939fad37c2b0b7e5425f40da9</URIString>
        <point1 x="872.84955" y="81.15405"/>
        <point2 x="876.7734" y="175.92773"/>
        <ID1 xsi:type="node">21</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="890.6667" y="131.83337" xsi:type="point"/>
    </child>
    <child ID="46" label="request_revision" layerID="1"
        created="1389986937453" x="1081.7737" y="230.65527"
        width="120.53125" height="47.582703" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a1b6ced67f0000013b244fea3bcf813b</URIString>
        <point1 x="1201.8049" y="231.15527"/>
        <point2 x="1082.2737" y="277.73798"/>
        <ID1 xsi:type="node">18</ID1>
        <ID2 xsi:type="node">13</ID2>
        <ctrlPoint0 x="1142.9418" y="275.55835" xsi:type="point"/>
    </child>
    <child ID="48" label="DREV" layerID="1" created="1389987024340"
        x="1002.1918" y="388.3916" width="77.5" height="77.0"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#FFC63B</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a1b6ced77f0000013b244feaa9ee9d7b</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="53" label="task.depends[*].request_revision" layerID="1"
        created="1389987183648" x="1076.3951" y="244.95898"
        width="190.66138" height="172.44278" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a1b6ced87f0000013b244feacfeea727</URIString>
        <point1 x="1229.7809" y="246.45898"/>
        <point2 x="1077.8951" y="415.90176"/>
        <ID1 xsi:type="node">18</ID1>
        <ID2 xsi:type="node">48</ID2>
        <ctrlPoint0 x="1220.275" y="373.5583" xsi:type="point"/>
    </child>
    <child ID="54" label="task.depends[*].approve" layerID="1"
        created="1389987236672" x="822.1396" y="248.92041"
        width="181.56439" height="179.59073" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a1b6ceda7f0000013b244fea6bf684bb</URIString>
        <point1 x="1002.204" y="427.01114"/>
        <point2 x="859.46497" y="250.42041"/>
        <ID1 xsi:type="node">48</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="832.44476" y="427.53494" xsi:type="point"/>
    </child>
    <child ID="59" label="task.depends[*].request_revision" layerID="1"
        created="1390041848192" x="864.2536" y="243.94739" width="159.0"
        height="158.71149" strokeWidth="3.0" strokeStyle="4"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a574d2c37f00000148ec1d5416dda6df</URIString>
        <point1 x="885.0193" y="245.44739"/>
        <point2 x="1012.30347" y="401.15887"/>
        <ID1 xsi:type="node">9</ID1>
        <ID2 xsi:type="node">48</ID2>
        <ctrlPoint0 x="938.8458" y="335.15417" xsi:type="point"/>
    </child>
    <child ID="66" label="create_time_log" layerID="1"
        created="1390050103632" x="1003.81006" y="316.4297" width="77.0"
        height="72.52734" strokeWidth="1.0" autoSized="false"
        controlCount="0" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a574d2c47f00000148ec1d54c76f7627</URIString>
        <point1 x="1042.9695" y="316.9297"/>
        <point2 x="1041.6505" y="388.45703"/>
        <ID1 xsi:type="node">13</ID1>
        <ID2 xsi:type="node">48</ID2>
    </child>
    <child ID="25" label="create_time_log" layerID="1"
        created="1388348049189" x="741.1509" y="245.725"
        width="115.453125" height="92.77731" strokeWidth="1.0"
        autoSized="false" controlCount="2" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5439fad37c2b0b7e54b86d70b9</URIString>
        <point1 x="856.104" y="249.80566"/>
        <point2 x="846.275" y="246.225"/>
        <ID1 xsi:type="node">9</ID1>
        <ctrlPoint0 x="829.0844" y="360.01578" xsi:type="point"/>
        <ctrlPoint1 x="682.52496" y="358.64685" xsi:type="point"/>
    </child>
    <child ID="70" label="create_time_log" layerID="1"
        created="1390055750897" x="1065.9458" y="436.4465"
        width="100.70093" height="51.8685" strokeWidth="1.0"
        autoSized="false" controlCount="2" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a5c84bd87f00000148ec1d5486b15f38</URIString>
        <point1 x="1078.1873" y="436.9465"/>
        <point2 x="1066.4458" y="453.82083"/>
        <ID1 xsi:type="node">48</ID1>
        <ctrlPoint0 x="1201.5228" y="470.24258" xsi:type="point"/>
        <ctrlPoint1 x="1091.9907" y="516.3417" xsi:type="point"/>
    </child>
    <child ID="56" label="task.depends[*].request_revision" layerID="1"
        created="1390041758943" x="459.34485" y="96.36914"
        width="164.69763" height="60.533966" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a574d2c17f00000148ec1d542c75e466</URIString>
        <point1 x="623.5425" y="156.4031"/>
        <point2 x="505.0533" y="96.86914"/>
        <ID1 xsi:type="node">7</ID1>
        <ID2 xsi:type="node">6</ID2>
        <ctrlPoint0 x="514.3917" y="140.68213" xsi:type="point"/>
    </child>
    <layer ID="1" label="Layer 1" created="1388347735329" x="0.0"
        y="0.0" width="1.4E-45" height="1.4E-45" strokeWidth="0.0" autoSized="false">
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5c39fad37c2b0b7e543d00aadd</URIString>
    </layer>
    <userZoom>1.5</userZoom>
    <userOrigin x="293.66864" y="-176.26875"/>
    <presentationBackground>#202020</presentationBackground>
    <PathwayList currentPathway="0" revealerIndex="-1">
        <pathway ID="0" label="Untitled Pathway" created="1388347735313"
            x="0.0" y="0.0" width="1.4E-45" height="1.4E-45"
            strokeWidth="0.0" autoSized="false" currentIndex="0" open="true">
            <strokeColor>#B3993333</strokeColor>
            <textColor>#000000</textColor>
            <font>SansSerif-plain-14</font>
            <URIString>http://vue.tufts.edu/rdf/resource/400bcd5d39fad37c2b0b7e54a8dd4d0e</URIString>
            <masterSlide ID="2" created="1388347735349" x="0.0" y="0.0"
                width="800.0" height="600.0" locked="true"
                strokeWidth="0.0" autoSized="false">
                <fillColor>#000000</fillColor>
                <strokeColor>#404040</strokeColor>
                <textColor>#000000</textColor>
                <font>SansSerif-plain-14</font>
                <URIString>http://vue.tufts.edu/rdf/resource/400bcd5e39fad37c2b0b7e5496c8827d</URIString>
                <titleStyle ID="3" label="Header"
                    created="1388347735385" x="335.5" y="174.5"
                    width="129.0" height="51.0" strokeWidth="0.0"
                    autoSized="true" isStyle="true" xsi:type="node">
                    <strokeColor>#404040</strokeColor>
                    <textColor>#FFFFFF</textColor>
                    <font>Gill Sans-plain-36</font>
                    <URIString>http://vue.tufts.edu/rdf/resource/400bcd5f39fad37c2b0b7e5405c26a3d</URIString>
                    <shape xsi:type="rectangle"/>
                </titleStyle>
                <textStyle ID="4" label="Slide Text"
                    created="1388347735387" x="346.5" y="283.0"
                    width="107.0" height="34.0" strokeWidth="0.0"
                    autoSized="true" isStyle="true" xsi:type="node">
                    <strokeColor>#404040</strokeColor>
                    <textColor>#FFFFFF</textColor>
                    <font>Gill Sans-plain-22</font>
                    <URIString>http://vue.tufts.edu/rdf/resource/400bcd6039fad37c2b0b7e54838aa09c</URIString>
                    <shape xsi:type="rectangle"/>
                </textStyle>
                <linkStyle ID="5" label="Links" created="1388347735388"
                    x="373.5" y="385.0" width="53.0" height="30.0"
                    strokeWidth="0.0" autoSized="true" isStyle="true" xsi:type="node">
                    <strokeColor>#404040</strokeColor>
                    <textColor>#B3BFE3</textColor>
                    <font>Gill Sans-plain-18</font>
                    <URIString>http://vue.tufts.edu/rdf/resource/400bcd6139fad37c2b0b7e542860fb86</URIString>
                    <shape xsi:type="rectangle"/>
                </linkStyle>
            </masterSlide>
        </pathway>
    </PathwayList>
    <date>2013-12-29</date>
    <modelVersion>6</modelVersion>
    <saveLocation>/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/images</saveLocation>
    <saveFile>/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/images/Task_Status_Workflow.vue</saveFile>
</LW-MAP>
