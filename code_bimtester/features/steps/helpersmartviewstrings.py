fileheader = """<?xml version="1.0"?>
<bimcollabsmartviewfile>
    <version>5</version>
    <applicationversion>Win - Version: 3.4 (build 3.4.13.559)</applicationversion>
</bimcollabsmartviewfile>
"""


smartviews_string_before = """<SMARTVIEWSETS>
    <SMARTVIEWSET>
        <TITLE>bimtester</TITLE>
        <DESCRIPTION></DESCRIPTION>
        <GUID>a2ddfaf7-97f2-4519-aabd-f2d94f6b4d6b</GUID>
        <MODIFICATIONDATE>2020-10-30T13:23:30</MODIFICATIONDATE>
        <SMARTVIEWS>"""


smartviews_string_after = """        </SMARTVIEWS>
    </SMARTVIEWSET>
</SMARTVIEWSETS>"""


each_smartview_string_title = """            <SMARTVIEW>
                <TITLE>Filter GUID</TITLE>
                <DESCRIPTION></DESCRIPTION>"""


each_smartview_string_before = """                <CREATOR>bernd@bimstatik.ch</CREATOR>
                <CREATIONDATE>2020-10-30T13:18:45</CREATIONDATE>
                <MODIFIER>bernd@bimstatik.ch</MODIFIER>
                <MODIFICATIONDATE>2020-10-30T13:23:30</MODIFICATIONDATE>
                <GUID>15fda94f-b4bf-43be-8ef4-15d3121137e1</GUID>
                <RULES>
                    <RULE>
                        <IFCTYPE>Any</IFCTYPE>
                        <PROPERTY>
                            <NAME>None</NAME>
                            <PROPERTYSETNAME>None</PROPERTYSETNAME>
                            <TYPE>None</TYPE>
                            <VALUETYPE>None</VALUETYPE>
                            <UNIT>None</UNIT>
                        </PROPERTY>
                        <CONDITION>
                            <TYPE>Is</TYPE>
                            <VALUE></VALUE>
                        </CONDITION>
                        <ACTION>
                            <TYPE>AddSetColored</TYPE>
                            <R>187</R>
                            <G>187</G>
                            <B>187</B>
                        </ACTION>
                    </RULE>
                    <RULE>
                        <IFCTYPE>Any</IFCTYPE>
                        <PROPERTY>
                            <NAME>None</NAME>
                            <PROPERTYSETNAME>None</PROPERTYSETNAME>
                            <TYPE>None</TYPE>
                            <VALUETYPE>None</VALUETYPE>
                            <UNIT>None</UNIT>
                        </PROPERTY>
                        <CONDITION>
                            <TYPE>Is</TYPE>
                            <VALUE></VALUE>
                        </CONDITION>
                        <ACTION>
                            <TYPE>SetTransparent</TYPE>
                        </ACTION>
                    </RULE>"""


each_smartview_string_after = """                </RULES>
                <INFORMATIONTAKEOFF>
                    <PROPERTYSETNAME>None</PROPERTYSETNAME>
                    <PROPERTYNAME>None</PROPERTYNAME>
                    <OPERATION>0</OPERATION>
                </INFORMATIONTAKEOFF>
            </SMARTVIEW>"""


rule_string_before = """                    <RULE>
                        <IFCTYPE>Any</IFCTYPE>
                        <PROPERTY>
                            <NAME>GUID</NAME>
                            <PROPERTYSETNAME>Summary</PROPERTYSETNAME>
                            <TYPE>Summary</TYPE>
                            <VALUETYPE>StringValue</VALUETYPE>
                            <UNIT>None</UNIT>
                        </PROPERTY>
                        <CONDITION>
                            <TYPE>Is</TYPE>
                            <VALUE>"""


rule_string_after = """</VALUE>
                        </CONDITION>
                        <ACTION>
                            <TYPE>SetColored</TYPE>
                            <R>255</R>
                            <G>10</G>
                            <B>10</B>
                        </ACTION>
                    </RULE>"""
