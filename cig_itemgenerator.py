# Custom Item Generator (for Datapack) by UltroGhast
import os
import json
import webbrowser
while True:
    # Generating Files
    def generate_recipefiles(ns,baseitem,nbt,crafting,count):
        global player_namespace
        global dp_namespace
        global refdp_path
        global functions_path
        recipes_path = functions_path.replace("/functions/","/recipes/")
        advancements_path = functions_path.replace("/functions/","/advancements/")
        with open(f"{recipes_path}{ns}.json","w") as openedfile: openedfile.write(json.dumps(crafting,indent=5,sort_keys=True))
        with open(f"{advancements_path}craft_{ns}.json","w") as openedfile: openedfile.write(json.dumps({"rewards":{"function":f"{refdp_path}craft_{ns}"},"criteria":{"ulg_requirement":{"trigger":"minecraft:recipe_unlocked","conditions":{"recipe":f"{refdp_path}{ns}"}}}},indent=5,sort_keys=True))
        with open(f"{functions_path}craft_{ns}.mcfunction","w") as openedfile: openedfile.write(f"give @s minecraft:{baseitem}{nbt} {str(count)}\nadvancement revoke @s only {refdp_path}craft_{ns}\nrecipe take @s {refdp_path}{ns}\nclear @s minecraft:knowledge_book {str(count)}\n#generated with Custom Item Generator for Datapacks by UltroGhast")
    def creating_newrecipe(ns=None,baseitem=None,nbt=None):
        while True:
            choose_recipetype = input(f"\nWhat type of crafting do you want as crafting for the item '{ns}'?\nShapeless - without a specific shape, only ingredients\nShaped - the items needs to be positioned in a specific way\n(Shapeless/Shaped) >>> ").lower()
            if choose_recipetype == "shapeless":
                recipe = {"type":"minecraft:crafting_shapeless","ingredients":[],"result":{"item":"minecraft:knowledge_book","count":1}}
                print("\nOk, now set the ingredients(9 max), you can't set nbt of the ingredients\n")
                while True:
                    newingredient = input("New ingredient: ").lower().replace("minecraft:","").replace(" ","_")
                    if len(newingredient) > 3:
                        recipe["ingredients"].append({"item":f"minecraft:{newingredient}"})
                        print(f"Added '{newingredient}' as ingredient")
                    else:
                        print("\nInvalid Entry, remember to use the id of the items you want as ingredients\n")
                        continue
                    if len(recipe["ingredients"]) > 8:
                        break
                    else:
                        pass
            elif choose_recipetype == "shaped":
                while True:
                    recipe = {"type":"minecraft:crafting_shaped","pattern":[],"key":{},"result":{"item":"minecraft:knowledge_book","count":1}}
                    print("\nOk, now set the pattern(it can be 2x1,1x2,1x3,3x1,2x2,2x3,3x2,3x3)\n")
                    choose_patterntype = input("(2x1,1x2,1x3,3x1,2x2,2x3,3x2,3x3) >>> ")
                    if choose_patterntype in ["2x1","1x2","1x3","3x1","2x2","2x3","3x2","3x3"]:
                        choose_patterntype = choose_patterntype.split("x")
                        choose_patterntype[0] = int(choose_patterntype[0])
                        choose_patterntype[1] = int(choose_patterntype[1])
                        patternexample = ""
                        for num in range(choose_patterntype[1]):
                            if num == 0: patternexample += "First Line:  "
                            if num == 1: patternexample += "Second Line: "
                            if num == 2: patternexample += "Third Line:  "
                            for num1 in range(choose_patterntype[0]):
                                patternexample += "#"
                            patternexample += "\n"
                        recipekeys = []
                        print("\nNow set the pattern of the crafting, it should be like that:\n"+patternexample+"\n")
                        for num in range(choose_patterntype[1]):
                            if num == 0: print("Set the first line:  ",end='')
                            if num == 1: print("Set the second line: ",end='')
                            if num == 2: print("Set the third line:  ",end='')
                            recipeline = input("")
                            if len(recipeline) == choose_patterntype[0]:
                                recipe["pattern"].append(recipeline)
                                for c in recipeline:
                                    if (not c in recipekeys) and (not c == " "): recipekeys.append(c)
                            else:
                                print("\nInvalid Entry, start again!")
                                break
                                continue
                        for i in recipekeys:
                            key_matchid = input(f"What item does the key '{i}' indicate? >>> ").lower().replace(" ","_").replace("minecraft:","")
                            if len(key_matchid) > 3:
                                recipe["key"][i] = {"item":f"minecraft:{key_matchid}"}
                    else:
                        print("It seems you didn't give a valid value, the generator will start again")
                        continue
                    break
            else:
                print("\nInvalid Entry, try again")
                continue
            result_count = input(f"\nThe result of the crafting will be this item:{baseitem}{nbt}.\nNow choose the count(number): ")
            try:
                result_count = int(result_count)
                recipe["result"]["count"] = result_count
            except:
                result_count = 1
                pass
            generate_recipefiles(ns,baseitem,nbt,recipe,str(result_count))
            break
            
    def generate_itemfiles(ns,baseitem,custom_model_data,nbt,model_display):
        global player_namespace
        global dp_namespace
        global followconventions
        global rp_path
        global functions_path
        global refdp_path
        #set model predicates(Custom Model Data)
        if os.path.isfile(f"{rp_path}/assets/minecraft/models/item/{baseitem}.json") == False:
            openedfile = open(f"{rp_path}/assets/minecraft/models/item/{baseitem}.json","w")
            openedfile.write(json.dumps({"parent": f"minecraft:item/{model_display}","textures": {"layer0": f"minecraft:item/{baseitem}"},"overrides":[{"predicate": {"custom_model_data":custom_model_data}, "model": f"{refdp_path}{ns}"}]}, indent=5, sort_keys=True))
            openedfile.close()
        else:
            openedfile = open(f"{rp_path}/assets/minecraft/models/item/{baseitem}.json","r")
            filecontent = json.loads(openedfile.read())
            filecontent["overrides"].append({"predicate": {"custom_model_data":custom_model_data}, "model": f"{refdp_path}{ns}"})
            filecontent["overrides"] = sorted(filecontent["overrides"], key=lambda k: k['predicate']['custom_model_data']) 
            openedfile = open(f"{rp_path}/assets/minecraft/models/item/{baseitem}.json","w")
            openedfile.write(json.dumps(filecontent,indent=5,sort_keys=True))
            openedfile.close()
        #set models and placeholder for textures
        if model_display == "block":
            refdp_path_block = refdp_path.replace("/customitem/","/customblock/")
            with open(f"{rp_path}/assets/{player_namespace}/models/{dp_namespace}/customitem/{ns}.json","w") as openedfile:
                openedfile.write(json.dumps({"comment":"Created with Custom Item Generator for Datapacks (by UltroGhast) sites.google.com/view/ultroghasthub/generators","parent":"block/block","textures":{"down":f"{refdp_path_block}{ns}","up":f"{refdp_path_block}{ns}","north":f"{refdp_path_block}{ns}","south":f"{refdp_path_block}{ns}","west":f"{refdp_path_block}{ns}","east":f"{refdp_path_block}{ns}"},"elements":[{"from":[0,0,0],"to":[16,16,16],"faces":{"down":{"texture":"#down","cullface":"down"},"up":{"texture":"#up","cullface":"up"},"north":{"texture":"#north","cullface":"north"},"south":{"texture":"#south","cullface":"south"},"west":{"texture":"#west","cullface":"west"},"east":{"texture":"#east","cullface":"east"}}}]}, indent=5, sort_keys=True))
            if os.path.isfile(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customblock/{ns}.png") == False:
                with open(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customblock/{ns}_placeholder.txt","w") as openedfile:
                    openedfile.write(f"This is a placeholder file! Instead of it, you should place the texture.png of the block and remove this file.\n\n\nCustom Item Generator for Datapacks by UltroGhast")
                webbrowser.open(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customblock/")
        else:
            with open(f"{rp_path}/assets/{player_namespace}/models/{dp_namespace}/customitem/{ns}.json","w") as openedfile:
                openedfile.write(json.dumps({"comment":"Created with Custom Item Generator for Datapacks (by UltroGhast) sites.google.com/view/ultroghasthub/generators","parent":f"minecraft:item/{model_display}","textures":{"layer0":f"{refdp_path}{ns}"}}, indent=5, sort_keys=True))
            if os.path.isfile(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customitem/{ns}.png") == False:
                with open(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customitem/{ns}_placeholder.txt","w") as openedfile:
                    openedfile.write(f"This is a placeholder file! Instead of it, you should place the texture.png of the item and remove this file.\n\n\nCustom Item Generator for Datapacks by UltroGhast")
                webbrowser.open(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customitem/")
        #set special things for special items
        if baseitem.endswith("_on_a_stick"):
            #minecraft.used:minecraft.carrot_on_a_stick
            openedfile = open("data/"+player_namespace+"/functions/"+dp_namespace+"/tick.mcfunction","r")
            filecontent = list(filter(lambda x: x != 2, openedfile.readlines()))
            filecontent.insert(0,f"execute as @a[scores={{{dp_namespace}{ns}=1..}},nbt={{SelectedItem:{{tag:{{{dp_namespace}:{{{ns}:1b}}}}}}}}] at @s run function {refdp_path}used_{ns}")
            filecontent.append(f"scoreboard players reset @a[scores={{{dp_namespace}{ns}=1..}}] {dp_namespace}{ns}")
            filecontent = "\n".join(filecontent)
            openedfile = open("data/"+player_namespace+"/functions/"+dp_namespace+"/tick.mcfunction","w")
            openedfile.write(filecontent)
            openedfile.close()
            openedfile = open("data/"+player_namespace+"/functions/"+dp_namespace+"/load.mcfunction","r")
            filecontent = list(filter(lambda x: x != 2, openedfile.readlines()))
            filecontent.append(f"scoreboard objectives add {dp_namespace}{ns} minecraft.used:minecraft.{baseitem}")
            filecontent = "\n".join(filecontent)
            openedfile = open("data/"+player_namespace+"/functions/"+dp_namespace+"/load.mcfunction","w")
            openedfile.write(filecontent)
            openedfile.close()
            if followconventions == True:
                openedfile = open("data/"+player_namespace+"/functions/"+dp_namespace+"/uninstall.mcfunction","r")
                filecontent = list(filter(lambda x: x != 2, openedfile.readlines()))
                filecontent.append(f"scoreboard objectives remove {dp_namespace}{ns}")
                filecontent = "\n".join(filecontent)
                openedfile = open("data/"+player_namespace+"/functions/"+dp_namespace+"/uninstall.mcfunction","w")
                openedfile.write(filecontent)
                openedfile.close()
            if os.path.isfile("data/"+player_namespace+"/functions/"+dp_namespace+f"/customitem/used_{ns}.mcfunction") == False:
                with open("data/"+player_namespace+"/functions/"+dp_namespace+f"/customitem/used_{ns}.mcfunction","w") as openedfile:
                    openedfile.write("#When you use the custom item, it executes these commands\n\n\n\n\n\n\n\n\n\n\n\n\n\n#Custom Item Generator for Datapacks by UltroGhast")
            print(f"\n\nWhen somebody will use the Custom Item, the player will execute the function {refdp_path}used_{ns}\n")
        if baseitem.endswith("_helmet"):
            choose_ifcustomhat = input("\nThe base item is an helmet, do you want to create a custom hat with a custom model? (Yes/No) >>> ").lower()
            if choose_ifcustomhat == "yes":
                print("\nAt the moment this feature is not available. Wait for the next version of the Item Generator (check it here: https://sites.google.com/view/ultroghasthub/generators/customitem_generator)")
            else:
                pass
        print("\nAll files succesfully generated! Remember to set the textures!")
        print(f'/give @p minecraft:{baseitem}{nbt} 1\n/summon minecraft:item ~ ~ ~ {{Item:{{id:"minecraft:{baseitem}",Count:1b,tag:{nbt}}}}}\n\n')
        creating_newrecipe(ns,baseitem,nbt)
    # Getting Dates
    def creating_newitem():
        global player_name
        global player_namespace
        global dp_namespace
        global custom_model_id
        global followconventions
        global rp_path
        while 1 == 1:
            print("Ok, {player}, let's create a new item! Type 'reset' in any input to reset item dates\n".format(player=player_name))
            #BASE ITEM
            choose_itemtype = input("What type of item do you need?\n'Useless Item' (do not do anything)\n'Placeable Item' (places an invisible item frame)\n'Usable' (do things when right click with it)\n'Hat' (wearable as hat)\n'Custom' (totally custom)\n>>> ").lower()
            if choose_itemtype == "useless item":
                item_id = "stick"
            elif choose_itemtype == "placeable item":
                item_id = "item_frame"
            elif choose_itemtype == "usable":
                item_id = "carrot_on_a_stick"
            elif choose_itemtype == "hat":
                item_id = "chainmail_helmet"
            elif choose_itemtype == "custom":
                item_id = input("\nType the Item ID (minecraft:apple, minecraft:diamond_sword etc.)\n>>> ").lower()
                if item_id.startswith("minecraft:"):
                    item_id = item_id.replace("minecraft:","")
                elif ":" in item_id:
                    print("\nIt seems you are using a by-mod item as base item. At the moment, this generator does not support by-mod items\nThe creation of the item session will restart.\n\n\n")
                    continue
                elif item_id == "reset":
                    break
                    continue
                else:
                    pass
            elif choose_itemtype == "reset":
                    break
                    continue
            else:
                continue
            #CUSTOM MODEL DATA
            print("\nNow choose the Custom Model Data you want to apply on the item",end='')
            if not custom_model_id == None:
                print(",remember the Custom Model Data should be like {cmdi}0000, you should use your ID in the right way to respect conventions!\n".format(cmdi=custom_model_id))
            else:
                print("\n")
                pass
            try:
                choose_cmd = int(input('Type here the Custom Model Data >>> '))
                if choose_cmd < 0 or choose_cmd > 9999999 and not custom_model_id == None:
                    print("Invalid Entry, the creations session of the item will restart\n")
                    continue
                elif choose_cmd < 0 or choose_cmd > 99999999:
                    print("Invalid Entry(Custom Model Data uses only numbers), the creation session of the item will restart\n")
                    continue
                else:
                    pass
            except:
                print("Invalid Entry(Custom Model Data uses only numbers), the creation session of the item will restart\n")
                continue
            #MODEL DISPLAY for BLOCKS
            model_display = None
            if item_id.endswith("spawn_egg") or item_id in ['item_frame','armor_stand']:
                choose_model_display = input("\nItems are displayed in the player gui, on the hands, on the head, on ground and on item frames. But not all in the same way. It depends on the display part of the model.\nYour item is a placeable block/entity. Should it have the default item model(generated) or should does it use the block model(block)?\nWhich one do you want to use? (generated/block) >>> ")
                if choose_model_display == "generated":
                    model_display = "generated"
                elif choose_model_display == "block":
                    model_display = "block"
                else:
                    print("Invalid Input, generated display model will be used")
            else:
                pass
            ### ITEM NBT PART ###
            item_nbt = {"display":{"Lore":[]}}
            #ITEM NAME
            item_name = input("\nNow write the Name the item will have: ")
            if len(item_name) == 0:
                print("Invalid Entry, the generator will restart")
                break
                continue
            else:
                pass
            item_namecolor = input("Choose the color of the name:\nblack, dark_blue, dark_green, dark_aqua, dark_red, dark_purple, gold\ndark_gray, gray, blue, green, aqua, red, light_purple, yellow, white\nYou can insert any color in the hexadecimal color format(#<hex>)\nYou can also type 'default' to set the default color of item names(white)\n>>> ").lower()
            if item_namecolor == "reset":
                continue
            elif item_namecolor == "default":
                item_namecolor = "reset"
            elif not len(item_namecolor) == 0:
                pass
            else:
                continue
            item_ctcid = item_name.lower().replace(" ","_").replace("ò","o").replace("è","e").replace("à","a").replace("ì","i").replace("ù","u")
            if item_name == "reset":
                continue
            item_nbt["display"]["Name"] = "{\"text\":\""+item_name+"\",\"italic\":false,\"color\":\""+item_namecolor+"\"}"
            #ITEM DESCRIPTION
            item_description = input("\nWrite the item description(type 'custom' to set a custom json text or don't write anything if you don't want to set a description) then press [ENTER] >>> ")
            if not (item_description == "custom" or len(item_description)==0):
                choose_desccolor = input("Choose the color of the description:\nblack, dark_blue, dark_green, dark_aqua, dark_red, dark_purple, gold\ndark_gray, gray, blue, green, aqua, red, light_purple, yellow, white\nYou can also insert any color in the hexadecimal color format(#<hex>)\n>>> ").lower()
                if choose_desccolor == "reset":
                    continue
                else:
                    pass
                choose_descitalic = input("Will the item description be in italic? (Yes/No): ")
                if choose_descitalic.lower() == "yes":
                    choose_descitalic = "true"
                elif choose_descitalic.lower() == "no":
                    choose_descitalic = "false"
                else:
                    print("Invalid Entry(available only Yes/No), the creation session of the item will restart\n")
                    continue
                item_nbt["display"]["Lore"].append('{"text":"'+item_description+'","color":"'+choose_desccolor+'","italic":'+choose_descitalic+'}')
            elif item_description == "custom":
                item_nbt["display"]["Lore"].append(input("Paste here the json text you want to use as item description: "))
            else:
                no_description = True
                pass
            if item_nbt["display"]["Lore"] == []:
                del item_nbt["display"]["Lore"]
            else:
                pass
            #COMMON TRAITS CONVENTION
            if followconventions == True:
                ctc = {"id":"","from":"","traits":{}}
                ctc["from"] = player_namespace+":"+dp_namespace
                ctc["id"] = item_ctcid
                print("\nSince your datapack follows conventions, write here the traits of the item(for the Common Traits Convention): ")
                if not item_id == "item_frame":
                    ctc["traits"]["item"] = True
                else:
                    ctc["traits"]["block"] = True
                if item_id == "chainmail_helmet":
                    ctc["traits"]["hat"] = True
                if item_id == "carrot_on_a_stick":
                    ctc["traits"]["tool"] = True
                while True:
                    newctc = input("Type the trait, then press [ENTER] to confirm it and write another.\nType 'finished' when you have finished putting traits.\n>>> ").lower().replace(" ","").replace(":1b","").replace(":true","")
                    if newctc == "finished":
                        break
                    elif newctc == "reset":
                        break
                        continue
                    elif not len(newctc) == 0 :
                        ctc["traits"][newctc] = True
                    else:
                        print("Invalid Entry, try again\n")
                        continue
            #CUSTOM NBT TAGS
            print("\nNow it's time to set all nbt tags which will be stored inside tag:{...}\nType the nbt tag, then press [ENTER] to confirm it and write another. Type 'finished' when you have finished putting nbt tags.")
            if item_id == "item_frame":
                print("Since your item is placeable(item frame as base item) you should also add an EntityTag nbt!\n")
            item_more_nbt = []
            item_more_nbt.append("CustomModelData:"+str(choose_cmd))
            item_more_nbt.append(dp_namespace+":{"+item_ctcid+":1b}")
            while True:
                newnbt = input("Write/Paste the nbt tag: ")
                if not (newnbt.startswith("{") or newnbt.startswith("display:") or newnbt.startswith("tag:") or newnbt.startswith("CustomModelData:") or newnbt == "reset" or newnbt == "finished" or len(newnbt) == 0 or ":" not in newnbt):
                    item_more_nbt.append(newnbt)
                    print("Added NBT tag: '"+newnbt+"'")
                elif newnbt == "reset":
                    break
                    continue
                elif newnbt == "finished":
                    break
                else:
                    print("Invalid Entry(written tags will be stored in the nbt tag:{}, and you can't insert display/CustomModelData tags), try again\n")
                    continue
            if followconventions == True:
                item_nbt = "{ctc:"+str(ctc)+",display:"+str(item_nbt["display"])
                for i in item_more_nbt:
                    item_nbt += ","+i
                item_nbt += "}"
            else:
                item_nbt = "{display:"+str(item_nbt["display"])
                for i in item_more_nbt:
                    item_nbt += ","+i
                item_nbt += "}"
            #MODEL DISPLAY ULTIMATE PART
            if model_display == None:
                if item_id.endswith("on_a_stick"):
                    model_display = "hendheld_rod"
                elif item_id.endswith("_sword") or item_id.endswith("_shovel") or item_id.endswith("_pickaxe") or item_id.endswith("_axe") or item_id.endswith("hoe"):
                    model_display = "hendheld"
                else:
                    model_display = "generated"
            #END
            while True:
                print("\nI got the dates I needed! It's time to generate. Here the dates of the custom item...\nItem Name: "+item_name+"\nBase Item: "+item_id+"\nCustom Model Data: "+str(choose_cmd)+"\n\/Entire Item NBT\/\n"+item_nbt+"\nModel Display: "+model_display)
                ultimate_decision = input("\n\nDo you want to generate a custom item with these dates?\n(Yes/No/Reset) >>> ").lower()
                if ultimate_decision == "yes":
                    generate_itemfiles(item_ctcid,item_id,choose_cmd,item_nbt,model_display)
                    break
                    break
                    continue
                elif ultimate_decision in ['no','reset']:
                    break
                    break
                    continue
                else:
                    pass
    # Start Program
    if os.path.isdir('./data') == True:
        if os.path.isfile('./saved_dp_dates.json') == True:
            dpdatesfile = open("saved_dp_dates.json","r")
            dpdates = dpdatesfile.read()
            dpdates = list(json.loads(dpdates))
            print("Hi! Welcome back to the Custom Item generator for Datapacks [V.1] by UltroGhast\n")
            print("Charged previous dates\nCreator Name: "+dpdates[0],"\nCreator namespace: "+dpdates[1],"\nDatapack namespace: "+dpdates[2],"\nFollows Convention: "+str(dpdates[3]),"\nCustom Model Data ID: "+str(dpdates[4]),"\nResources Path: "+dpdates[5],"\nFunctions Path: "+dpdates[6],"\nRef Path: "+dpdates[7])
            player_name = dpdates[0]
            player_namespace = dpdates[1]
            dp_namespace = dpdates[2]
            followconventions = dpdates[3]
            custom_model_id = dpdates[4]
            rp_path = dpdates[5]
            functions_path = dpdates[6]
            refdp_path = dpdates[7]
            dpdatesfile.close()
            ulg = input("\nPress [Enter] to create a new item or type 'reset' to reset the dates\n>>>")
            if ulg == "reset":
                print('Registed Dates Removed!\nKilling the program')
                os.remove('./saved_dp_dates.json')
                exit()
            else:
                creating_newitem()
            # INSTALL
        else:
            # Define some functions
            def get_player_namespace():
                global dpdates
                global player_namespace
                player_namespace = str(input("Ok,"+player_name+", now enter your namespace: "))
                if player_namespace == "help":
                    print("What's the creator namespace?\nIt's a really short and lower name to indicate you. For example 'UltroGhast'(me) becomes 'ulg'\nPeople usually use their namespace in their datapack if they want to make the datapack compatible with others and have a good and optimized structure.\n")
                    get_player_namespace()
                if len(player_namespace) == 0:
                    print("Invalid Input, I'll ask it again!\n")
                    get_player_namespace()
                else:
                    player_namespace.replace(" ", "_").lower()
                    print('Creator Namespace Saved > '+player_namespace)
                    dpdates[1] = player_namespace
            def get_dp_namespace():
                global dpdates
                global dp_namespace
                dp_namespace = str(input("Enter the datapack namespace: "))
                if dp_namespace == "help":
                    print("What's the datapack namespace?\nIt's a really short and lower name to indicate the datapack. For example 'Mrs Murble\'s Recipes'(one of my datapacks) becomes 'murblerecipes'\n")
                    get_dp_namespace()
                elif len(dp_namespace) == 0:
                    print("Invalid Input, I'll ask it again!\n")
                    get_dp_namespace()
                else:
                    dp_namespace.replace(" ", "_").lower()
                    print('Datapack Namespace Saved > '+dp_namespace)
                    dpdates[2] = dp_namespace
            def ask_followconventions():
                global dpdates
                global followconventions
                print('Does your datapack follow Official Conventions?(mc-datapacks.github.io/en/conventions/)\nType "Yes" or "No" >>> ')
                followconventions = str(input()).lower()
                if followconventions == "yes":
                    followconventions = True
                elif followconventions == "no":
                    followconventions = False
                    dpdates[4] = None
                    pass
                else:
                    print("Invalid Input, I'll ask it again!\n")
                    ask_followconventions()
                dpdates[3] = followconventions
            def ask_cmd():
                global dpdates
                global custom_model_id
                custom_model_id = input('Since your datapack follows conventions,what\'s your Custom Model Data ID? (Type "None" if you don\'t have one)\n>>> ')
                try:
                    custom_model_id = int(custom_model_id)
                    if custom_model_id > 0 and custom_model_id < 1000:
                        print("Custom Model Data ID succesfully registed: "+str(custom_model_id))
                        dpdates[4] = custom_model_id
                    else:
                        print('Custom Model Data ID uses only numbers! Refresh yourself about it: mc-datapacks.github.io/en/conventions/custom_model_id\n')
                        ask_cmd()
                except ValueError:
                    if custom_model_id.lower() == "none":
                        dpdates[4] = None
                        pass
                    else:
                        print('Custom Model Data ID uses only numbers! Refresh yourself about it: mc-datapacks.github.io/en/conventions/custom_model_id')
                        ask_cmd()
            def get_rppath():
                global dpdates
                global rp_path
                rp_path = os.getcwd()
                rp_path = rp_path.replace("\\", "\\\\").split("\\")
                rp_path = list(filter(lambda x: len(str(x)) > 0,rp_path))
                rp_path.pop(-1)
                rp_path.pop(-1)
                rp_path.pop(-1)
                rp_path.pop(-1)
                rp_path = "\\".join(rp_path)
                rp_path += "\\resourcepacks\\"
                rpp_choose = input("Now I need to know where I should modify the models, please help me to find the Resource Pack Directory\nIf it is in {rppath} type 'name', else type 'path': ".format(rppath=rp_path))
                if rpp_choose.lower() == "name":
                    rp_name = input("What's the name of your resource pack? Paste it here: ")
                    rp_path += rp_name
                    if os.path.isfile(rp_path+'\\pack.mcmeta') == False:
                        print("Sure "+rp_path+" is the Resource Pack path? There appears to be no pack.mcmeta file inthere!\nTry again!")
                        get_rppath()
                    else:
                        print("Resource Pack Path succesfully saved! > "+rp_path)
                        dpdates[5] = rp_path
                elif rpp_choose.lower() == "path":
                    rp_path = input("What's the path of your resource pack(rp folder included)? Paste it here: ")
                    if os.path.isfile(rp_path+'\\pack.mcmeta') == False:
                        print("Sure "+rp_path+" is the Resource Pack path? There appears to be no pack.mcmeta file inthere!\nTry again!")
                        get_rppath()
                    else:
                        print("Resource Pack Path succesfully saved! > "+"rp_path")
                        dpdates[5] = rp_path
                else:
                    print("Invalid Input, I'll ask it again!\n")
                    get_rppath()
            # Starting Part
            print("Hi! I'm UltroGhast and welcome to the Custom Item generator for Datapacks [V.1]\n")
            print('Before we start, the generator needs to know some things to work\nIf you don\'t understand a question, type \'help\' as answer\nThe generator will not ask you these things anymore')
            dpdates = [1,1,1,1,1,1,1,1]
            player_name = input("\n\nPlease insert your name: ")
            dpdates[0] = player_name
            get_player_namespace()
            get_dp_namespace()
            ask_followconventions()
            if followconventions == True:
                ask_cmd()
            get_rppath()
            functions_path = str("./data/"+player_namespace+"/functions/"+dp_namespace+"/customitem/")
            refdp_path = str(player_namespace+":"+dp_namespace+"/customitem/")
            dpdates[6] = functions_path
            dpdates[7] = refdp_path
            
            with open("saved_dp_dates.json","w") as dpdatesfile:
                dpdatesfile.write(json.dumps(dpdates))
                dpdatesfile.close()
            ###create directories and files
            #create function tags
            if not os.path.isdir("./data/minecraft"): os.mkdir("./data/minecraft")
            if not os.path.isdir("./data/minecraft/tags"): os.mkdir("./data/minecraft/tags")
            if not os.path.isdir("./data/minecraft/tags/functions"): os.mkdir("./data/minecraft/tags/functions")

            if os.path.isfile('./data/minecraft/tags/functions/tick.json') == True:
                tickfile = open("data/minecraft/tags/functions/tick.json","r")
                tick_content = json.loads(tickfile.read())
                tickfile = open("data/minecraft/tags/functions/tick.json","w")
                tick_line = player_namespace+":"+dp_namespace+"/tick"
                if not any([i == tick_line for i in tick_content["values"]]):
                    tick_content["values"].append(tick_line)
                tickfile.write(json.dumps(tick_content))
                tickfile.close()
            else:
                with open("data/minecraft/tags/functions/tick.json","w") as tickfile:
                    tick_content = {"values":[str(player_namespace+":"+dp_namespace+"/tick")]}
                    tickfile.write(json.dumps(tick_content))
                    
            if os.path.isfile('./data/minecraft/tags/functions/load.json') == True:
                loadfile = open("data/minecraft/tags/functions/load.json","r")
                load_content = json.loads(loadfile.read())
                loadfile = open("data/minecraft/tags/functions/load.json","w")
                load_line = player_namespace+":"+dp_namespace+"/load"
                if not any([i == load_line for i in load_content["values"]]):
                    load_content["values"].append(load_line)
                loadfile.write(json.dumps(load_content))
                loadfile.close()
            else:
                with open("data/minecraft/tags/functions/load.json","w") as loadfile:
                    load_content = {"values":[str(player_namespace+":"+dp_namespace+"/load")]}
                    loadfile.write(json.dumps(load_content))
            #datapack data
            if not os.path.isdir(f"./data/{player_namespace}"): os.mkdir(f"./data/{player_namespace}")
            if not os.path.isdir(f"./data/{player_namespace}/functions"): os.mkdir(f"./data/{player_namespace}/functions")
            if not os.path.isdir(f"./data/{player_namespace}/functions/{dp_namespace}"): os.mkdir(f"./data/{player_namespace}/functions/{dp_namespace}")
            if not os.path.isdir(f"./data/{player_namespace}/functions/{dp_namespace}/customitem"): os.mkdir(f"./data/{player_namespace}/functions/{dp_namespace}/customitem")

            if os.path.isfile(f"./data/{player_namespace}/functions/{dp_namespace}/tick.mcfunction") == False:
                tickfun = open(f"data/{player_namespace}/functions/{dp_namespace}/tick.mcfunction","w")
                tickfun.close()
            if os.path.isfile(f"./data/{player_namespace}/functions/{dp_namespace}/load.mcfunction") == False:
                loadfun = open(f"data/{player_namespace}/functions/{dp_namespace}/load.mcfunction","w")
                loadfun.close()
            if followconventions == True:
                if os.path.isfile(f"./data/{player_namespace}/functions/{dp_namespace}/uninstall.mcfunction") == False:
                    uninfun = open(f"data/{player_namespace}/functions/{dp_namespace}/uninstall.mcfunction","w")
                    uninfun.close()

            if not os.path.isdir(f"./data/{player_namespace}/recipes"): os.mkdir(f"./data/{player_namespace}/recipes")
            if not os.path.isdir(f"./data/{player_namespace}/recipes/{dp_namespace}"): os.mkdir(f"./data/{player_namespace}/recipes/{dp_namespace}")
            if not os.path.isdir(f"./data/{player_namespace}/recipes/{dp_namespace}/customitem"): os.mkdir(f"./data/{player_namespace}/recipes/{dp_namespace}/customitem")
            if not os.path.isdir(f"./data/{player_namespace}/advancements"): os.mkdir(f"./data/{player_namespace}/advancements")
            if not os.path.isdir(f"./data/{player_namespace}/advancements/{dp_namespace}"): os.mkdir(f"./data/{player_namespace}/advancements/{dp_namespace}")
            if not os.path.isdir(f"./data/{player_namespace}/advancements/{dp_namespace}/customitem"): os.mkdir(f"./data/{player_namespace}/advancements/{dp_namespace}/customitem")
            if not os.path.isdir(f"./data/{player_namespace}/loot_tables"): os.mkdir(f"./data/{player_namespace}/loot_tables")
            if not os.path.isdir(f"./data/{player_namespace}/loot_tables/{dp_namespace}"): os.mkdir(f"./data/{player_namespace}/loot_tables/{dp_namespace}")
            if not os.path.isdir(f"./data/{player_namespace}/loot_tables/{dp_namespace}/customitem"): os.mkdir(f"./data/{player_namespace}/loot_tables/{dp_namespace}/customitem")
            if not os.path.isdir(f"{rp_path}/assets/"): os.mkdir(f"{rp_path}/assets/")
            if not os.path.isdir(f"{rp_path}/assets/minecraft"): os.mkdir(f"{rp_path}/assets/minecraft")
            if not os.path.isdir(f"{rp_path}/assets/minecraft/models"): os.mkdir(f"{rp_path}/assets/minecraft/models")
            if not os.path.isdir(f"{rp_path}/assets/minecraft/models/item"): os.mkdir(f"{rp_path}/assets/minecraft/models/item")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}"): os.mkdir(f"{rp_path}/assets/{player_namespace}")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}/models"): os.mkdir(f"{rp_path}/assets/{player_namespace}/models")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}/textures"): os.mkdir(f"{rp_path}/assets/{player_namespace}/textures")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}/models/{dp_namespace}"): os.mkdir(f"{rp_path}/assets/{player_namespace}/models/{dp_namespace}")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}/models/{dp_namespace}/customitem"): os.mkdir(f"{rp_path}/assets/{player_namespace}/models/{dp_namespace}/customitem")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}"): os.mkdir(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customitem"): os.mkdir(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customitem")
            if not os.path.isdir(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customblock"): os.mkdir(f"{rp_path}/assets/{player_namespace}/textures/{dp_namespace}/customblock")
    else:
        ifquit = input("The generator isn't in the right directory!\nPlace it in the Datapack Folder, with pack.mcmeta, pack.png and the data folder!\nClose the script typing 'quit'\n>>>")
        if ifquit.lower() == "quit":
            exit()
        else:
            continue
