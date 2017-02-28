import pymysql
import os

_rootPath = "D:\\工作\\代码生成\\ccdm\\" #保存文件路径
_dbAddress = "localhost"
_dbUser = "root"
_dbPwd = "root"
_dbName = "ccdm"

#详细页面代码生成
def DetailAction(_table,_columns,_path):
    _tableName = "%s" % _table
    _tableName = _tableName.split('_')[2]
    _html = ""
    for _columnItem in _columns:
        if _columnItem[19]!="":
            _html+="<div class=\"row col-xs-12\">\r"
            _html+="<label class=\"col-xs-6 control-label pull-left\" for=\"form-field-1\"> "+_columnItem[19]+"：@Model."+_columnItem[3]+" </label>\r"
            _html+="</div>\r"
    _filePath = _path + "\\Detail.cshtml"
    fo = open(_filePath, "w+")
    fo.write(_html)
    fo.close()

#新增页面代码生成
def NewAction(_table,_columns,_path):
    _tableName = "%s" % _table
    _tableName = _tableName.split('_')[2]
    _html = "@using (Ajax.BeginForm(\"do" + _tableName.capitalize() + "\", \"" + _tableName.capitalize() + "\", new AjaxOptions { HttpMethod = \"POST\", OnSuccess = \"handle_resp\", OnFailure = \"failed_resp\", OnBegin = \"ajax_OnBegin\", OnComplete = \"ajax_OnComplete\" }, new { @id = \"checkout-form\", @class = \"form-horizontal\", @role = \"form\" }))\r"
    _html+="{\r"

    _html+="<div class=\"modal-body\">\r"
    for _columnItem in _columns:
        if _columnItem[19]=="":
            _html+="@Html.HiddenFor(m => m."+_columnItem[3]+ ", new { @id = \""+_columnItem[3]+ "_" + _columnItem[7]+"\"})\r";
        else:
            _html+="<div class=\"form-group\">\r"
            _html+="<label class=\"col-xs-4 control-label \" for=\"form-field-1\"> " + _columnItem[19] + "： </label>\r"
            _html+="<div class=\"col-xs-8\">\r"
            _html+="@Html.TextBoxFor(m => m."+_columnItem[3]+ ", new { @id = \""+_columnItem[3]+ "_" + _columnItem[7]+"\", @class =\"col-xs-10 col-sm-10 \", @placeholder = \"请输入" + _columnItem[19] + "\" })\r";
            _html+="</div>\r"
            _html+="</div>\r"

    _html+="</div>\r"
    _html+="}"
    _filePath = _path + "\\New.cshtml"
    fo = open(_filePath, "w+")
    fo.write(_html)
    fo.close()

#编辑页面代码生成
def EditAction(_table,_columns,_path):
    _tableName = "%s" % _table
    _tableName = _tableName.split('_')[2]
    _html = "@using (Ajax.BeginForm(\"do" + _tableName.capitalize() + "\", \"" + _tableName.capitalize() + "\", new AjaxOptions { HttpMethod = \"POST\", OnSuccess = \"handle_resp\", OnFailure = \"failed_resp\", OnBegin = \"ajax_OnBegin\", OnComplete = \"ajax_OnComplete\" }, new { @id = \"checkout-form\", @class = \"form-horizontal\", @role = \"form\" }))\r"
    _html+="{\r"

    for _columnItem in _columns:
        if _columnItem[19]=="":
            _html+="@Html.HiddenFor(m => m."+_columnItem[3]+ ", new { @id = \""+_columnItem[3]+ "_" + _columnItem[7]+"\"})\r";
        else:
            _html+="<div class=\"form-group\">\r"
            _html+="<label class=\"col-xs-4 control-label \" for=\"form-field-1\"> " + _columnItem[19] + "： </label>\r"
            _html+="<div class=\"col-xs-8\">\r"
            _html+="@Html.TextBoxFor(m => m."+_columnItem[3]+ ", new { @id = \""+_columnItem[3]+ "_" + _columnItem[7]+"\", @class =\"col-xs-10 col-sm-10 \", @placeholder = \"请输入" + _columnItem[19] + "\" })\r";
            _html+="</div>\r"
            _html+="</div>\r"

    _html+="<div class=\"clearfix form-actions\">\r"
    _html+="<div class=\"col-md-offset-5 col-md-9\">\r"
    _html+="<button class=\"btn btn-info\" type=\"submit\">\r"
    _html+="<i class=\"ace-icon fa fa-check bigger-110\"></i>\r"
    _html+="Save（保存）\r"
    _html+="</button>\r"
    _html+="</div>\r"
    _html+="</div>\r"
    _html+="}"
    _filePath = _path + "\\Edit.cshtml"
    fo = open(_filePath, "w+")
    fo.write(_html)
    fo.close()

