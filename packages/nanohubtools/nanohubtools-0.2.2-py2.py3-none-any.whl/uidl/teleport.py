import json 
import requests
import jsonschema


class TeleportGlobals():
    def __init__(self, *args, **kwargs):
        self.settings = {'language' : 'en', 'title' : ''}
        self.assets = []
        self.meta = []
        self.manifest = {}
        
    def __json__(self):
        return {
            "settings" : self.settings,
            "assets" : self.assets,
            "meta" : self.meta,
            "manifest" : self.manifest
        }
    
    def __str__(self):
        return json.dumps(self.__json__())
        
    def buildReact(self):
      react = ""
      for asset in self.assets:
        if asset["type"] == "script":          
          react += asset["content"] + "\n";
        if asset["type"] == "style":
          react += "var tstyle = document.createElement('style')\n";
          react += "document.head.appendChild(tstyle);\n";
          react += "tstyle.sheet.insertRule('" + asset["content"] + "');\n";
      return react
      
        
class TeleportApp():
    def __init__(self, app_name, main_component, *args, **kwargs):
        self.app_name = app_name
        self.definitions = {"main": main_component}
        self.default = list(self.definitions.keys())[0]
        
    def __json__(self):
        return {
            "name" : self.app_name,
            "stateDefinitions" : {
                "route" : {
                    "type": "string",
                    "defaultValue": self.default,  
                    "values" : [{ 
                        "value": k,
                        "pageOptions": {
                            "navLink": "/"+k,
                            "componentName": v
                        }
                    } for k,v in self.definitions.items()]
                }
            },
            "node" : {
                "route" : {
                    "type": "element",
                    "content": {
                        "elementType": "Router",
                        "children" : [{ 
                            "node"
                            "type": "conditional",
                            "content": {
                                "node" : {
                                  "type": "element",
                                  "content": {
                                    "elementType": "container",
                                    "children": [{
                                      "type": "element",
                                      "content": {
                                        "elementType": v,
                                        "dependency": {
                                          "type": "local"
                                        }
                                      }
                                    }]
                                  }
                                },
                                "value" : k,
                                "reference": {
                                    "type": "dynamic",
                                    "content": {
                                        "referenceType": "state",
                                        "id": "route"
                                    }
                                }
                            }
                        } for k,v in self.definitions.items()]
                    }
                }
            },
        }
    
    def __str__(self):
        return json.dumps(self.__json__())

class TeleportNode():
  def __init__(self, *args, **kwargs):
    self.type = ""
    self.content = None
    
  def __json__(self):
    return {
      "type": self.type,
      "content" : self.contentToJson(),
    }
    
  def contentToJson(self):
    if self.content is None:
      return {}
    else:
      return self.content.__json__()      
  
  def __str__(self):
      return json.dumps(self.__json__())

  def buildReact(self):   
    react = ""
    if self.content == None:
      react += "React.createElement('div', {key:Util.create_UUID()}, '')\n"
    else:
      if self.type == "static":
        react += "React.createElement('div', {key:Util.create_UUID()}, '" + str(self.content).replace("'", "\"") + "')\n"
      else:
        react += self.content.buildReact()
    return react
        

class TeleportElement(TeleportNode):
  def __init__(self, content, *args, **kwargs):
    TeleportNode.__init__(self)
    self.type = "element"      
    self.content = content
    
  def addContent(self, child):
    self.content.children.append(child)
    
'''
class TeleportDynamic(TeleportNode):
  def __init__(self, *args, **kwargs):
    TeleportNode.__init__(self)
    self.type = "dynamic"      
    self.content = "TODO"
'''


class TeleportStatic(TeleportNode):
  def __init__(self, *args, **kwargs):
    TeleportNode.__init__(self)
    self.type = "static"      
    self.content = kwargs.get("content", "")

  def __json__(self):
    return {
      "type": self.type,
      "content" : self.content,
    }    

        
