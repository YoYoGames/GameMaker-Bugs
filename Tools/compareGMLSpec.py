
# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET
import requests
import json
import argparse


def loadManualInfo( _base ):
    headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KMD, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0'}
    url = _base + "/whxdata/idata1.new.js"
    jsFileResponse = requests.get(url, headers=headers)
    jsFile = jsFileResponse.text

    #strip off the various bits from the file (the JS bits that are not JSON)
    indexFirstOpen = jsFile.find( '{' )
    indexSecondOpen = jsFile.find( '{', indexFirstOpen+1 )
    jsFileOriginal = jsFile
    jsFile = jsFile[ indexSecondOpen: ]
    indexLastSemiColon = jsFile.rfind( ';' )
    indexSecondLastSemiColon = jsFile.rfind( ';', 0, indexLastSemiColon )
    indexThirdLastSemiColon = jsFile.rfind( ';', 0, indexSecondLastSemiColon )
    jsFile = jsFile[0:indexThirdLastSemiColon]

    manualInfo = json.loads(jsFile)
    return manualInfo


def searchForManualURL( _json, _search):
    foundExact = None
    foundCandidates = []
    for k in manualInfo[ "keys"]:
        if k[ "name"] == _search:
            foundExact = k
        elif _search in k["name"]:
            foundCandidates.append( k )
    if foundExact is None:
        return ""
    else:
        return "https://manual.gamemaker.io/monthly/en/#t=" + foundExact[ "topics" ][0]["url"]


def loadGmlSpec( _fileLoc ):
    # Passing the path of the
    # xml document to enable the
    # parsing process
    tree = ET.parse(_fileLoc)

    # getting the parent tag of
    # the xml document
    root = tree.getroot()


    # Get all the functions
    functions = tree.findall( "Functions/Function" );
    gmlFuncs = []
    for f in functions:
        gmlF = {
            "params" : []
        }
        gmlFuncs.append( gmlF )
        if (f.find( "Description") is None):
            description = ""
        else:
            description = f.find( "Description").text
        gmlF[ "returns" ] = f.get( "ReturnType" )
        gmlF["description"] = description;
        gmlF[ "pure" ] = f.get( "Pure" )
        gmlF[ "name" ] = f.get( "Name" )
        gmlF[ "deprecated" ] = f.get( "Deprecated")
        gmlF[ "featureFlag" ] = f.get( "FeatureFlag") or "none"
        params = f.findall( "Parameter" )
        for p in params:
            gmlP = {}
            gmlP[ "name" ] = p.get( "Name" ) or "unknown"
            gmlP[ "type" ] = p.get( "Type" ) or "None"
            gmlP[ "optional" ] = p.get( "Optional" ) or "false"
            gmlP[ "text" ] = p.text or ""
            gmlF[ "params" ].append(gmlP)


    # Get all the variables
    variables = tree.findall( "Variables/Variable" );
    gmlVars = []
    for v in variables:
        gmlV = {}
        gmlVars.append( gmlV )
        gmlV[ "name" ] = v.get( "Name" ) or "unknown"
        gmlV[ "deprecated" ] = v.get( "Deprecated")
        gmlV[ "type" ] = v.get( "Type" )
        gmlV[ "get" ] = v.get( "Get" )
        gmlV[ "set" ] = v.get( "Set" )
        gmlV[ "instance" ] = v.get( "Instance" )
        gmlV[ "text" ] = v.text or ""
        gmlV[ "featureFlag" ] = v.get( "FeatureFlag" ) or "none"

    # Get all the constants
    constants = tree.findall( "Constants/Constant" );
    gmlConsts = []
    for c in constants:
        gmlC = {}
        gmlConsts.append( gmlC )
        gmlC[ "name" ] = c.get( "Name" ) or "unknown"
        gmlC[ "deprecated" ] = c.get( "Deprecated")
        gmlC[ "type" ] = c.get( "Type" )
        gmlC[ "class" ] = c.get( "Class" )
        gmlC[ "text" ] = c.text or ""
        gmlC[ "featureFlag" ] = c.get( "FeatureFlag" ) or "none"

    # Get all the structures
    structures = tree.findall( "Structures/Structure" );
    gmlStructs = []
    for s in structures:
        gmlS = { "fields" : [] }
        gmlStructs.append( gmlS )
        gmlS[ "name" ] = s.get( "Name" ) or "unknown"
        gmlS[ "featureFlag" ] = s.get( "FeatureFlag" ) or "none"
        fields = s.findall( "Field" )
        for f in fields:
            gmlF = {}
            gmlS[ "fields" ].append(gmlF)
            gmlF[ "name" ] = f.get( "Name" ) or "unknown"
            gmlF[ "type" ] = f.get( "Type" ) or "None"
            gmlF[ "get" ] = f.get( "Get" ) or "false"
            gmlF[ "set" ] = f.get( "Set" ) or "false"
            gmlF[ "text" ] = f.text or ""

    # Get all the enumerations
    enums = tree.findall( "Enumerations/Enumeration" );
    gmlEnums = []
    for e in enums:
        gmlE = { "members" : [] } 
        gmlEnums.append( gmlE )
        gmlE[ "name" ] = e.get( "Name" ) or "unknown"
        gmlE[ "featureFlag" ] = e.get( "FeatureFlag" ) or "none"
        members = e.findall( "Member" )
        for m in members:
            gmlM = {}
            gmlE[ "members"].append( gmlM )
            gmlM[ "name" ] = m.get( "Name" ) or "unknown"
            gmlM[ "deprecated" ] = m.get( "Deprecated") or "false"
            gmlM[ "value" ] = m.get( "Value" ) or "None"
            gmlM[ "text" ] = m.text or ""

    return { "functions" : gmlFuncs, "variables" : gmlVars, "constants" : gmlConsts, "structs" : gmlStructs, "enums" : gmlEnums  }


