# 🏠 RoomieQuest

A full-stack roommate management app that helps people living together stay organized — shared tasks, shopping lists, and real-time updates for every member of a room.

**Stack:** React + Vite · Supabase (PostgreSQL + Auth + Realtime) · Tailwind CSS

---

## Features

- **Auth** — email/password signup and login, auto-synced to public USERS table via database trigger
- **Rooms** — create a room with a password, or join one by ID. Max 5 members per room, max 3 rooms per user — enforced at the database level with triggers
- **Tasks** — add tasks, check them off to delete them, see who added each one
- **Shopping List** — add items with optional prices, mark as purchased (strikes through and shifts to bottom), see who added each item
- **Realtime** — all changes sync live across every roommate's screen via Supabase Realtime WebSocket channels

---

## Project Structure

```
src/
├── App.jsx                 # Root — owns user/room state, handles routing
├── supabaseClient.js       # Supabase client init
├── index.css               # Global styles, fonts, animations
└── components/
    ├── Auth.jsx            # Login / signup
    ├── Dashboard.jsx       # Room list, create/join room
    └── Room.jsx            # Tasks + shopping list + realtime
```

---

## Architecture

### How components communicate

React uses one-way data flow. Data passes down via props, events pass back up via callback functions.

```
App.jsx  (owns user + activeRoomId state)
│
├── Auth.jsx
│     Supabase auth state change → App updates user → shows Dashboard
│
├── Dashboard.jsx
│     Receives: user, onEnterRoom
│     User clicks Enter Room → calls onEnterRoom(roomId) → App sets activeRoomId
│
└── Room.jsx
      Receives: roomId, user, onExit
      User clicks ← Dashboard → calls onExit() → App sets activeRoomId null
```

**The rule:** children never modify parent state directly. They call a function the parent passed down.

### Database Schema

```sql
USERS          (user_id, user_name, email)
ROOMS          (room_id, password)
MEMBERSHIP     (user_id, room_id)
TASKS          (task_id, room_id, user_id, description, is_done, created_at)
SHOPPING_ITEMS (item_id, room_id, added_by, item, item_price, is_purchased, created_at)
```

All tables use **Row Level Security (RLS)** — users can only read/write data for rooms they're members of. Policies are enforced at the database level, not the application level.

### Realtime

Supabase opens a WebSocket channel per room. Any INSERT, UPDATE, or DELETE on TASKS or SHOPPING_ITEMS triggers a re-fetch on all connected clients.

```js
supabase
  .channel(`room-${roomId}`)
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'TASKS', filter: `room_id=eq.${roomId}` },
    () => loadTasks()
  )
  .subscribe();
```

The channel is cleaned up via `useEffect` return when the user leaves the room.

### useCallback

`loadTasks` and `loadShoppingItems` are wrapped in `useCallback` to prevent stale closures in the realtime subscription. Without it, every render creates a new function reference, the `useEffect` dependency array sees a change, and the channel gets torn down and rebuilt on every keystroke.

---

## Database Triggers

### Auto-sync auth users to public USERS table

```sql
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public."USERS" (user_id, user_name, email)
  VALUES (
    NEW.id,
    COALESCE(NULLIF(SPLIT_PART(NEW.email, '@', 1), ''), 'user_' || LEFT(NEW.id::text, 6)),
    NEW.email
  )
  ON CONFLICT (user_id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### Max 5 members per room

```sql
CREATE OR REPLACE FUNCTION check_room_member_limit()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT COUNT(*) FROM "MEMBERSHIP" WHERE room_id = NEW.room_id) >= 5 THEN
    RAISE EXCEPTION 'Room is full (max 5 members)';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_room_member_limit
BEFORE INSERT ON "MEMBERSHIP"
FOR EACH ROW EXECUTE FUNCTION check_room_member_limit();
```

### Max 3 rooms per user

```sql
CREATE OR REPLACE FUNCTION check_user_room_limit()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT COUNT(*) FROM "MEMBERSHIP" WHERE user_id = NEW.user_id) >= 3 THEN
    RAISE EXCEPTION 'You can only be in up to 3 rooms';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_user_room_limit