class TeleportComponent():
  def __init__(self, name_component, node, *args, **kwargs):
      self.name_component = name_component;
      self.propDefinitions = {}
      self.stateDefinitions = {}
      self.node = node
      
  def __json__(self):
      return {
        "name":self.name_component,
        "propDefinitions" : self.propDefinitions,
        "stateDefinitions" : self.stateDefinitions,
        "node" : self.node.__json__()
      }
  
  def __str__(self):
      return json.dumps(self.__json__())

  def addNode(self, child):
    if (isinstance(child, TeleportNode) ):
      self.node.addContent(child)
    else:
      raise AttributeError("children have to be Node types")

  def addStateVariable(self, state, definition={type:"string", "defaultValue":""}):
    if isinstance(definition, dict):
      if ("type" in definition and "defaultValue" in definition):
        self.stateDefinitions[state] =  {"type": definition["type"], "defaultValue": definition["defaultValue"] }
      else:
        raise AttributeError("type and/or defaultValue are missing on the definition")
        
    else:
      raise AttributeError("definition should be a dict")

  def addPropVariable(self, state, definition={type:"string", "defaultValue":""}):
    if isinstance(definition, dict):
      if ("type" in definition and "defaultValue" in definition):
        self.propDefinitions[state] =  {"type": definition["type"], "defaultValue": definition["defaultValue"] }
      else:
        raise AttributeError("type and/or defaultValue are missing on the definition")
        
    else:
      raise AttributeError("definition should be a dict")

  
  def buildReact(self, componentName):   
    react = ""
    react += "class " + componentName + " extends React.Component {\n"
    react += "constructor(props) {\n"
    react += "super(props);\n"
    react += "this.state = {\n"
    for k,s in self.stateDefinitions.items():
      react += "'" + str(k) + "' : " + json.dumps(s['defaultValue']) + ", \n"
    react += "};\n"
    react += "}; \n"
    react += "render(){\n"
    react += "var children = [];\n"
    react += "let self=this;\n"
    react += "children.push(\n"
    react += self.node.buildReact()
    react += ")\n"
    react += "var node = React.createElement('div', {key:Util.create_UUID()}, children)  \n"              
    react += "return node;\n"
    react += "}\n"
    react += "}\n"
    return react

class TeleportProject():
  def __init__(self, name, *args, **kwargs):
      self.project_name = name
      self.globals = TeleportGlobals();
      self.app = TeleportApp(name, "MainComponent");
      self.components = {
        "MainComponent" : TeleportComponent("MainComponent", TeleportElement(TeleportContent(elementType="container")))
      };
      self.components["MainComponent"].node.content.style = {
        "height": "100vh",
      }
      
  def __json__(self):
      return {
          "$schema": "https://docs.teleporthq.io/uidl-schema/v1/project.json",
          "name": self.project_name,
          "globals" : self.globals.__json__(),
          "root" : self.app.__json__(),
          "components" : {k:v.__json__() for k,v in self.components.items()}
      }
  
  def __str__(self):
      return json.dumps(self.__json__())
      
  def validate (self):
    return True;
    response = requests.get("https://docs.teleporthq.io/uidl-schema/v1/project.json")    
    if (response.text != ""):      
      schema = response.json()
      schema = json.dumps(schema)
      #v = jsonschema.Draft6Validator(response.text).validate(self.__json__())
      v = jsonschema.Draft6Validator(schema, (), jsonschema.RefResolver("https://docs.teleporthq.io/uidl-schema/v1/", ""))
      v = v.validate(self.__json__())
      return v;

  def buildReact(self):
    react = ""
    react += "<!DOCTYPE html>\n"
    react += "<html style='height:100%'>\n"
    react += "<head>\n"
    react += "<meta charset='UTF-8'/>\n"
    react += "<title>Hello World</title>\n"
    react += "<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>\n"
    react += "<script src='https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js'></script>\n"
    react += "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'/>\n"
    react += "</head>\n"
    react += "  <body style='padding:0;margin:0;height:100%'>\n"
    react += "    <div id='root' style='height:100vh'></div>\n"
    react += "<script type='text/javascript'>\n"
    react += "requirejs.config({\n"
    react += "    paths: {\n"
    react += "        'react': 'https://unpkg.com/react@16.8.6/umd/react.development',\n"
    react += "        'react-dom': 'https://unpkg.com/react-dom@16.8.6/umd/react-dom.development',\n"
    react += "        'material-ui': 'https://unpkg.com/@material-ui/core@latest/umd/material-ui.development',\n"
    react += "        'plotlycomponent': 'https://unpkg.com/react-plotly.js@2.2/dist/create-plotly-component',\n"
    react += "        'axios': 'https://unpkg.com/axios/dist/axios.min',\n"
    react += "    }\n"
    react += "});\n"
    react += "requirejs(['react', 'react-dom', 'material-ui', 'axios'], function(React, ReactDOM, Material, Axios) {\n"
    react += "  window.React = React\n"
    react += "  requirejs(['plotlycomponent'], function(PlotlyComponent) {\n"
    react += "    window.React = React\n"
    react += "    const Plot = PlotlyComponent(Plotly);\n";
    react += "    class Util {\n"
    react += "        static create_UUID(){\n"
    react += "            var dt = new Date().getTime();\n"
    react += "            var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {\n"
    react += "                var r = (dt + Math.random()*16)%16 | 0;\n"
    react += "                dt = Math.floor(dt/16);\n"
    react += "                return (c=='x' ? r :(r&0x3|0x8)).toString(16);\n"
    react += "            });\n"
    react += "            return uuid;\n"
    react += "        }\n"
    react += "    }\n"
    react += self.globals.buildReact();
    for k, v in self.components.items():
      react += v.buildReact(k)
    react += "    ReactDOM.render(\n"
    react += "        React.createElement(MainComponent, {key:Util.create_UUID()}),\n"
    react += "        document.getElementById('root')\n"
    react += "    );\n"
    react += "  })    \n"
    react += "})    \n"
    react += "</script>\n"
    react += "  </body>\n"
    react += "</html>\n"
    f = open("tempreact.html", "w")
    f.write(react)
    f.close()
    return react
        
        