def isEqualGmlFunctions( _new, _old ):
    ret = True;
    if (len(_new["params"]) != len(_old["params"]) ):
        ret = False
    return ret

def isEqualGmlVariable( _new, _old ):
    ret = True;
    return ret

def isEqualGmlConstants( _new, _old ):
    ret = True;
    return ret

def isEqualGmlStructs( _new, _old ):
    ret = True;
    if (len(_new["fields"]) != len(_old["fields"]) ):
        ret = False
    return ret

def isEqualGmlEnums( _new, _old ):
    ret = True;
    if (len(_new["members"]) != len(_old["members"]) ):
        ret = False
    return ret

def compareOldAndNew( old, new, isEqualFunc ):
    newFuncs = []
    deletedFuncs = []
    changedFuncs = []
    for f in new:
        found = False;
        foundFunc = None;
        for fO in old:
            if (f["name"] == fO["name"]):
                found = True
                foundFunc = fO     # we need to delete these later
                if (not isEqualFunc(f, fO)):
                    f["previous"] = fO
                    changedFuncs.append( f )
                break;

        if not found:
            if not ("featureFlag" in f) or f["featureFlag"] == "none":
                newFuncs.append( f )
        else: 
            old.remove( foundFunc )
    deletedFuncs = old
    return { "new" : newFuncs, "deleted" : deletedFuncs, "changed" : changedFuncs }


def printChanges( changes, prefix ):
    print( prefix + " NEW - ##########################################################################################")
    for f in changes["new"]:
        print( f["name"] )
    print( prefix + " DELETED - ######################################################################################")
    for f in changes["deleted"]:
        print( f["name"] )
    print( prefix + "CHANGED - #######################################################################################")
    for f in changes["changed"]:
        print( f["name"] )


def mdChanges( changes, sectionName, outputFunc, deletedFunc=None, changedFunc=None  ):
    if (len(changes["new"]) > 0):
        print( "## Misc New " + sectionName)
        print( "")
        for f in changes["new"]:
            print( outputFunc(f)  )
        print( "")
    if (len(changes["deleted"]) > 0):
        print( "## Misc Deleted " + sectionName )
        print( "")
        for f in changes["deleted"]:
            if deletedFunc == None:
                print( outputFunc(f) )
            else:
                print( deletedFunc(f) )
        print( "")
    if (len(changes["changed"]) > 0):
        print( "## Misc Changed " + sectionName)
        print( "")
        for f in changes["changed"]:
            if changedFunc == None:
                print( outputFunc(f) )
            else:
                print( changedFunc(f) + "" )
        print( "")

def getParams( func ):
    params = "("
    count = 0
    for p in func[ "params" ]:
        if (count > 0):
            params += ","
        if (p["optional"] == "true"):
            params+="["
        params+=p[ "name" ]
        if (p["optional"] == "true"):
            params+="]"
        count+=1
    params += ")"
    return params