BEFORE INSERT ON "MEMBERSHIP"
FOR EACH ROW EXECUTE FUNCTION check_user_room_limit();
```

---

## Bugs Encountered & Fixed

### 1. `TypeError: Failed to fetch` on login
**Cause:** Supabase took the project offline (free tier inactivity).  
**Fix:** Reactivated the project in the Supabase dashboard.

### 2. Exit button did nothing (vanilla JS version)
**Cause:** Script loaded as `type="module"` — functions are scoped to the module and don't attach to `window`. Inline `onclick="exitRoom()"` looks for the function on `window` and finds nothing.  
**Fix:** Used `addEventListener` instead of inline HTML handlers.

### 3. RLS blocked all inserts (403 Forbidden)
**Cause:** Supabase enables Row Level Security by default. No policies = no access.  
**Fix:** Added explicit INSERT, SELECT, UPDATE, DELETE policies for each table, scoped to room members via MEMBERSHIP.

### 4. Foreign key violation on MEMBERSHIP insert
**Cause:** `MEMBERSHIP.user_id` has a foreign key to `public.USERS`, but the user didn't have a row there yet. Supabase Auth and the public USERS table are completely separate.  
**Fix:** Added a database trigger `on_auth_user_created` that automatically inserts into USERS whenever a new auth user is created.

### 5. Database trigger error: `relation "USERS" does not exist`
**Cause:** Triggers on `auth.users` run in the `auth` schema. Referencing `"USERS"` without a schema prefix looked for `auth."USERS"` which doesn't exist.  
**Fix:** Used fully qualified `public."USERS"` in the trigger function.

### 6. Trigger error: `record "new" has no field "user_id"`
**Cause:** The room limit trigger was placed on the `ROOMS` table. `NEW` refers to the row being inserted — a ROOMS row — which has no `user_id` column.  
**Fix:** Moved the trigger to `MEMBERSHIP` where `user_id` actually lives.

### 7. Inputs reset after every keystroke in Room view
**Cause:** The `Card` component was defined inside the `Room` function. Every state change (keystroke) caused React to see `Card` as a brand new component type and unmount/remount it, resetting all child inputs.  
**Fix:** Moved `Card` outside the `Room` function to the top level of the file.

### 8. Shopping list checkboxes broken after adding an item
**Cause:** After inserting, a temp item with ID `temp-123456` was added to state. `toggleItem` guards against temp IDs and blocks the action. If realtime doesn't fire fast enough to replace the temp with a real row, checkboxes stay broken.  
**Fix:** Called `loadShoppingItems()` directly after a successful insert to force-replace the temp item immediately.

### 9. Stale closure in realtime subscription
**Cause:** `loadTasks` and `loadShoppingItems` were defined as plain `async` functions inside the component. The `useEffect` that set up the realtime channel captured old versions of these functions on first render.  
**Fix:** Wrapped both in `useCallback` with proper dependency arrays so the realtime channel always calls the latest version.

### 10. `useEffect` re-running on every render
**Cause:** Functions passed as `useEffect` dependencies were being recreated on every render, causing the effect to re-run, tear down the channel, and rebuild it constantly.  
**Fix:** `useCallback` memoizes the functions so their reference stays stable between renders.

---

## Running Locally

```bash
git clone https://github.com/yourusername/roomie-quest.git
cd roomie-quest
npm install
npm run dev
```

Open `http://localhost:5173`.

Add your Supabase credentials to `src/supabaseClient.js`.

---

## Roadmap

- [ ] AI-powered task assignment based on room member profiles
- [ ] Room names instead of UUIDs
- [ ] Member list inside each room
- [ ] Email notifications for overdue tasks
- [ ] Unit and integration tests
- [ ] Deploy to Vercel

---

*Built by Daniel — started Dec 2025*