class TeleportContent():
  def __init__(self, *args, **kwargs):
    self.elementType = kwargs.get("elementType", None)
    self.attrs = {}
    self.events = {}
    self.style = {}
    self.children = []
    self.name =  kwargs.get("name", None)
    
  def __json__(self):
    tjson = {}
    if self.name != None:
      tjson["name"] = self.name
    if self.elementType != None:
      tjson["elementType"] = self.elementType
    if len(self.style) > 0:
      tjson["style"] = self.style
    if len(self.attrs) > 0:
      tjson["attrs"] = self.attrs # False -> "false"
    if len(self.events) > 0:
      tjson["events"] = self.events
    if len(self.children) > 0:
      tjson["children"] = [component.__json__() for component in self.children]
    return tjson
  
  def __str__(self):
      return json.dumps(self.__json__())             

  def buildElementType(self):   
    elementType = self.elementType
    if elementType == "container":
      elementType = "'div'"
    return elementType

  def buildReact(self):   
    react = ""
    elementType = self.buildElementType()
    if elementType == "container":
      elementType = "'div'"
    react += "React.createElement("+elementType+", {key:Util.create_UUID()"
    sep = " ,"
    for attr, value in self.attrs.items():
      v = value
      if isinstance(value,dict):
        if "type" in value and "content" in value:
          content = value["content"]
          if (value["type"] == "dynamic"):
            if ("referenceType" in content and content["referenceType"] == "state"):
              v = "self.state['" + content["id"] + "']";
            elif ("referenceType" in content and content["referenceType"] == "prop"):
              v = "self.props['" + content["id"] + "']";
            elif ("referenceType" in content and content["referenceType"] == "local"):
              v = "" + content["id"] + "";
      else: 
        v = str(json.dumps(v))
      react += sep + "'"+ attr + "': " + v + ""

    valid_events = {
      "click": "onClick",
      "focus": "onFocus",
      "blur": "onBlur",
      "change": "onChange",
      "submit": "onSubmit",
      "keydown": "onKeyDown",
      "keyup": "onKeyUp",
      "keypress": "onKeyPress",
      "mouseenter": "onMouseEnter",
      "mouseleave": "onMouseLeave",
      "mouseover": "onMouseOver",
      "select": "onSelect",
      "touchstart": "onTouchStart",
      "touchend": "onTouchEnd",
      "scroll": "onScroll",
      "load": "onLoad"
    };
    for ev, list in self.events.items():
      if ev in valid_events:
        v = "function(e){"
        for func in list:  
    
          if "type" in func and func["type"] == "stateChange":
            v += "self.setState({'" + str(func["modifies"]) + "':" + json.dumps(func["newState"]) + "}); "
          elif "type" in func and func["type"] == "logging":
            v += "console.log('" + str(func["modifies"]) + "', " + str(json.dumps(func["newState"])) + "); "
          elif "type" in func and func["type"] == "propCall":
            v += str(func["calls"]) + "(" + ", ".join(func["args"]) + ");"
            
        v += "}"
        if v != "function(){}": 
          react += sep + "'"+ valid_events[ev] + "': " + v + ""
    if len(self.style) > 0:
      react += sep + "'style': " + json.dumps(self.style) + ""
    react += "}"

    if len(self.children) > 0:

      if len(self.children) == 1:
        react += ",\n"
        for child in self.children:
          react += child.buildReact()
        react += ")\n"
      else:
        react += ",[\n"
        sep = ""
        for child in self.children:
          react += sep + child.buildReact()
          sep = " ,"
        react += "])\n"
    else:
      react += ")\n"
    
    return react

