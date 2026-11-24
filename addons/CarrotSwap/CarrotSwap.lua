-- CarrotSwap: equip Carrot on a Stick while mounted, restore the old trinket when not.
-- Gear can't be changed in combat, so any swap that comes up in combat waits until it ends.

local CARROT_ID = 11122
local TRINKET_SLOTS = { [13] = true, [14] = true }

local f = CreateFrame("Frame")
local warned = false    -- already said the old trinket is missing; don't repeat it
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

local function CanSwap()
  return not InCombatLockdown() and not UnitIsDeadOrGhost("player")
end

-- Remember the last trinket (not the carrot) seen in each trinket slot, so we
-- always know what to put back, even if the carrot went on some other way
-- (by hand, or before a /reload or logout).
local function RememberTrinkets()
  local db = DB()
  db.last = db.last or {}
  for slot in pairs(TRINKET_SLOTS) do
    local id = GetInventoryItemID("player", slot)
    if id and id ~= CARROT_ID then db.last[slot] = id end
  end
end

local function Debug(msg)
  if DB().debug then Print("|cff999999" .. msg .. "|r") end
end

local function PutCarrotOn()
  local db = DB()
  if CarrotSlot() or IsInventoryItemLocked(db.slot) then return end
  if GetItemCount(CARROT_ID) == 0 then Debug("no carrot in bags"); return end
  RememberTrinkets()
  warned = false
  db.wasEmpty = GetInventoryItemID("player", db.slot) == nil
  Debug("mounted: equipping carrot in slot " .. db.slot)
  EquipItemByName(CARROT_ID, db.slot)
end

local function TakeCarrotOff()
  local db = DB()
  local slot = CarrotSlot()
  if not slot or IsInventoryItemLocked(slot) then return end  -- locked: a swap is already moving
  local old = (db.last and db.last[slot]) or db.previous  -- previous: saved by v1.0
  if db.wasEmpty or db.previous == false or not old then
    Debug("dismounted: slot was empty before, moving carrot to bags")
    PickupInventoryItem(slot)
    if CursorHasItem() then
      PutItemInBackpack()
      for bag = 1, 4 do
        if not CursorHasItem() then break end
        PutItemInBag(19 + bag)   -- bag slots are inventory slots 20-23
      end
      if CursorHasItem() then ClearCursor(); Print("bags full, carrot left on.") end
    end
  elseif GetItemCount(old) > 0 then
    Debug("dismounted: putting item " .. old .. " back in slot " .. slot)
    EquipItemByName(old, slot)
  else
    if not warned then Print("your old trinket isn't in your bags, carrot left on.") end
    warned = true
    return
  end
  db.wasEmpty = nil
  db.previous = nil
end

local function Update()
  local db = DB()
  if not db.enabled then return end
  local mounted = IsMounted() and not UnitOnTaxi("player")
  if not CanSwap() then
    Debug("in combat or dead, swap waits")
    pending = true
    return
  end
  pending = false
  RememberTrinkets()
  if mounted then PutCarrotOn() else TakeCarrotOff() end
end

f:SetScript("OnEvent", function(_, event, unit)
  if event == "UNIT_AURA" and unit ~= "player" then return end
  if event == "PLAYER_REGEN_ENABLED" and not pending then return end
  if event == "PLAYER_EQUIPMENT_CHANGED" then RememberTrinkets(); return end
  -- small delay: the mount aura and IsMounted() don't always update on the same frame
  C_Timer.After(0.1, Update)
end)

-- Backup check twice a second. Events alone missed some dismounts: if
-- IsMounted() hasn't caught up when the last aura event fires, no later event
-- comes. Only acts when the carrot doesn't match the mount state.
C_Timer.NewTicker(0.5, function()
  local db = DB()
  if not db.enabled or InCombatLockdown() then return end
  local mounted = IsMounted() and not UnitOnTaxi("player")
  local wearing = CarrotSlot() ~= nil
  if mounted ~= wearing and (wearing or GetItemCount(CARROT_ID) > 0) then Update() end
end)

f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:RegisterEvent("PLAYER_REGEN_ENABLED")
f:RegisterEvent("PLAYER_UNGHOST")
f:RegisterEvent("PLAYER_ALIVE")
f:RegisterEvent("PLAYER_EQUIPMENT_CHANGED")
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
  elseif msg == "debug" then
    db.debug = not db.debug
    Print("debug " .. (db.debug and "on." or "off."))
  elseif msg == "13" or msg == "14" then
    db.slot = tonumber(msg)
    Print("carrot goes in " .. (db.slot == 13 and "top (13)" or "bottom (14)") .. " trinket slot.")
  else
    Print(("v1.2, %s, slot %d. Commands: /carrot on | off | 13 | 14 | debug"):format(
      db.enabled and "enabled" or "disabled", db.slot))
  end
end
