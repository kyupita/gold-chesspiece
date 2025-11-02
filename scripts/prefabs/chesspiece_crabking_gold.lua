local assets =
{
    Asset("ANIM", "anim/chesspiece_crabking_gold.zip"),
	Asset("ANIM", "anim/swap_chesspiece_crabking_gold.zip"),
	Asset("ATLAS", "images/chesspiece_crabking_gold.xml"),
    Asset("IMAGE", "images/chesspiece_crabking_gold.tex"),
}

local PHYSICS_RADIUS = .45

--[[inst.components.lootdropper:DropLoot()
    local fx = SpawnPrefab("collapse_small")
    fx.Transform:SetPosition(inst.Transform:GetWorldPosition())
    fx:SetMaterial("stone")
    inst:Remove()
end]]

local function onequip(inst, owner)
    owner.AnimState:OverrideSymbol("swap_body", "swap_chesspiece_crabking_gold", "swap_body")
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
	
	inst.AnimState:SetBank("chesspiece_crabking_gold")
	inst.AnimState:SetBuild("chesspiece_crabking_gold")
	inst.AnimState:PlayAnimation("idle")
	
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
	inst.components.symbolswapdata:SetData("chesspiece_crabking_gold", "swap_body")

	inst:AddComponent("hauntable")
	inst.components.hauntable:SetHauntValue(TUNING.HAUNT_TINY)
	
	--inst.OnLoad = onload
	--inst.OnSave = onsave
	
	return inst
end

STRINGS.NAMES.CHESSPIECE_CRABKING_GOLD = "crabking"

STRINGS.CHARACTERS.GENERIC.DESCRIBE.CHESSPIECE_CRABKING_GOLD = "Still not as crabby as Maxwell."

--[[STRINGS.CHARACTERS.WILSON.DESCRIBE.CHESSPIECE_CRABKING_GOLD = "Still not as crabby as Maxwell."
STRINGS.CHARACTERS.WILLOW.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WOLFGANG.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WENDY.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WX78.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WICKERBOTTOM.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WOODIE.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WAXWELL.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WATHGRITHR.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WEBBER.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WINONA.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WARLY.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WORTOX.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WORMWOOD.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WURT.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WALTER.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""
STRINGS.CHARACTERS.WANDA.DESCRIBE.CHESSPIECE_CRABKING_GOLD = ""]]

return Prefab("chesspiece_crabking_gold", fn, assets, prefabs)