class MaterialContent(TeleportContent):

  def buildElementType(self):   
    elementType = self.elementType
    return "Material." + elementType



class MaterialBuilder():
  def AppBar(*args, **kwargs):
    AppBar = TeleportElement(MaterialContent(elementType="AppBar"))
    AppBar.content.attrs["position"] = "static"
    if kwargs.get("style_state", None) is not None:
      AppBar.content.attrs["className"] = {
        "type": "dynamic",
        "content": {
          "referenceType": "state",
          "id": kwargs.get("style_state")
        }    
      }
    AppBar.content.style = {'width': 'inherit'}
      
    ToolBar = TeleportElement(MaterialContent(elementType="Toolbar"))
    ToolBar.content.attrs["variant"] = kwargs.get("variant", "regular")
    IconButton = TeleportElement(MaterialContent(elementType="IconButton"))
    IconButton.content.attrs["edge"] = "start"
    IconButton.content.attrs["color"] = "inherit"
    IconButton.content.attrs["aria-label"] = "menu"
    if kwargs.get("onClickMenu", None) is not None:
      IconButton.content.events["click"] = kwargs.get("onClickMenu", [])
      
      
    Icon = TeleportElement(MaterialContent(elementType="Icon"))
    IconText = TeleportStatic(content="menu")
    Icon.addContent(IconText)
    IconButton.addContent(Icon)
    Typography = TeleportElement(MaterialContent(elementType="Typography"))
    Typography.content.attrs["variant"] = "h6"
    TypographyText = TeleportStatic(content=kwargs.get("title", ""))
    Typography.addContent(TypographyText)

    ToolBar.addContent(IconButton)
    ToolBar.addContent(Typography)
    AppBar.addContent(ToolBar)
    return AppBar

  def Drawer(*args, **kwargs):
    """This function creates a Material Element of type drawer.
    Kwargs:
    variant (string): variant type of Drawer ['permanent' | 'persistent' | 'temporary'].
    anchor (string) : Side from which the drawer will appear.  'left' | 'top' | 'right' | 'bottom'
    open (bool/string): If true, the drawer is open. If string, the drawer reacts to the state variable 
    onClickClose(dict) : Callback fired when the drawer requests to be closed.
    
    Returns:
      TeleportElement

    Raises:
       AttributeError

    >>> Drawer(state="DrawerIsVisible", position="static", "variant":"dense" )

    """  

    Drawer = TeleportElement(MaterialContent(elementType="Drawer"))
    Drawer.content.attrs["variant"] = kwargs.get("variant", "persistent")
    Drawer.content.attrs["anchor"] = kwargs.get("anchor", "left")
    state = kwargs.get("state", True)
    if isinstance(state ,str):
      Drawer.content.attrs["open"] = {
        "type": "dynamic",
        "content": {
          "referenceType": "state",
          "id": state
        }    
      }
    elif isinstance(state, bool):
      Drawer.content.attrs["open"] = state
      
    List = TeleportElement(MaterialContent(elementType="List"))
    ListItem = TeleportElement(MaterialContent(elementType="ListItem"))
    ListItem.content.attrs["button"] = True
    if "onClickClose" in kwargs:
      ListItem.content.events["click"] = kwargs.get("onClickClose", [])
    
    ListItemIcon = TeleportElement(MaterialContent(elementType="ListItemIcon"))
    InboxIcon = TeleportElement(MaterialContent(elementType="Icon"))
    InboxIconText = TeleportStatic(content="chevron_" + kwargs.get("anchor", "left"))
    InboxIcon.addContent(InboxIconText)    
    ListItemText = TeleportElement(MaterialContent(elementType="ListItemText"))
    ListItemText.content.attrs["primary"] = ""
    Divider = TeleportElement(MaterialContent(elementType="Divider"))
    ListItemIcon.addContent(InboxIcon)
    ListItem.addContent(ListItemIcon)
    #ListItem.addContent(ListItemText)
    List.addContent(ListItem)
    Drawer.addContent(List)

    Drawer.addContent(Divider)
        
    return Drawer

  def Button(*args, **kwargs):
    """This function creates a Material Element of type button.
    Kwargs:
    title (string): title of the button
    size (string) : 
    variant (string): 
    
    Returns:
      TeleportElement

    Raises:
       AttributeError

    >>> 

    """  
    Grid = TeleportElement(MaterialContent(elementType="Grid"))
    Grid.content.attrs["item"] = True
    #Grid.content.attrs["alignContent"] = "center"
    Button = TeleportElement(MaterialContent(elementType="Fab"))
    Button.content.attrs["size"] = kwargs.get("size", "medium")
    Button.content.attrs["variant"] = kwargs.get("variant", "extended")
    Button.content.attrs["color"] = kwargs.get("color", "primary")
    Button.content.attrs["disableRipple"] = kwargs.get("disableRipple", False)
    if ("style" in kwargs):
      Button.content.attrs["className"] = kwargs.get("style")
      
    if kwargs.get("onClickButton", None) is not None:
      Button.content.events["click"] = kwargs.get("onClickButton")

    Button.addContent(TeleportStatic(content=kwargs.get("title", "")))
    Grid.addContent(Button)
    return Grid
  
  def ThemeProvider(theme_var):      
    ThemeProvider = TeleportElement(MaterialContent(elementType="ThemeProvider"))
    ThemeProvider.content.attrs["theme"] = {
      "type": "dynamic",
      "content": {
        "referenceType": "local",
        "id": theme_var
      }
    }
    return ThemeProvider
    