#列表页代码生成
def ListAction(_table,_columns,_path):
    _tableName = "%s" % _table
    _tableName = _tableName.split('_')[2]
    #循环HTML table列表结构
    _html = "<table id=\"dynamic-table"+_tableName.capitalize()+"\" class=\"table table-striped table-bordered table-hover\">\r"
    _html += "<thead>\r"
    _html += "<tr>\r"
    for _columnItem in _columns:
        _html += "<th>"+_columnItem[19]+"</th>\r"

    _html += "<th>操作</th>\r"
    _html += "</tr>\r"
    _html += "</thead>\r"
    _html += "</table>\r"
    #结束 循环HTML table列表结构
    _html+="\r\n\r\n"
    #开始循环js内容
    _html+="@section pagespecific {\r";
    _html+="<script src=\"@Url.Content(\"~/assets/js/jquery.dataTables.min.js\")\"></script>\r";
    _html+="<script src=\"@Url.Content(\"~/assets/js/jquery.dataTables.bootstrap.min.js\")\"></script>\r";
    _html+="<script src=\"@Url.Content(\"~/assets/js/dataTables.select.min.js\")\"></script>\r";
    _html+="<script src=\"@Url.Content(\"~/assets/js/dataTables.buttons.min.js\")\"></script>\r";

    _html+="<script>\r";
    _html+="var _dynamicTable"+_tableName.capitalize()+" = $('#dynamic-table"+_tableName.capitalize()+"').dataTable({\r";
    _html+="\"processing\": true,\r";
    _html+="\"serverSide\": true,\r";
    _html+="\"ordering\": false,\r";
    _html+="\"pagingType\": \"full_numbers\",\r";
    _html+="\"language\": {\r";
    _html+="\"lengthMenu\": \"每页 _MENU_ 条记录\",\r";
    _html+="\"zeroRecords\": \"目前还没有任何数据\",\r";
    _html+="\"info\": \"当前第：_PAGE_ 页 共：_PAGES_ 页\",\r";
    _html+="\"infoEmpty\": \"目前还没有任何数据\",\r";
    _html+="\"sSearch\": \"搜索\",\r";
    _html+="\"oPaginate\": {\r";
    _html+="\"sFirst\": \"第一页\",\r";
    _html+="\"sPrevious\": \"上一页\",\r";
    _html+="\"sNext\": \"下一页\",\r";
    _html+="\"sLast\": \"最后一页\"\r";
    _html+="}\r";
    _html+="},\r";
    _html+="\"ajax\": {\r";
    _html+="\"url\": \"@Url.Action(\"Get"+_tableName.capitalize()+"ListData\", \""+_tableName.capitalize()+"\")\",\r";
    _html+="\"type\": \"POST\"\r";
    _html+="},\r";
    _html+="\"columns\": [\r";
    for _columnItem in _columns:
        _html+="{\"data\": \""+_columnItem[3]+"\"},"

    _html+="{ \"data\": \"id\" }\r";
    _html+="],\r";
    _html+="\"columnDefs\": [\r";
    _html+="{\r";
    _html+="\"targets\": -1,//-1表示最后一行\r";
    _html+="render: function (data, type, full, meta) {\r";
    _html+="var _btns = \"<div class=\"hidden-sm hidden-xs action-buttons\">\";\r";
    _html+="_btns += \"<a class=\"blue\" href=\"@Url.Action(\"Detail"+_tableName.capitalize()+"\",\""+_tableName.capitalize()+"\")?id=\" + data + "">\";\r";
    _html+="_btns += \"<i class=\"ace-icon fa fa-search-plus bigger-130\"></i>详细\";\r";
    _html+="_btns += \"</a>\";\r";
    _html+="_btns += \"<a class=\"green\" href=\"@Url.Action(\"Edit"+_tableName.capitalize()+"\",\""+_tableName.capitalize()+"\")?id=\" + data + "">\";\r";
    _html+="_btns += \"<i class=\"ace-icon fa fa-pencil bigger-130\"></i>编辑\";\r";
    _html+="_btns += \"</a>\";\r";
    _html+="_btns += \"<a class=\"red\" href=\"#\" onclick=\"dialogConfirm"+_tableName.capitalize()+"_click('\" + data + \"')\">\";\r";
    _html+="_btns += \"<i class=\"ace-icon fa fa-trash-o bigger-130\"></i>删除\";\r";
    _html+="_btns += \"</a>\";\r";
    _html+="_btns += \"</div>\";\r";
    _html+="return _btns;\r";
    _html+="}\r";
    _html+="}]\r";
    _html+="});\r";
    _html+="$(\"#dynamic-table"+_tableName.capitalize()+"_length\").parent().parent().hide();\r";
    _html+="function delete"+_tableName.capitalize()+"_click(id) {\r";
    _html+="$.axs('@Url.Action(\"doDelete"+_tableName.capitalize()+"\", \""+_tableName.capitalize()+"\")', { id: id }, function (data) {\r";
    _html+="if (data.flag) {\r";
    _html+="_dynamicTable"+_tableName.capitalize()+".DataTable().ajax.reload();\r";
    _html+="} else {\r";
    _html+="bootbox.dialog({\r";
    _html+="message: data.msg,\r";
    _html+="buttons: {\r";
    _html+="\"success\": {\r";
    _html+="\"label\": \"确定\",\r";
    _html+="\"className\": \"btn-sm btn-primary\"\r";
    _html+="}\r";
    _html+="}\r";
    _html+="});\r";
    _html+="}\r";
    _html+="});\r";
    _html+="}\r";
    _html+="function dialogConfirm"+_tableName.capitalize()+"_click(id)\r";
    _html+="{\r";
    _html+="$(\"#dialog-confirm\").removeClass('hide').dialog({\r";
    _html+="resizable: false,\r";
    _html+="width: '320',\r";
    _html+="modal: true,\r";
    _html+="title: \"是否清空该数据？\",\r";
    _html+="title_html: true,\r";
    _html+="buttons: [\r";
    _html+="{\r";
    _html+="html: \"<i class='ace-icon fa fa-trash-o bigger-110'></i>&nbsp; 删除\",\r";
    _html+="\"class\": \"btn btn-danger btn-minier\",\r";
    _html+="click: function () {\r";
    _html+="delete"+_tableName.capitalize()+"_click(id);\r";
    _html+="$(this).dialog(\"close\");\r";
    _html+="}\r";
    _html+="}\r";
    _html+=",\r";
    _html+="{\r";
    _html+="html: \"<i class='ace-icon fa fa-times bigger-110'></i>&nbsp; 取消\",\r";
    _html+="\"class\": \"btn btn-minier\",\r";
    _html+="click: function () {\r";
    _html+="$(this).dialog(\"close\");\r";
    _html+="}\r";
    _html+="}\r";
    _html+="]\r";
    _html+="});\r";
    _html+="}\r";
    _html+="</script>\r";
    _html+="}\r";

    _filePath = _path + "\\List.cshtml"
    fo = open(_filePath, "w+")
    fo.write(_html)
    fo.close()

