local assets =
{
    Asset("ANIM", "anim/chesspiece_anchor_gold.zip"),
	Asset("ANIM", "anim/swap_chesspiece_anchor_gold.zip"),
	Asset("ATLAS", "images/chesspiece_anchor_gold.xml"),
    Asset("IMAGE", "images/chesspiece_anchor_gold.tex"),
}

local PHYSICS_RADIUS = .45

--[[inst.components.lootdropper:DropLoot()
    local fx = SpawnPrefab("collapse_small")
    fx.Transform:SetPosition(inst.Transform:GetWorldPosition())
    fx:SetMaterial("stone")
    inst:Remove()
end]]

local function onequip(inst, owner)
    owner.AnimState:OverrideSymbol("swap_body", "swap_chesspiece_anchor_gold", "swap_body")
end

local function onunequip(inst, owner)
    owner.AnimState:ClearOverrideSymbol("swap_body")
end

local function onworkfinished(inst)
    inst.components.lootdropper:DropLoot()
   	local fx = SpawnPrefab("collapse_small")
    fx.Transform:SetPosition(inst.Transform:GetWorldPosition())
    fx:SetMaterial("stone")
    inst:Remove()
end

local function fn()
	local inst = CreateEntity()

	inst.entity:AddTransform()
	inst.entity:AddAnimState()
	inst.entity:AddSoundEmitter()
	inst.entity:AddNetwork()
	
	MakeHeavyObstaclePhysics(inst, PHYSICS_RADIUS)
	inst:SetPhysicsRadiusOverride(PHYSICS_RADIUS)
	
	inst.AnimState:SetBank("chesspiece_anchor_gold")
	inst.AnimState:SetBuild("chesspiece_anchor_gold")
	inst.AnimState:PlayAnimation("idle")
	

	inst:SetPrefabName("chesspiece_anchor_gold")
	
	inst:AddTag("heavy")
	inst.gymweight = 2
	
	inst.entity:SetPristine()

	if not TheWorld.ismastersim then
		return inst
	end

	inst:AddComponent("lootdropper")
	inst.components.lootdropper:SetLoot({"goldnugget"})
	
	inst:AddComponent("workable")
	inst.components.workable:SetWorkAction(ACTIONS.HAMMER)
	inst.components.workable:SetWorkLeft(1)
	inst.components.workable:SetOnFinishCallback(onworkfinished)



	
	
	inst:AddComponent("heavyobstaclephysics")
	inst.components.heavyobstaclephysics:SetRadius(PHYSICS_RADIUS)

	inst:AddComponent("inspectable")
	--[[inst.components.inspectable.getstatus = getstatus]]

	inst:AddComponent("inventoryitem")
	inst.components.inventoryitem.cangoincontainer = false
	inst.components.inventoryitem:SetSinks(true)
	
	inst:AddComponent("equippable")
	inst.components.equippable.equipslot = EQUIPSLOTS.BODY
	inst.components.equippable:SetOnEquip(onequip)
	inst.components.equippable:SetOnUnequip(onunequip)
	inst.components.equippable.walkspeedmult = TUNING.HEAVY_SPEED_MULT

	inst:AddComponent("submersible")
	inst:AddComponent("symbolswapdata")
	inst.components.symbolswapdata:SetData("chesspiece_anchor_gold", "swap_body")

	inst:AddComponent("hauntable")
	inst.components.hauntable:SetHauntValue(TUNING.HAUNT_TINY)
	
	--inst.OnLoad = onload
	--inst.OnSave = onsave
	
	return inst
end

STRINGS.NAMES.CHESSPIECE_ANCHOR_GOLD = "Anchor Figure"

STRINGS.CHARACTERS.GENERIC.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "It's as heavy as it looks."

--[[STRINGS.CHARACTERS.WILSON.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "It's as heavy as it looks."
STRINGS.CHARACTERS.WILLOW.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "It's hard to burn stuff at sea."
STRINGS.CHARACTERS.WOLFGANG.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Is big. And heavy. Wolfgang would like to lift."
STRINGS.CHARACTERS.WENDY.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Why did we sculpt an anchor."
STRINGS.CHARACTERS.WX78.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "AS HEAVY AS THE REAL THING, BUT LESS USEFUL"
STRINGS.CHARACTERS.WICKERBOTTOM.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Artists tend to reference what they're familiar with."
STRINGS.CHARACTERS.WOODIE.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Looks good to me."
STRINGS.CHARACTERS.WAXWELL.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "How kitsch."
STRINGS.CHARACTERS.WATHGRITHR.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "'Twas made in hönör öf öur stalwart vessel!"
STRINGS.CHARACTERS.WEBBER.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Anchors away!"
STRINGS.CHARACTERS.WINONA.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "I'm fond'a this one."
STRINGS.CHARACTERS.WARLY.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "I think Maman would like this."
STRINGS.CHARACTERS.WORTOX.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "So heavy, heavy, dreary, dreary."
STRINGS.CHARACTERS.WORMWOOD.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Heavy"
STRINGS.CHARACTERS.WURT.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Why made anchor for land, florpt?"
STRINGS.CHARACTERS.WALTER.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "Technically this could still work as a real anchor."
STRINGS.CHARACTERS.WANDA.DESCRIBE.CHESSPIECE_ANCHOR_GOLD = "It's not going anywhere. I can look at it later."]]

return Prefab("chesspiece_anchor_gold", fn, assets, prefabs)