class PlotlyContent(TeleportContent):
  def buildElementType(self):   
    elementType = self.elementType
    return "" + elementType

    
class PlotlyBuilder():
  def BasePlotlyComponent(*args, **kwargs):
    BasePlotlyComponent = TeleportComponent("BasePlotlyComponent", TeleportElement(TeleportContent(elementType="container")))
    BasePlotlyComponent.addStateVariable("data", {"type":"array", "defaultValue": [{'x': [], 'y': []}]})
    PlotlyPlot = TeleportElement(PlotlyContent(elementType="Plot"))
    PlotlyPlot.content.attrs["data"] = {
      "type": "dynamic",
      "content": {
        "referenceType": "state",
        "id": "data"
      }    
    }
    PlotlyPlot.content.attrs["useResizeHandler"] = True
    PlotlyPlot.content.style = {
      "height": "100vh",
    }
    BasePlotlyComponent.node.content.style = {
      "height": "100vh"
    }
    
    BasePlotlyComponent.addNode(PlotlyPlot)
    return BasePlotlyComponent    
    
  def BasePlot(tp, *args, **kwargs):
    if ("BasePlotlyComponent" not in tp.components):
      tp.components["BasePlotlyComponent"] = PlotlyBuilder.BasePlotlyComponent()  
      
    ContainerPlot = TeleportElement(TeleportContent(elementType="container"))
    ContainerPlot.content.style = {
      "height": "100vh"
    }
        
    BasePlot = TeleportElement(TeleportContent(elementType="BasePlotlyComponent"))
    if kwargs.get("data", None) is not None:
      BasePlot.content.attrs["data"] = kwargs.get("data", None)

    if kwargs.get("ref", None) is not None:
      BasePlot.content.attrs["ref"] = kwargs.get("ref", None)
      
    if kwargs.get("style_state", None) is not None:
      ContainerPlot.content.attrs["className"] = {
        "type": "dynamic",
        "content": {
          "referenceType": "state",
          "id": kwargs.get("style_state")
        }    
      }
    
    ContainerPlot.addContent(BasePlot)
    return ContainerPlot