#控制器代码生成
def ControllerAction(_table,_columns,_path):
    _fullTableName = "%s" % _table
    _tableName = _fullTableName.split('_')[2]

    _html = "BaseRepository<"+_fullTableName+"> _Rep"+_tableName.capitalize()+" = new BaseRepository<"+_fullTableName+">();\r"
    _html += "/// <summary>\r"
    _html += "/// 列表\r"
    _html += "/// </summary>\r"
    _html += "/// <returns>列表页</returns>\r"
    _html += "public ActionResult List()\r"
    _html += "{\r"
    _html += "return View();\r"
    _html += "}\r\n"
    _html += "/// <summary>\r"
    _html += "/// 编辑\r"
    _html += "/// </summary>\r"
    _html += "/// <param name=\"id\">主键</param>\r"
    _html += "/// <returns>编辑页</returns>\r"
    _html += "public ActionResult Edit"+_tableName.capitalize()+"(string id)\r"
    _html += "{\r"
    _html += "var model = _Rep"+_tableName.capitalize()+".FindEntities(id);\r"
    _html += "return View(model);\r"
    _html += "}\r\n"

    _html += "/// <summary>\r"
    _html += "/// 查询分页数据集\r"
    _html += "/// </summary>\r"
    _html += "/// <param name=\"param\">DataTables 页面参数</param>\r"
    _html += "/// <returns>返回Json数据集</returns>\r"
    _html += "public JsonResult Get"+_tableName.capitalize()+"ListData(DataTableParam param)\r"
    _html += "{\r"
    _html += "try\r"
    _html += "{\r"
    _html += "int _total = 0;\r"
    _html += "var _data = _Rep"+_tableName.capitalize()+".LoadOffSetEntities(param.Start, param.Length, out _total, false, o => o.createDate).ToList();\r"
    _html += "DataTablesResult<"+_fullTableName+"> dtr = new DataTablesResult<"+_fullTableName+">(param.Draw, _total, _total, _data);\r"
    _html += "return Json(dtr);\r"
    _html += "}\r"
    _html += "catch\r"
    _html += "{\r"
    _html += "return Json(new DataTablesResult<"+_fullTableName+">(0, 0, 0, new List<"+_fullTableName+">()));\r"
    _html += "}\r"
    _html += "}\r\n"
    _html += "/// <summary>\r"
    _html += "/// 新增或编辑保存数据\r"
    _html += "/// </summary>\r"
    _html += "/// <param name=\"model\">要保存的实体</param>\r"
    _html += "/// <returns>返回Msg</returns>\r"
    _html += "public JsonResult do"+_tableName.capitalize()+"("+_fullTableName+" model)\r"
    _html += "{\r"
    _html += "Msg _msg = new Msg();\r"
    _html += "try\r"
    _html += "{\r"
    _html += "if (string.IsNullOrEmpty(model.id))\r"
    _html += "{\r"
    _html += "model.id = Utils.GetRamCode();\r"
    _html += "model.createDate = DateTime.Now;\r"
    _html += "model.createID = GetUserID();\r"
    _html += "model.updateDate = DateTime.Now;\r"
    _html += "model.updateID = GetUserID();\r"
    _html += "if (_Rep"+_tableName.capitalize()+".AddEntities(model) != null)\r"
    _html += "{\r"
    _html += "_msg.flag = true;\r"
    _html += "_msg.data = Url.Action(\"List\");\r"
    _html += "_msg.other = \"跳转\";\r"
    _html += "_msg.msg = \"新增成功\";\r"
    _html += "}\r"
    _html += "}\r"
    _html += "else\r"
    _html += "{\r"
    _html += "model.updateDate = DateTime.Now;\r"
    _html += "model.updateID = GetUserID();\r"
    _html += "if (_Rep"+_tableName.capitalize()+".UpdateEntities(model))\r"
    _html += "{\r"
    _html += "_msg.flag = true;\r"
    _html += "_msg.data = Url.Action(\"List\");\r"
    _html += "_msg.other = \"跳转\";\r"
    _html += "_msg.msg = \"更新成功\";\r"
    _html += "}\r"
    _html += "else\r"
    _html += "{\r"
    _html += "_msg.other = \"不跳转\";\r"
    _html += "_msg.msg = \"更新失败\";\r"
    _html += "}\r"
    _html += "}\r"
    _html += "}\r"
    _html += "catch \r"
    _html += "{\r\n"
    _html += "}\r"
    _html += "return Json(_msg);\r"
    _html += "}\r\n"
    _html += "/// <summary>\r"
    _html += "/// 删除\r"
    _html += "/// </summary>\r"
    _html += "/// <param name=\"id\">主键</param>\r"
    _html += "/// <returns>成功返回Msg.flag=true，失败Msg.flag=false</returns>\r"
    _html += "public JsonResult doDelete"+_tableName.capitalize()+"(string id)\r"
    _html += "{\r"
    _html += "Msg _msg = new Msg();\r"
    _html += "try\r"
    _html += "{\r"
    _html += "if (string.IsNullOrEmpty(id))\r"
    _html += "{\r"
    _html += "_msg.msg = \"找不到内容\";\r"
    _html += "}\r"
    _html += "else\r"
    _html += "{\r"
    _html += "var _model = _Rep"+_tableName.capitalize()+".FindEntities(id);\r"
    _html += "_Rep"+_tableName.capitalize()+".DeleteEntities(_model);\r"
    _html += "_msg.flag = true;\r"
    _html += "}\r"
    _html += "}\r"
    _html += "catch \r"
    _html += "{\r\n"
    _html += "}\r"
    _html += "return Json(_msg);\r"
    _html += "}\r"

    _html += "/// <summary>\r"
    _html += "/// 根据主键id查找数据\r"
    _html += "/// </summary>\r"
    _html += "/// <param name=\"id\">主键id</param>\r"
    _html += "/// <returns>json</returns>\r"
    _html += "public JsonResult Get"+_tableName.capitalize()+"DataByID(string id)\r"
    _html += "{\r"
    _html += "Msg _msg = new Msg();\r"
    _html += "string _supplierID = Session[Keys.SUPPLIERID].ToString();\r"
    _html += "var _m"+_tableName.capitalize()+" = _Rep"+_tableName.capitalize()+".GetFirst(w => w.supplierCompanyID == _supplierID && w.id == id);\r"
    _html += "_msg.flag = _m"+_tableName.capitalize()+" != null && !string.IsNullOrEmpty(_m"+_tableName.capitalize()+".id);\r"
    _html += "_msg.data = _m"+_tableName.capitalize()+";\r"
    _html += "_msg.msg = !_msg.flag ? \"无法找到对应数据\" : \"操作成功\";\r"
    _html += "return Json(_msg);\r"
    _html += "}"
    _filePath = _path + "\\Controller.cs"
    fo = open(_filePath, "w+")
    fo.write(_html)
    fo.close()

