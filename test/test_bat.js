function writeGroupControlVarToCookie( controlName , flag )
{
	if( flag == 0 )
	{
		document.cookie = controlName + "=" + document.getElementByName(controlName).value;
	}
	else
	{
		var i;
		var str = "";
		for (i=0;i<document.getElementsByName(controlName).length;i++)
		{
			if( document.getElementsByName( controlName )[i].checked == true )
			{
				str += "," + document.getElementsByName( controlName )[i].value;
			}
		}
		if (i==0)
		{
			if( document.getElementById( controlName ).checked == true )
			{
				str = document.getElementById( controlName ).value;
			}
		}

		document.cookie = controlName + "=" + escape(str);
	}
}
function CheckDate()
{
	if (document.getElementById("searchInResult").checked == true)
	{
	if(document.getElementById("PublicationDate") != null)
	{
		document.getElementById("PublicationDate").selectedIndex = 0;
		document.getElementById("PublicationDate").disabled = true;
		document.getElementById("PublicationDate").style.backgroundColor='#ababab';
	}
	if(document.getElementById("yearstart") != null)
	{
		document.getElementById("yearstart").disabled = true;
		document.getElementById("yearstart").style.backgroundColor='#ababab';
	}
	if(document.getElementById("RealYearStart") != null)
	{
		document.getElementById("RealYearStart").disabled = true;
		document.getElementById("RealYearStart").style.backgroundColor='#ababab';
	}
	if(document.getElementById("yearend") != null)
	{
		document.getElementById("yearend").disabled = true;
		document.getElementById("yearend").style.backgroundColor='#ababab';
	}
	if(document.getElementById("RealYearEnd") != null)
	{
		document.getElementById("RealYearEnd").disabled = true;
		document.getElementById("RealYearEnd").style.backgroundColor='#ababab';
	}
	if(document.getElementById("SearchRange") != null)
	{
		document.getElementById("SearchRange").disabled = true;
		document.getElementById("SearchRange").style.backgroundColor='#ababab';
	}
	}
	else
	{
	if(document.getElementById("PublicationDate") != null)
	{
		document.getElementById("PublicationDate").disabled = false;
		document.getElementById("PublicationDate").style.backgroundColor='';
	}
	if(document.getElementById("yearstart") != null)
	{
		document.getElementById("yearstart").disabled = false;
		document.getElementById("yearstart").style.backgroundColor='';
	}
	if(document.getElementById("RealYearStart") != null)
	{
		document.getElementById("RealYearStart").disabled = false;
		document.getElementById("RealYearStart").style.backgroundColor='';
	}
	if(document.getElementById("yearend") != null)
	{
		document.getElementById("yearend").disabled = false;
		document.getElementById("yearend").style.backgroundColor='';
	}
	if(document.getElementById("RealYearEnd") != null)
	{
		document.getElementById("RealYearEnd").disabled = false;
		document.getElementById("RealYearEnd").style.backgroundColor='';
	}
	if(document.getElementById("SearchRange") != null)
	{
		document.getElementById("SearchRange").disabled = false;
		document.getElementById("SearchRange").style.backgroundColor='';
	}
	}
}
function SetEnableOfDate(disabled)
{
	if(document.getElementById("yearstart") != null)
	{
		document.getElementById("yearstart").disabled = disabled;
		document.getElementById("yearstart").style.backgroundColor=(disabled==true?'#ababab':'');
	}
	if(document.getElementById("RealYearStart") != null)
	{
		document.getElementById("RealYearStart").disabled = disabled;
		document.getElementById("RealYearStart").style.backgroundColor=(disabled==true?'#ababab':'');
	}
	if(document.getElementById("yearend") != null)
	{
		document.getElementById("yearend").disabled = disabled;
		document.getElementById("yearend").style.backgroundColor=(disabled==true?'#ababab':'');
	}
	if(document.getElementById("RealYearEnd") != null)
	{
		document.getElementById("RealYearEnd").disabled = disabled;
		document.getElementById("RealYearEnd").style.backgroundColor=(disabled==true?'#ababab':'');
	}
}
function GetUSPSubDB(strSubDB,intIndex)
{
	//检索范围,+0+,1,1|SUBDB2,+2+,1,1
	//库名，选中的库，最多能选的库个数，已经选择的库个数
	var arrDB = document.getElementById("hdnUSPSubDB").value.split('|');
	document.getElementById("hdnUSPSubDB").value = "";
	for (i=0; i<arrDB.length; i++)
	{
		if (arrDB[i].indexOf(strSubDB) > -1)
		{
							var arrItem = arrDB[i].split(',');
									if (arrItem[1].indexOf("+" + intIndex + "+") > -1)
			{
				//用户在作减少数据库操作
				//已经有了，需要去掉
				arrItem[1] = arrItem[1].replace("+" + intIndex + "+","+");
				arrItem[3] = parseInt(arrItem[3]) - 1;
				document.getElementById(strSubDB + 'All').checked = false;
			}
			else
			{
				//用户在作增加数据库操作
				if (parseInt(arrItem[3]) >= parseInt(arrItem[2]))
				{
					//已经达到最大的数目
					alert(arrItem[0] + "最多只能选择" + arrItem[2] + "个");
					document.getElementById(strSubDB+intIndex).checked = false;
				}
				else
				{
					arrItem[1] = arrItem[1] + intIndex + "+";
					arrItem[3] = parseInt(arrItem[3]) + 1;
					if (arrItem[3] >= arrItem[2])
					{
						document.getElementById(strSubDB + 'All').checked = true;
					}
				}

			}

			document.getElementById("hdnUSPSubDB").value += arrItem[0] + "," + arrItem[1] +  "," + arrItem[2] +  "," + arrItem[3] + "|";
											}
		else
		{
			document.getElementById("hdnUSPSubDB").value += arrDB[i] + "|";
		}
	}
	document.getElementById("hdnUSPSubDB").value = document.getElementById("hdnUSPSubDB").value.substring(0,document.getElementById("hdnUSPSubDB").value.length - 1);
}
function ReplaceUSPSubDB(strSubDB,intIndex)
{
	//检索范围,+0+,1,1|SUBDB2,+2+,1,1
	//库名，选中的库，最多能选的库个数，已经选择的库个数
	var arrDB = document.getElementById("hdnUSPSubDB").value.split('|');
	document.getElementById("hdnUSPSubDB").value = "";
	for (i=0; i<arrDB.length; i++)

	{
		if (arrDB[i].indexOf(strSubDB) > -1)
		{
			arrDB[i] = arrDB[i].replace(/\+\d+\+/,'+' + intIndex + '+');
			document.getElementById("hdnUSPSubDB").value += arrDB[i] + "|";
		}
		else
		{
			document.getElementById("hdnUSPSubDB").value += arrDB[i] + "|";
		}
	}
	document.getElementById("hdnUSPSubDB").value = document.getElementById("hdnUSPSubDB").value.substring(0,document.getElementById("hdnUSPSubDB").value.length - 1);
}
function SubDBSelectAll(SubDBName,count)
{
		for (var ii=0; ii<=count+count; ii++)
		{
			if (document.getElementById(SubDBName + 'All').checked == true)
			{
				//全选
				if (document.getElementById(SubDBName + ii)!=null && document.getElementById(SubDBName + ii).checked == false)
				{
					document.getElementById(SubDBName + ii).click();
				}
			}
			else
			{
				//清除
				if (document.getElementById(SubDBName + ii)!=null && document.getElementById(SubDBName + ii).checked == true)
				{
					document.getElementById(SubDBName + ii).click();
				}
			}
		}
}
function SetFreEnabled()
{
try
{
	var disabled = false;
	if (document.getElementById("extension") != null)
	{
		disabled = document.getElementById("extension").checked;
	}
	var nId = document.getElementById("VarNum").value;
	var num = parseInt(nId);
	for(var i=1;i<= num;i++)
	{
		var freID = "advancedfrequency" + i;
		if (document.getElementById( freID ) != null)
		{
			document.getElementById( freID ).disabled=disabled;
			document.getElementById( freID ).style.backgroundColor=(disabled==true?'#ababab':'');
		}
	}
	if (disabled==true) return;
	for(var i=num;i>=1;i--)
	{
			var aqtemp = "advancedfrequency" + i;
			var avtemp = "advancedfield" + i;
			var avtemp1 = document.getElementById(avtemp).value;
			frequencyAndTips( aqtemp , avtemp1 );
	}
}
catch(err){}
if (typeof(CheckFieldForSCPD) == 'function') CheckFieldForSCPD();
}
function CheckInputValue()
{
try
{
		var count = parseInt(document.getElementById("VarNum").value);
		for (i = 1; i<=count; i++)
		{
			if (document.getElementById('advancedvalue' + i).value.indexOf('<') > -1 || document.getElementById('advancedvalue' + i).value.indexOf('>') > -1 )
			{ alert('您所输入的检索词中含有"<"或者">"符号！');
			return false;}
		}
}
catch(err)
{
}
}
function startWriteGroupControlVarToCookie()
{
	try
	{
		var nId1 = document.getElementById("VarNum").value;
		var num1 = parseInt(nId1);
		var sName = "";
		for(var i=1;i<=num1;i++)
		{
			//记下输入的检索词
			sName = "advancedvalue" + i;
			writeGroupControlVarToCookie( sName , 0 );

			//记下检索项
			sName = "advancedfield" + i;
			writeGroupControlVarToCookie( sName , 0 );

			if( i != 1 )
			{
				//记下逻辑关系 逻辑关系从2开始
				sName = "logical" + i;
				writeGroupControlVarToCookie( sName , 0 );
			}
		}
	}
	catch( err )
	{
	}
}
function getValueFromCookie( cookieName )
{
		var name = cookieName + "=";
		var isfound = false;
		var start = 0;
		var end = 0;
		var CookieString = document.cookie;
		var str = "";
		var i = 0;
		while( i < CookieString.length )
		{
			start = i;
			end = start + name.length;
			if( CookieString.substring(start,end) == name)
			{
				isfound = true;
				break;
			}
			i++;
		}

		if( isfound == true )
		{
			start = end;
			end = CookieString.indexOf(";",start);
			if(end < start)
				end = CookieString.length;
			str = unescape(CookieString.substring(start,end));
		}

		return str;
}
function getGroupControlVarFromCookie( controlName , flag )
{
	var str = getValueFromCookie( controlName );
	if( flag == 0 )
	{
		if( str != "" )
		{
			var q = 0;
			for (var q = 0; q < document.getElementsByName( controlName ).length; q++)
			{
				if (document.getElementByName( controlName ).options[q].value == str)
				{
					document.getElementByName( controlName ).options[q].selected = true;
				}
			}
			if( q == 0 )
			{
				document.getElementById( controlName ).value = str;
			}
		}
	}
	else
	{
		var arrIds = str.split(',');
		var i;
		for (i=0;i<document.getElementsByName( controlName ).length;i++)
		{
			for(var j=0;j< arrIds.length;j++)
			{
				if(document.getElementsByName( controlName )[i].value == arrIds[j])
				{
					document.getElementsByName( controlName )[i].checked = true;
					break;
				}
			}
		}

		if (i==0)
		{
			if( document.getElementById( controlName ).value == str )
			{
				document.getElementById( controlName ).checked = true;
			}
		}
	}
}
function startGetGroupControlVarFromCookie()
{
	try{
	var nId1 = document.getElementById("VarNum").value;
	var num1 = parseInt(nId1);
	var sName = "";
	for(var i=1;i<=num1;i++)
	{
		//还原输入的检索词
		sName = "advancedvalue" + i;
		getGroupControlVarFromCookie( sName , 0 );

		//还原检索项
		sName = "advancedfield" + i;
		getGroupControlVarFromCookie( sName , 0 );

		if( i != 1 )
		{
			//还原逻辑关系 逻辑关系从2开始
			sName = "logical" + i;
			getGroupControlVarFromCookie( sName , 0 );
		}
	}
	}
	catch( err )
	{
		//如果点的是-号，还原时可能原来的最后一个己经不存在了，所以报错。
	}
}
function frequencyAndTips( ctlDisabled , curSelectedValue)
{
if( curSelectedValue == "ffd" )
{
	document.getElementById("order").value = "relevant";
	document.getElementById("order").text = "相关度";
}
}
	function ttodGetNaviItemCookies()
	{
		var cookieName = "nNaviItem";
		var str = getValueFromCookie( cookieName )
		if( str != "" )
		{
			document.getElementById("VarNum").value = str;
			return true;
		}
		else
		{
			var nId = document.getElementById("VarNum").value;
			document.cookie = "nNaviItem=" + nId;
		}
		return;
	}

	function ttodAddNaviItemCookies()
	{
		var cookieName = "nNaviItem";
		var str = getValueFromCookie( cookieName )
		//if( str != "" )
		//{
		//	document.getElementById("VarNum").value = str;
		//}
		var nId = document.getElementById("VarNum").value;
		nId = parseInt( nId ) + 1;
		document.all("VarNum").value = nId;
		document.cookie = "nNaviItem=" + nId;
		return;
	}
	function ttodRemoveNaviItemCookies()
	{
		var cookieName = "nNaviItem";
		var str = getValueFromCookie( cookieName )
		//if( str != "" )
		//{
		//	document.getElementById("VarNum").value = str;
			if(document.getElementById("VarNum").value == 0)
				document.getElementById("VarNum").value = 1;
		//}
		var nId = document.getElementById("VarNum").value;
		nId = parseInt( nId );
		if( nId > 1 )
		{
			nId = nId - 1;
		}
		document.getElementById("VarNum").value = nId;
		document.cookie = "nNaviItem=" + nId;
		return;
	}