class NanohubUtils():
  def validateCredentials(tp, *args, **kwargs):
    url = kwargs.get("url", "")
    method_name = kwargs.get("method_name", "validateCredentials")
    client_id = kwargs.get("client_id", "")
    client_secret = kwargs.get("client_secret", "")
    user = kwargs.get("user", "")
    pwd = kwargs.get("pwd", "")
    url = kwargs.get("url", "")
    js = ""
    js += "function " + method_name + "(user, pwd){"
    js += "  var data = '';"
    js += "  data = 'client_id="+client_id+"&';"
    js += "  data += 'client_secret="+client_secret+"&';"
    js += "  data += 'grant_type=password&';"
    js += "  data += 'username=' + user + '&';"
    js += "  data += 'password=' + pwd + '&';"
    js += "  var header_token = { 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*' };"
    js += "  var options = { 'handleAs' : 'json' , 'headers' : header_token, 'method' : 'POST', 'data' : data };"
    js += "  var url = '" + url + "';"
    js += "  let self = this;"
    js += "  Axios.request(url, options)"
    js += "  .then(function(response){"
    js += "    var data = response.data;"
    js += "    window.sessionStorage.setItem('nanohub_token', data.token);"
    js += "    window.sessionStorage.setItem('nanohub_refresh_token', data.refresh_token);"
    js += "  }).catch(function(error){"
    js += "    console.log(error.response);"
    js += "  })"
    js += "}"
    
    tp.globals.assets.append({
      "type": "script",
      "content": js
    })
    
    return [
      {
        "type": "propCall",
        "calls": method_name,
        "args": ['\'' + user + '\'', '\''+ pwd +'\'']
      }
    ]

  def refreshToken(tp, *args, **kwargs):
    url = kwargs.get("url", "")
    method_name = kwargs.get("method_name", "refreshToken")
    client_id = kwargs.get("client_id", "")
    client_secret = kwargs.get("client_secret", "")
    user = kwargs.get("user", "")
    pwd = kwargs.get("pwd", "")
    url = kwargs.get("url", "")
    token = kwargs.get("token", "window.sessionStorage.getItem('nanohub_token')")
    js = ""
    js += "function " + method_name + "(token){"
    js += "  var data = '';"
    js += "  data = 'client_id="+client_id+"&';"
    js += "  data += 'client_secret="+client_secret+"&';"
    js += "  data += 'grant_type=refresh_token&';"
    js += "  data += 'refresh_token=' + token + '&';"
    js += "  var header_token = { 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*' };"
    js += "  var options = { 'handleAs' : 'json' , 'headers' : header_token, 'method' : 'POST', 'data' : data };"
    js += "  var url = '" + url + "';"
    js += "  let self = this;"
    js += "  Axios.request(url, options)"
    js += "  .then(function(response){"
    js += "    var data = response.data;"
    js += "    window.sessionStorage.setItem('nanohub_token', data.token);"
    js += "    window.sessionStorage.setItem('nanohub_refresh_token', data.refresh_token);"
    js += "  })"
    js += "}"
    
    tp.globals.assets.append({
      "type": "script",
      "content": js
    })
    
    return [
      {
        "type": "propCall",
        "calls": method_name,
        "args": [token]
      }
    ]    