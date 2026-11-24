-- CarrotSwap: equip Carrot on a Stick while mounted, restore the old trinket when not.
-- Gear can't be changed in combat, so any swap that comes up in combat waits until it ends.

local CARROT_ID = 11122
local TRINKET_SLOTS = { [13] = true, [14] = true }

local f = CreateFrame("Frame")
local pending = false   -- a swap is waiting for combat to end

local function Print(msg)
  DEFAULT_CHAT_FRAME:AddMessage("|cffff9933CarrotSwap:|r " .. msg)
end

local function DB()
  CarrotSwapDB = CarrotSwapDB or {}
  CarrotSwapDB.slot = CarrotSwapDB.slot or 14
  if CarrotSwapDB.enabled == nil then CarrotSwapDB.enabled = true end
  return CarrotSwapDB
end

local function CarrotSlot()
  for slot in pairs(TRINKET_SLOTS) do
    if GetInventoryItemID("player", slot) == CARROT_ID then return slot end
  end
end

local function HaveCarrot()
  return CarrotSlot() or GetItemCount(CARROT_ID) > 0
end

local function CanSwap()
  return not InCombatLockdown() and not UnitIsDeadOrGhost("player")
end

local function PutCarrotOn()
  local db = DB()
  if CarrotSlot() or not HaveCarrot() then return end
  -- Remember what was in the slot so we can put it back. Don't overwrite an
  -- older memory (e.g. you logged out mounted with the carrot on).
  if not db.previous then
    db.previous = GetInventoryItemID("player", db.slot) or false
  end
  EquipItemByName(CARROT_ID, db.slot)
end

local function TakeCarrotOff()
  local db = DB()
  local slot = CarrotSlot()
  if not slot then db.previous = nil; return end  -- you took it off yourself
  if db.previous == nil then return end           -- you put it on yourself; leave it
  if db.previous and GetItemCount(db.previous) > 0 then
    EquipItemByName(db.previous, slot)
  elseif db.previous == false then
    -- slot was empty before: move the carrot back to the bags
    PickupInventoryItem(slot)
    if CursorHasItem() then
      PutItemInBackpack()
      if CursorHasItem() then ClearCursor(); Print("bags full, carrot left on.") end
    end
  else
    Print("couldn't find your old trinket in your bags, carrot left on.")
  end
  db.previous = nil
end

local function Update()
  local db = DB()
  if not db.enabled then return end
  local mounted = IsMounted() and not UnitOnTaxi("player")
  if not CanSwap() then
    pending = true
    return
  end
  pending = false
  if mounted then PutCarrotOn() else TakeCarrotOff() end
end

f:SetScript("OnEvent", function(_, event, unit)
  if event == "UNIT_AURA" and unit ~= "player" then return end
  if event == "PLAYER_REGEN_ENABLED" and not pending then return end
  -- small delay: the mount aura and IsMounted() don't always update on the same frame
  C_Timer.After(0.1, Update)
end)

f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:RegisterEvent("PLAYER_REGEN_ENABLED")
f:RegisterEvent("PLAYER_UNGHOST")
f:RegisterEvent("PLAYER_ALIVE")
f:RegisterUnitEvent("UNIT_AURA", "player")
if C_EventUtils == nil or C_EventUtils.IsEventValid("PLAYER_MOUNT_DISPLAY_CHANGED") then
  pcall(f.RegisterEvent, f, "PLAYER_MOUNT_DISPLAY_CHANGED")
end

SLASH_CARROTSWAP1 = "/carrot"
SLASH_CARROTSWAP2 = "/carrotswap"
SlashCmdList.CARROTSWAP = function(msg)
  local db = DB()
  msg = (msg or ""):lower():match("^%s*(.-)%s*$")
  if msg == "on" or msg == "off" then
    db.enabled = (msg == "on")
    Print(db.enabled and "enabled." or "disabled.")
    if db.enabled then Update() end
  elseif msg == "13" or msg == "14" then
    db.slot = tonumber(msg)
    Print("carrot goes in " .. (db.slot == 13 and "top (13)" or "bottom (14)") .. " trinket slot.")
  else
    Print(("%s, slot %d. Commands: /carrot on | off | 13 | 14"):format(
      db.enabled and "enabled" or "disabled", db.slot))
  end
end