def outputMDFunctions( func ):
    return "- " + outputMDFunctionsNoDesc(func) + " - " + func["description"]

def outputMDFunctionsNoDesc( func ):
    return "`" + func["name"] + getParams(func) + "`"

def outputMDFunctionsChanged( func ):
    return outputMDFunctionsNoDesc(func["previous"]) + " changed to `" + func["name"] + getParams(func) + "`"

def outputMDVariables( func ):
    return "- `" + func["name"] + "` - " + func["text"]

def outputMDConstants( func ):
    return "- `" + func["name"] + "` - " + func["text"]

def outputMDStructs( func ):
    params = " {\n"
    count = 0
    for p in func[ "fields" ]:
        if (count > 0):
            params += ",\n"
        params+=p[ "name" ]
        params+=" : "+p["text"] 
        count+=1
    params += "\n}\n"
    return "```\n" + func["name"] + params + "```"

def outputMDStructsChanged( func ):
    params = " {\n"
    count = 0
    original = func["previous"]
    for p in func[ "fields" ]:

        found = False
        for pp in original[ "fields" ]:
            if p["name"] == pp["name"]:
                found = True
                break

        if (count > 0):
            params += ",\n"
        if not found:
            params+="/* new */ "
        else:
            params+="/* ___ */  "
        params+=p[ "name" ]
        params+=" : "+p["text"] 
        count+=1
    params += "\n}\n"
    return "```\n" + func["name"] + params + "```"


def outputMDEnums( func ):
    params = "{\n"
    count = 0
    for p in func[ "members" ]:
        if (count > 0):
            params += ",\n"
        params+=p[ "name" ]
        params+="="+p["value"]
        count+=1
    params += "\n}\n"
    return "```\n" + func["name"] + params + "```"

def outputMDEnumsChanged( func ):
    params = " {\n"
    count = 0
    original = func["previous"]
    for p in func[ "members" ]:

        found = False
        for pp in original[ "members" ]:
            if p["name"] == pp["name"]:
                found = True
                break

        if (count > 0):
            params += ",\n"
        if not found:
            params+="/* new */ "
        else:
            params+="/* ___ */  "
        params+=p[ "name" ]
        params+="="+p["value"]
        count+=1
    params += "\n}\n"
    return "```\n" + func["name"] + params + "```"

# -------------------------------------------------------------------------------------------------------
# load the new and old gmlSpec
parser = argparse.ArgumentParser("compareGmlSpec", description="compare 2 GMLSpec.xml and output MD with the added, deleted and changed elements")
parser.add_argument( 'new', help='full path to the new GmlSpec.xml to use for comparison')
parser.add_argument( 'old', help='full path to the old GmlSpec.xml to use for comparison')
args = parser.parse_args()


gmlSpecNew = loadGmlSpec(args.new)
gmlSpecOld = loadGmlSpec(args.old)



# -------------------------------------------------------------------------------------------------------
funcChanges = compareOldAndNew( gmlSpecOld["functions"], gmlSpecNew["functions"], isEqualGmlFunctions )
# -------------------------------------------------------------------------------------------------------
varChanges = compareOldAndNew( gmlSpecOld["variables"], gmlSpecNew["variables"], isEqualGmlVariable )
# -------------------------------------------------------------------------------------------------------
constChanges = compareOldAndNew( gmlSpecOld["constants"], gmlSpecNew["constants"], isEqualGmlConstants )
# -------------------------------------------------------------------------------------------------------
structChanges = compareOldAndNew( gmlSpecOld["structs"], gmlSpecNew["structs"], isEqualGmlStructs )
# -------------------------------------------------------------------------------------------------------
enumChanges = compareOldAndNew( gmlSpecOld["enums"], gmlSpecNew["enums"], isEqualGmlEnums )

mdChanges( funcChanges,  "Functions", outputMDFunctions, outputMDFunctionsNoDesc, outputMDFunctionsChanged )
mdChanges( varChanges,  "Variables", outputMDVariables )
mdChanges( constChanges,  "Constants", outputMDConstants )
mdChanges( structChanges,  "Structs", outputMDStructs, outputMDStructs, outputMDStructsChanged )
mdChanges( enumChanges,  "Enums", outputMDEnums, outputMDEnums, outputMDEnumsChanged )


# download the manual info
# manualInfo = loadManualInfo("https://manual.gamemaker.io/monthly/en")