def EditJavaScript(_table,_columns,_path):
    _tableName = "%s" % _table
    _tableName = _tableName.split('_')[2]
    _html = "function Modaltable"+_tableName.capitalize()+"_click(id) {\r"
    _html += "$.axs('@Url.Action(\"Get"+_tableName.capitalize()+"DataByID\", \""+_tableName.capitalize()+"\")', { id: id }, function (res) {\r"
    _html += "if (res.flag) {\r"
    for _columnItem in _columns:
        _id = _columnItem[3]+ "_" + _columnItem[7]
        _html += "$('#my-modal"+_tableName.capitalize()+"  #"+_id+"').val(res.data."+_columnItem[3]+");\r"
    
    _html += "$('#my-modal"+_tableName.capitalize()+"').modal('show');\r"
    _html += "} else {\r"
    _html += "bootbox.dialog({\r"
    _html += "message: res.msg,\r"
    _html += "buttons: {\r"
    _html += "\"success\": {\r"
    _html += "\"label\": \"确定\",\r"
    _html += "\"className\": \"btn-sm btn-primary\"\r";
    _html += "}\r"
    _html += "}\r"
    _html += "});\r"
    _html += "}\r"
    _html += "});\r"
    _html += "}\r"

    _html += "function NewModaltable"+_tableName.capitalize()+"_click() {\r"
    for _columnItem in _columns:
        _id = _columnItem[3]+ "_" + _columnItem[7]
        _html += "$('#my-modal"+_tableName.capitalize()+"  #"+_id+"').val(\"\");\r"

    _html += "$('#my-modal"+_tableName.capitalize()+"').modal('show');\r"
    _html += "}\r"
    _filePath = _path + "\\javascript.txt"
    fo = open(_filePath, "w+")
    fo.write(_html)
    fo.close()

db = pymysql.connect(_dbAddress,_dbUser,_dbPwd,_dbName,charset='utf8')#数据库链接地址、账号、密码、数据库名称

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL 查询
cursor.execute("show tables")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()
for row in data:
    _path = _rootPath + "%s" % row
    if(os.path.exists(_path) == False):
        os.makedirs(_path)
    _sqlGetColumns = " select * from information_schema.columns "
    _where = " where table_schema ='" + _dbName + "' and table_name = '%s'" % row
    cursor.execute(_sqlGetColumns + _where)
    _preporetyList = cursor.fetchall()
    NewAction(row,_preporetyList,_path)
    EditAction(row,_preporetyList,_path)
    ListAction(row,_preporetyList,_path)
    ControllerAction(row,_preporetyList,_path)
    EditJavaScript(row,_preporetyList,_path)
    DetailAction(row,_preporetyList,_path)
    print("=========%s代码生成完成=========="% row)

# 关闭数据库连接
db.close()
print("操作完成")

