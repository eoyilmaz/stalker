<!-- Tufts VUE 3.2.2 concept-map (Task_Status_Workflow.vue) 2015-06-18 -->
<!-- Tufts VUE: http://vue.tufts.edu/ -->
<!-- Do Not Remove: VUE mapping @version(1.1) jar:file:/home/eoyilmaz/.local/share/vue/VUE.jar!/tufts/vue/resources/lw_mapping_1_1.xml -->
<!-- Do Not Remove: Saved date Thu Jun 18 04:28:12 EEST 2015 by eoyilmaz on platform Linux 4.0.4-301.fc22.x86_64 in JVM 1.8.0_45-b14 -->
<!-- Do Not Remove: Saving version @(#)VUE: built May 23 2013 at 2146 by tomadm on Linux 2.6.18-348.2.1.el5 i386 JVM 1.7.0_21-b11(bits=32) -->
<?xml version="1.0" encoding="US-ASCII"?>
<LW-MAP xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="none" ID="0"
    label="Task_Status_Workflow.vue" created="1388347735325" x="0.0"
    y="0.0" width="1.4E-45" height="1.4E-45" strokeWidth="0.0" autoSized="false">
    <resource referenceCreated="1434590892499" size="35158"
        spec="/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/_static/images/Task_Status_Workflow.vue"
        type="1" xsi:type="URLResource">
        <title>Task_Status_Workflow.vue</title>
        <property key="File" value="/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/_static/images/Task_Status_Workflow.vue"/>
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
    <child ID="8" label="task.depends_on[*].approve&#xa;or no dependency"
        layerID="1" created="1388347803614" x="533.74115" y="70.56363"
        width="121.582825" height="63.072296" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd2d39fad37c2b0b7e546aff6d54</URIString>
        <point1 x="535.24115" y="72.06363"/>
        <point2 x="636.9042" y="132.13593"/>
        <ID1 xsi:type="node">6</ID1>
        <ID2 xsi:type="node">7</ID2>
        <ctrlPoint0 x="605.57526" y="97.49305" xsi:type="point"/>
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
        created="1388347934209" x="1003.2942" y="165.45312" width="81.0"
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
        x="759.7791" y="-2.179165" width="84.66669" height="68.66667"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#EA2218</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#FFFFFF</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4d39fad37c2b0b7e5415afe5b9</URIString>
        <shape xsi:type="hexagon"/>
    </child>
    <child ID="28" label="resume" layerID="1" created="1388348620342"
        x="678.95337" y="220.56944" width="149.08716" height="61.25334"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5539fad37c2b0b7e543dfd69cc</URIString>
        <point1 x="679.45337" y="281.32278"/>
        <point2 x="827.5405" y="221.06944"/>
        <ID1 xsi:type="node">29</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="738.41797" y="241.32248" xsi:type="point"/>
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
    <child ID="10" label="create_time_log" layerID="1"
        created="1388347840854" x="704.5831" y="164.18347"
        width="125.809326" height="33.194763" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd4339fad37c2b0b7e54d84a5e4e</URIString>
        <point1 x="705.0831" y="164.68347"/>
        <point2 x="829.89246" y="196.87823"/>
        <ID1 xsi:type="node">7</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="765.09717" y="168.25021" xsi:type="point"/>
    </child>
    <child ID="22" label="stop" layerID="1" created="1388348026798"
        x="804.153" y="65.987305" width="37.611145" height="116.98999"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5339fad37c2b0b7e543f29cb47</URIString>
        <point1 x="841.26416" y="182.4773"/>
        <point2 x="804.653" y="66.487305"/>
        <ID1 xsi:type="node">9</ID1>
        <ID2 xsi:type="node">21</ID2>
        <ctrlPoint0 x="810.37506" y="143.81372" xsi:type="point"/>
    </child>
    <child ID="45" label="resume" layerID="1" created="1388352320248"
        x="822.34424" y="65.98755" width="45.103394" height="108.87671"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/4040cb2939fad37c2b0b7e5425f40da9</URIString>
        <point1 x="822.84424" y="66.48755"/>
        <point2 x="861.613" y="174.36426"/>
        <ID1 xsi:type="node">21</ID1>
        <ID2 xsi:type="node">9</ID2>
        <ctrlPoint0 x="856.6667" y="122.50004" xsi:type="point"/>
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
    <child ID="53" label="task.depends_on[*].request_revision" layerID="1"
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
    <child ID="54" label="task.depends_on[*].approve" layerID="1"
        created="1389987236672" x="857.20386" y="293.70032"
        width="152.99811" height="126.148285" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a1b6ceda7f0000013b244fea6bf684bb</URIString>
        <point1 x="1003.224" y="418.3486"/>
        <point2 x="1008.70197" y="295.20032"/>
        <ID1 xsi:type="node">48</ID1>
        <ID2 xsi:type="node">13</ID2>
        <ctrlPoint0 x="827.44476" y="378.53494" xsi:type="point"/>
    </child>
    <child ID="59" label="task.depends_on[*].request_revision" layerID="1"
        created="1390041848192" x="863.7536" y="243.94739" width="160.0"
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
        created="1390050103632" x="1004.31006" y="316.4297" width="76.0"
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
        created="1388348049189" x="741.6509" y="245.725"
        width="114.953125" height="92.27731" strokeWidth="1.0"
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
        width="100.20093" height="51.3685" strokeWidth="1.0"
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
    <child ID="56" label="task.depends_on[*].request_revision" layerID="1"
        created="1390041758943" x="468.4242" y="93.67566" width="160.0"
        height="64.96039" strokeWidth="3.0" strokeStyle="4"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/a574d2c17f00000148ec1d542c75e466</URIString>
        <point1 x="623.46716" y="157.13605"/>
        <point2 x="510.77924" y="95.17566"/>
        <ID1 xsi:type="node">7</ID1>
        <ID2 xsi:type="node">6</ID2>
        <ctrlPoint0 x="529.72516" y="145.34879" xsi:type="point"/>
    </child>
    <child ID="83" label="delete_time_log" layerID="1"
        created="1390229964313" x="701.86884" y="176.61932"
        width="125.67432" height="31.027588" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b02ac6397f0000013e376dbaac4e08d3</URIString>
        <point1 x="827.04315" y="207.14691"/>
        <point2 x="702.36884" y="177.11932"/>
        <ID1 xsi:type="node">9</ID1>
        <ID2 xsi:type="node">7</ID2>
        <ctrlPoint0 x="752.8457" y="196.75125" xsi:type="point"/>
    </child>
    <child ID="85" label="WFD" layerID="1" created="1390239171735"
        x="494.5249" y="611.99994" width="82.3916" height="79.0"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#D0D0D0</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b951897f0000010f9ede6dbf93a108</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="86" label="RTS" layerID="1" created="1390239171735"
        x="691.59143" y="611.99994" width="82.3916" height="80.83333"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#FC938D</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b9518a7f0000010f9ede6df7032851</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="87" label="approve" layerID="1" created="1390239171735"
        x="575.43567" y="630.1156" width="117.87976" height="13.479248"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b9518b7f0000010f9ede6d33187e87</URIString>
        <point1 x="575.93567" y="643.09485"/>
        <point2 x="692.8154" y="643.04816"/>
        <ID1 xsi:type="node">85</ID1>
        <ID2 xsi:type="node">86</ID2>
        <ctrlPoint0 x="637.8251" y="630.15967" xsi:type="point"/>
    </child>
    <child ID="88" label="WIP" layerID="1" created="1390239171735"
        x="888.65796" y="611.99994" width="77.5" height="77.0"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#FFC63B</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b9518c7f0000010f9ede6d5646bd67</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="94" label="approve" layerID="1" created="1390239171735"
        x="964.96716" y="631.6112" width="117.1167" height="13.0"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b9518d7f0000010f9ede6d0afb73cb</URIString>
        <point1 x="965.46716" y="643.6913"/>
        <point2 x="1081.5839" y="643.402"/>
        <ID1 xsi:type="node">88</ID1>
        <ID2 xsi:type="node">95</ID2>
        <ctrlPoint0 x="1027.0425" y="632.6758" xsi:type="point"/>
    </child>
    <child ID="95" label="CMPL" layerID="1" created="1390239171735"
        x="1080.8329" y="611.99994" width="77.5" height="77.75"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#8AEE95</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b9518e7f0000010f9ede6de123e8b3</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="100" label="create_time_log" layerID="1"
        created="1390239171735" x="772.4731" y="630.88525"
        width="117.44147" height="13.339111" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b9518f7f0000010f9ede6da65640f1</URIString>
        <point1 x="772.9731" y="643.72437"/>
        <point2 x="889.41455" y="643.0438"/>
        <ID1 xsi:type="node">86</ID1>
        <ID2 xsi:type="node">88</ID2>
        <ctrlPoint0 x="830.01373" y="631.3865" xsi:type="point"/>
    </child>
    <child ID="115" label="delete_time_log" layerID="1"
        created="1390239171735" x="573.78766" y="663.8028"
        width="120.32428" height="17.02948" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b951907f0000010f9ede6d61625eb4</URIString>
        <point1 x="693.61194" y="664.3028"/>
        <point2 x="574.28766" y="664.9955"/>
        <ID1 xsi:type="node">86</ID1>
        <ID2 xsi:type="node">85</ID2>
        <ctrlPoint0 x="628.64166" y="684.0154" xsi:type="point"/>
    </child>
    <child ID="120" label="delete_time_log" layerID="1"
        created="1390239171735" x="770.619" y="665.2781"
        width="121.743774" height="19.78424" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b951917f0000010f9ede6ddfc41ffa</URIString>
        <point1 x="891.8628" y="665.7781"/>
        <point2 x="771.119" y="666.969"/>
        <ID1 xsi:type="node">88</ID1>
        <ID2 xsi:type="node">86</ID2>
        <ctrlPoint0 x="833.7622" y="690.7511" xsi:type="point"/>
    </child>
    <child ID="122" label="request_revision" layerID="1"
        created="1390239225857" x="961.28296" y="665.8157"
        width="123.26221" height="22.071533" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b951927f0000010f9ede6d857e3460</URIString>
        <point1 x="1084.0452" y="666.3157"/>
        <point2 x="961.78296" y="667.92004"/>
        <ID1 xsi:type="node">95</ID1>
        <ID2 xsi:type="node">88</ID2>
        <ctrlPoint0 x="1016.5156" y="695.65656" xsi:type="point"/>
    </child>
    <child ID="123" label="CONTAINER TASK STATUS WORKFLOW" layerID="1"
        created="1390239279430" x="709.70917" y="576.3718" width="242.0"
        height="17.0" strokeWidth="0.0" autoSized="false" xsi:type="text">
        <strokeColor>#404040</strokeColor>
        <textColor>#000000</textColor>
        <font>SansSerif-plain-14</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b951937f0000010f9ede6df249fca0</URIString>
        <richText>&lt;html&gt;
  &lt;head color="#404040" style="color: #404040"&gt;
    &lt;style type="text/css"&gt;
      &lt;!--
        body { margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; font-size: 11; font-family: Arial; color: #404040 }
        ol { margin-top: 6; font-family: Arial; vertical-align: middle; margin-left: 30; font-size: 11; list-style-position: outside }
        p { margin-top: 0; margin-left: 0; margin-right: 0; margin-bottom: 0; color: #404040 }
        ul { margin-top: 6; font-size: 11; margin-left: 30; vertical-align: middle; list-style-position: outside; font-family: Arial }
      --&gt;
    &lt;/style&gt;
    
  &lt;/head&gt;
  &lt;body&gt;
    &lt;p color="#404040" style="text-align: center; color: #404040"&gt;
      CONTAINER TASK STATUS WORKFLOW
    &lt;/p&gt;
  &lt;/body&gt;
&lt;/html&gt;
</richText>
        <label>CONTAINER TASK STATUS WORKFLOW</label>
    </child>
    <child ID="125" label="LEAF TASK STATUS WORKFLOW" layerID="1"
        created="1390239332214" x="796.04254" y="-49.737953"
        width="242.0" height="17.0" strokeWidth="0.0" autoSized="false" xsi:type="text">
        <strokeColor>#404040</strokeColor>
        <textColor>#000000</textColor>
        <font>SansSerif-plain-14</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b0b951957f0000010f9ede6d01435234</URIString>
        <richText>&lt;html&gt;
  &lt;head color="#404040" style="color: #404040"&gt;
    &lt;style type="text/css"&gt;
      &lt;!--
        body { margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; font-size: 11; font-family: Arial; color: #404040 }
        ol { margin-top: 6; font-family: Arial; vertical-align: middle; margin-left: 30; font-size: 11; list-style-position: outside }
        p { margin-top: 0; margin-left: 0; margin-right: 0; margin-bottom: 0; color: #404040 }
        ul { margin-top: 6; font-size: 11; margin-left: 30; vertical-align: middle; list-style-position: outside; font-family: Arial }
      --&gt;
    &lt;/style&gt;
    
  &lt;/head&gt;
  &lt;body&gt;
    &lt;p color="#404040" style="text-align: center; color: #404040"&gt;
      LEAF TASK STATUS WORKFLOW
    &lt;/p&gt;
  &lt;/body&gt;
&lt;/html&gt;
</richText>
        <label>LEAF TASK STATUS WORKFLOW</label>
    </child>
    <child ID="126" label="resume" layerID="1" created="1390300976758"
        x="673.1849" y="330.24115" width="330.14667" height="111.1467"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/b465a9c87f00000160874ad883e2b183</URIString>
        <point1 x="673.6849" y="330.74115"/>
        <point2 x="1002.83154" y="433.19635"/>
        <ID1 xsi:type="node">29</ID1>
        <ID2 xsi:type="node">48</ID2>
        <ctrlPoint0 x="778.7791" y="470.26202" xsi:type="point"/>
    </child>
    <child ID="127" label="hold" layerID="1" created="1390405947783"
        x="667.5642" y="332.91675" width="337.17053" height="129.22067"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/baa74e4c7f000001444cc84d9fe05d8e</URIString>
        <point1 x="1004.23474" y="438.66983"/>
        <point2 x="668.0642" y="333.41675"/>
        <ID1 xsi:type="node">48</ID1>
        <ID2 xsi:type="node">29</ID2>
        <ctrlPoint0 x="763.10004" y="516.04285" xsi:type="point"/>
    </child>
    <child ID="132" label="resume" layerID="1" created="1390424390043"
        x="836.1739" y="-8.720401" width="483.16998" height="436.11707"
        strokeWidth="1.0" autoSized="false" controlCount="2"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/bbd8eded7f000001444cc84d0c8a9afd</URIString>
        <point1 x="836.6739" y="18.19101"/>
        <point2 x="1079.6913" y="426.89667"/>
        <ID1 xsi:type="node">21</ID1>
        <ID2 xsi:type="node">48</ID2>
        <ctrlPoint0 x="1215.7904" y="-134.97574" xsi:type="point"/>
        <ctrlPoint1 x="1569.1111" y="426.96072" xsi:type="point"/>
    </child>
    <child ID="133" label="stop" layerID="1" created="1390424424438"
        x="834.6763" y="-25.234804" width="512.50903" height="456.37933"
        strokeWidth="1.0" autoSized="false" controlCount="2"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/bbd8edee7f000001444cc84da1d1e216</URIString>
        <point1 x="1079.4398" y="429.37418"/>
        <point2 x="835.1763" y="15.500305"/>
        <ID1 xsi:type="node">48</ID1>
        <ID2 xsi:type="node">21</ID2>
        <ctrlPoint0 x="1616.1722" y="463.98547" xsi:type="point"/>
        <ctrlPoint1 x="1246.1915" y="-191.52309" xsi:type="point"/>
    </child>
    <child ID="134" label="WFD" layerID="1" created="1433612001033"
        x="1560.3584" y="36.174225" width="82.3916" height="79.0"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#D0D0D0</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d21dc0a8012b17e4445f9ad9d4f0</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="135" label="RTS" layerID="1" created="1433612001033"
        x="1727.6917" y="139.34091" width="82.3916" height="80.83333"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#FC938D</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d21ec0a8012b17e4445fe5262599</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="136" label="task.depends_on[*].approve&#xa;or no dependency"
        layerID="1" created="1433612001033" x="1638.491" y="88.07114"
        width="121.58301" height="63.07242" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d21ec0a8012b17e4445f7e54fab2</URIString>
        <point1 x="1639.991" y="89.57114"/>
        <point2 x="1741.6542" y="149.64355"/>
        <ID1 xsi:type="node">134</ID1>
        <ID2 xsi:type="node">135</ID2>
        <ctrlPoint0 x="1710.3252" y="115.00061" xsi:type="point"/>
    </child>
    <child ID="137" label="WIP" layerID="1" created="1433612001033"
        x="1931.25" y="191.50757" width="77.5" height="77.0"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#FFC63B</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d21fc0a8012b17e4445f9fb714d9</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="138" label="PREV" layerID="1" created="1433612001033"
        x="2110.6665" y="106.75757" width="77.5" height="76.75"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#83CEFF</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d220c0a8012b17e4445fa5c7307d</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="139" label="request_review" layerID="1"
        created="1433612001033" x="1997.7762" y="152.04327"
        width="114.14465" height="52.295715" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d221c0a8012b17e4445f09711db8</URIString>
        <point1 x="1998.2762" y="203.83899"/>
        <point2 x="2111.421" y="152.54327"/>
        <ID1 xsi:type="node">137</ID1>
        <ID2 xsi:type="node">138</ID2>
        <ctrlPoint0 x="2038.2917" y="166.80643" xsi:type="point"/>
    </child>
    <child ID="140" label="HREV" layerID="1" created="1433612001033"
        x="2109.6665" y="258.75754" width="77.5" height="75.75"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#DAA9FF</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d222c0a8012b17e4445f68152c62</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="141" label="request_revision" layerID="1"
        created="1433612001033" x="2108.0442" y="182.95312" width="81.0"
        height="76.30438" strokeWidth="1.0" autoSized="false"
        controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d222c0a8012b17e4445f68878e0b</URIString>
        <point1 x="2148.9275" y="183.45312"/>
        <point2 x="2148.4165" y="258.7575"/>
        <ID1 xsi:type="node">138</ID1>
        <ID2 xsi:type="node">140</ID2>
        <ctrlPoint0 x="2148.4165" y="223.50754" xsi:type="point"/>
    </child>
    <child ID="142" label="create_time_log" layerID="1"
        created="1433612001033" x="2000.013" y="252.98291"
        width="110.37891" height="41.964813" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d223c0a8012b17e4445ffb86e992</URIString>
        <point1 x="2109.8918" y="294.44772"/>
        <point2 x="2000.513" y="253.48291"/>
        <ID1 xsi:type="node">140</ID1>
        <ID2 xsi:type="node">137</ID2>
        <ctrlPoint0 x="2049.2915" y="291.011" xsi:type="point"/>
    </child>
    <child ID="143" label="approve" layerID="1" created="1433612001033"
        x="2187.1155" y="150.0445" width="120.8562" height="51.443665"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d224c0a8012b17e4445f3f7e4d37</URIString>
        <point1 x="2187.6155" y="150.5445"/>
        <point2 x="2307.4717" y="200.98816"/>
        <ID1 xsi:type="node">138</ID1>
        <ID2 xsi:type="node">144</ID2>
        <ctrlPoint0 x="2257.748" y="160.48065" xsi:type="point"/>
    </child>
    <child ID="144" label="CMPL" layerID="1" created="1433612001033"
        x="2298.6665" y="186.50757" width="77.5" height="77.75"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#8AEE95</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d224c0a8012b17e4445f2622ddfe</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="145" label="STOP" layerID="1" created="1433612001033"
        x="1864.529" y="15.3284" width="84.66669" height="68.66667"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#EA2218</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#FFFFFF</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d225c0a8012b17e4445f95fe4ae5</URIString>
        <shape xsi:type="hexagon"/>
    </child>
    <child ID="146" label="resume" layerID="1" created="1433612001033"
        x="1783.7035" y="238.07706" width="149.08691" height="61.253265"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d225c0a8012b17e4445f5cde7a27</URIString>
        <point1 x="1784.2035" y="298.83032"/>
        <point2 x="1932.2904" y="238.57706"/>
        <ID1 xsi:type="node">147</ID1>
        <ID2 xsi:type="node">137</ID2>
        <ctrlPoint0 x="1843.168" y="258.83005" xsi:type="point"/>
    </child>
    <child ID="147" label="OH" layerID="1" created="1433612001033"
        x="1717.0" y="285.34094" width="77.5" height="65.58331"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#D0D0D0</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d226c0a8012b17e4445f58f103df</URIString>
        <shape xsi:type="hexagon"/>
    </child>
    <child ID="148" label="hold" layerID="1" created="1433612001033"
        x="1790.3564" y="249.20691" width="147.0138" height="62.595306"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d226c0a8012b17e4445f20a567f8</URIString>
        <point1 x="1936.8702" y="249.70691"/>
        <point2 x="1790.8564" y="311.30222"/>
        <ID1 xsi:type="node">137</ID1>
        <ID2 xsi:type="node">147</ID2>
        <ctrlPoint0 x="1853.914" y="299.03363" xsi:type="point"/>
    </child>
    <child ID="149" label="now &lt; start" layerID="1"
        created="1433612001033" x="1809.3333" y="181.69104"
        width="125.809326" height="33.194885" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d227c0a8012b17e4445f218056c0</URIString>
        <point1 x="1809.8333" y="182.19104"/>
        <point2 x="1934.6426" y="214.38593"/>
        <ID1 xsi:type="node">135</ID1>
        <ID2 xsi:type="node">137</ID2>
        <ctrlPoint0 x="1869.8472" y="185.75778" xsi:type="point"/>
    </child>
    <child ID="150" label="stop" layerID="1" created="1433612001033"
        x="1908.9031" y="83.49414" width="37.611084" height="116.99072"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d228c0a8012b17e4445fb829c90a</URIString>
        <point1 x="1946.0142" y="199.98486"/>
        <point2 x="1909.4031" y="83.99414"/>
        <ID1 xsi:type="node">137</ID1>
        <ID2 xsi:type="node">145</ID2>
        <ctrlPoint0 x="1915.125" y="161.32129" xsi:type="point"/>
    </child>
    <child ID="151" label="resume" layerID="1" created="1433612001033"
        x="1927.0944" y="83.49512" width="45.103394" height="108.87598"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d229c0a8012b17e4445ffe30d926</URIString>
        <point1 x="1927.5944" y="83.99512"/>
        <point2 x="1966.363" y="191.8711"/>
        <ID1 xsi:type="node">145</ID1>
        <ID2 xsi:type="node">137</ID2>
        <ctrlPoint0 x="1961.4167" y="140.0076" xsi:type="point"/>
    </child>
    <child ID="152" label="request_revision" layerID="1"
        created="1433612001033" x="2186.5234" y="248.16272"
        width="120.53174" height="47.582825" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d229c0a8012b17e4445f6d767d7e</URIString>
        <point1 x="2306.5552" y="248.66272"/>
        <point2 x="2187.0234" y="295.24554"/>
        <ID1 xsi:type="node">144</ID1>
        <ID2 xsi:type="node">140</ID2>
        <ctrlPoint0 x="2247.692" y="293.06592" xsi:type="point"/>
    </child>
    <child ID="153" label="DREV" layerID="1" created="1433612001033"
        x="2106.942" y="405.89917" width="77.5" height="77.0"
        strokeWidth="1.0" autoSized="false" xsi:type="node">
        <fillColor>#FFC63B</fillColor>
        <strokeColor>#000000</strokeColor>
        <textColor>#000000</textColor>
        <font>Arial-bold-12</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22ac0a8012b17e4445f8ac663b8</URIString>
        <shape xsi:type="ellipse"/>
    </child>
    <child ID="154" label="task.depends_on[*].request_revision" layerID="1"
        created="1433612001033" x="2181.1453" y="262.4668"
        width="190.66113" height="172.44257" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22ac0a8012b17e4445f5c71943d</URIString>
        <point1 x="2334.5308" y="263.9668"/>
        <point2 x="2182.6453" y="433.40936"/>
        <ID1 xsi:type="node">144</ID1>
        <ID2 xsi:type="node">153</ID2>
        <ctrlPoint0 x="2325.025" y="391.06586" xsi:type="point"/>
    </child>
    <child ID="155" label="task.depends_on[*].approve" layerID="1"
        created="1433612001033" x="1961.9539" y="311.20795"
        width="152.9978" height="126.148224" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22bc0a8012b17e4445f2a8d786b</URIString>
        <point1 x="2107.974" y="435.85617"/>
        <point2 x="2113.4517" y="312.70795"/>
        <ID1 xsi:type="node">153</ID1>
        <ID2 xsi:type="node">140</ID2>
        <ctrlPoint0 x="1932.1948" y="396.0425" xsi:type="point"/>
    </child>
    <child ID="156" label="task.depends_on[*].request_revision" layerID="1"
        created="1433612001033" x="1968.5037" y="261.4546" width="160.0"
        height="158.71179" strokeWidth="3.0" strokeStyle="4"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22cc0a8012b17e4445fd590992f</URIString>
        <point1 x="1989.7692" y="262.9546"/>
        <point2 x="2117.0535" y="418.66638"/>
        <ID1 xsi:type="node">137</ID1>
        <ID2 xsi:type="node">153</ID2>
        <ctrlPoint0 x="2043.5958" y="352.66174" xsi:type="point"/>
    </child>
    <child ID="157" label="create_time_log" layerID="1"
        created="1433612001033" x="2109.0598" y="333.9453" width="76.0"
        height="72.52344" strokeWidth="1.0" autoSized="false"
        controlCount="0" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22dc0a8012b17e4445f23a0e668</URIString>
        <point1 x="2147.7192" y="334.4453"/>
        <point2 x="2146.4004" y="405.96875"/>
        <ID1 xsi:type="node">140</ID1>
        <ID2 xsi:type="node">153</ID2>
    </child>
    <child ID="158" label="create_time_log" layerID="1"
        created="1433612001033" x="1846.4009" y="263.23257"
        width="114.953125" height="92.27725" strokeWidth="1.0"
        autoSized="false" controlCount="2" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22dc0a8012b17e4445f3be48af4</URIString>
        <point1 x="1960.854" y="267.313"/>
        <point2 x="1951.025" y="263.73257"/>
        <ID1 xsi:type="node">137</ID1>
        <ctrlPoint0 x="1933.8345" y="377.52335" xsi:type="point"/>
        <ctrlPoint1 x="1787.2749" y="376.15442" xsi:type="point"/>
    </child>
    <child ID="159" label="create_time_log" layerID="1"
        created="1433612001033" x="2170.6958" y="453.95404"
        width="100.20093" height="51.36853" strokeWidth="1.0"
        autoSized="false" controlCount="2" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22ec0a8012b17e4445fe8d0268c</URIString>
        <point1 x="2182.9373" y="454.45404"/>
        <point2 x="2171.1958" y="471.3284"/>
        <ID1 xsi:type="node">153</ID1>
        <ctrlPoint0 x="2306.273" y="487.75015" xsi:type="point"/>
        <ctrlPoint1 x="2196.7407" y="533.84924" xsi:type="point"/>
    </child>
    <child ID="160" label="task.depends_on[*].request_revision" layerID="1"
        created="1433612001033" x="1573.1741" y="111.183105"
        width="160.0" height="64.960526" strokeWidth="3.0"
        strokeStyle="4" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#EA2218</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d22fc0a8012b17e4445f07f35e93</URIString>
        <point1 x="1728.2172" y="174.64363"/>
        <point2 x="1615.529" y="112.683105"/>
        <ID1 xsi:type="node">135</ID1>
        <ID2 xsi:type="node">134</ID2>
        <ctrlPoint0 x="1634.4751" y="162.85635" xsi:type="point"/>
    </child>
    <child ID="161" label="now > start" layerID="1"
        created="1433612001033" x="1806.6188" y="194.12686"
        width="125.67444" height="31.027649" strokeWidth="1.0"
        autoSized="false" controlCount="1" arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d230c0a8012b17e4445fcce5a2e1</URIString>
        <point1 x="1931.7932" y="224.65451"/>
        <point2 x="1807.1188" y="194.62686"/>
        <ID1 xsi:type="node">137</ID1>
        <ID2 xsi:type="node">135</ID2>
        <ctrlPoint0 x="1857.5957" y="214.25882" xsi:type="point"/>
    </child>
    <child ID="162" label="resume" layerID="1" created="1433612001033"
        x="1777.9348" y="347.74854" width="330.14697" height="111.14679"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d231c0a8012b17e4445f0569c66e</URIString>
        <point1 x="1778.4348" y="348.24854"/>
        <point2 x="2107.5818" y="450.7038"/>
        <ID1 xsi:type="node">147</ID1>
        <ID2 xsi:type="node">153</ID2>
        <ctrlPoint0 x="1883.529" y="487.7696" xsi:type="point"/>
    </child>
    <child ID="163" label="hold" layerID="1" created="1433612001033"
        x="1772.3145" y="350.42432" width="337.1704" height="129.22067"
        strokeWidth="1.0" autoSized="false" controlCount="1"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d231c0a8012b17e4445f44b3f111</URIString>
        <point1 x="2108.9849" y="456.17737"/>
        <point2 x="1772.8145" y="350.92432"/>
        <ID1 xsi:type="node">153</ID1>
        <ID2 xsi:type="node">147</ID2>
        <ctrlPoint0 x="1867.8501" y="533.5504" xsi:type="point"/>
    </child>
    <child ID="164" label="resume" layerID="1" created="1433612001033"
        x="1940.9238" y="8.787188" width="483.17017" height="436.11703"
        strokeWidth="1.0" autoSized="false" controlCount="2"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d232c0a8012b17e4445f46acc020</URIString>
        <point1 x="1941.4238" y="35.69861"/>
        <point2 x="2184.4414" y="444.40424"/>
        <ID1 xsi:type="node">145</ID1>
        <ID2 xsi:type="node">153</ID2>
        <ctrlPoint0 x="2320.5405" y="-117.46817" xsi:type="point"/>
        <ctrlPoint1 x="2673.861" y="444.4683" xsi:type="point"/>
    </child>
    <child ID="165" label="stop" layerID="1" created="1433612001033"
        x="1939.4261" y="-7.727159" width="512.50916" height="456.37927"
        strokeWidth="1.0" autoSized="false" controlCount="2"
        arrowState="2" xsi:type="link">
        <strokeColor>#404040</strokeColor>
        <textColor>#404040</textColor>
        <font>Arial-plain-11</font>
        <URIString>http://vue.tufts.edu/rdf/resource/0447d233c0a8012b17e4445fb3acd833</URIString>
        <point1 x="2184.19" y="446.8817"/>
        <point2 x="1939.9261" y="33.007996"/>
        <ID1 xsi:type="node">153</ID1>
        <ID2 xsi:type="node">145</ID2>
        <ctrlPoint0 x="2720.9224" y="481.49304" xsi:type="point"/>
        <ctrlPoint1 x="2350.9414" y="-174.01553" xsi:type="point"/>
    </child>
    <layer ID="1" label="Layer 1" created="1388347735329" x="0.0"
        y="0.0" width="1.4E-45" height="1.4E-45" strokeWidth="0.0" autoSized="false">
        <URIString>http://vue.tufts.edu/rdf/resource/400bcd5c39fad37c2b0b7e543d00aadd</URIString>
    </layer>
    <userZoom>0.1872035782673108</userZoom>
    <userOrigin x="141.14682" y="-174.72716"/>
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
                    width="129.0" height="50.0" strokeWidth="0.0"
                    autoSized="true" isStyle="true" xsi:type="node">
                    <strokeColor>#404040</strokeColor>
                    <textColor>#FFFFFF</textColor>
                    <font>Gill Sans-plain-36</font>
                    <URIString>http://vue.tufts.edu/rdf/resource/400bcd5f39fad37c2b0b7e5405c26a3d</URIString>
                    <shape xsi:type="rectangle"/>
                </titleStyle>
                <textStyle ID="4" label="Slide Text"
                    created="1388347735387" x="346.5" y="283.0"
                    width="108.0" height="34.0" strokeWidth="0.0"
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
    <saveLocation>/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/_static/images</saveLocation>
    <saveFile>/home/eoyilmaz/Documents/development/stalker/stalker/docs/source/_static/images/Task_Status_Workflow.vue</saveFile>
</LW-MAP>
