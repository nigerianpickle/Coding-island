import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock Supabase client
const mockSelect = vi.fn();
const mockInsert = vi.fn();
const mockUpdate = vi.fn();
const mockDelete = vi.fn();
const mockEq = vi.fn();
const mockSingle = vi.fn();
const mockIn = vi.fn();
const mockOrder = vi.fn();

const mockFrom = vi.fn(() => ({
  select: mockSelect.mockReturnThis(),
  insert: mockInsert.mockReturnThis(),
  update: mockUpdate.mockReturnThis(),
  delete: mockDelete.mockReturnThis(),
  eq: mockEq.mockReturnThis(),
  in: mockIn.mockReturnThis(),
  order: mockOrder.mockReturnThis(),
  single: mockSingle,
  maybeSingle: mockSingle,
}));

vi.mock('../supabaseClient', () => ({
  supabase: {
    from: mockFrom,
    auth: {
      getUser: vi.fn(),
      signInWithPassword: vi.fn(),
      signUp: vi.fn(),
      signOut: vi.fn(),
    },
  },
}));

import { supabase } from '../supabaseClient';

beforeEach(() => {
  vi.clearAllMocks();
});

// --- Simulated logic functions (mirrors what components do) ---

async function loadTasks(roomId) {
  const { data, error } = await supabase
    .from('TASKS')
    .select('*')
    .eq('room_id', roomId)
    .order('created_at', { ascending: true });
  if (error) throw error;
  return data;
}

async function addTask(roomId, userId, description) {
  if (!description.trim()) throw new Error('Description is required');
  const { error } = await supabase
    .from('TASKS')
    .insert({ room_id: roomId, user_id: userId, description });
  if (error) throw error;
}

async function deleteTask(taskId) {
  const { error } = await supabase
    .from('TASKS')
    .delete()
    .eq('task_id', taskId);
  if (error) throw error;
}

async function addShoppingItem(roomId, userId, item, price = 0) {
  if (!item.trim()) throw new Error('Item name is required');
  const { error } = await supabase
    .from('SHOPPING_ITEMS')
    .insert({ room_id: roomId, added_by: userId, item, item_price: price });
  if (error) throw error;
}

async function toggleShoppingItem(itemId, currentValue) {
  if (String(itemId).startsWith('temp-')) return false;
  const { error } = await supabase
    .from('SHOPPING_ITEMS')
    .update({ is_purchased: !currentValue })
    .eq('item_id', itemId);
  if (error) throw error;
  return true;
}

async function loadMembers(roomId) {
  const { data: memberships, error } = await supabase
    .from('MEMBERSHIP')
    .select('user_id')
    .eq('room_id', roomId);
  if (error) throw error;
  return memberships;
}

// --- Integration Tests ---

describe('loadTasks', () => {
  it('fetches tasks for a room', async () => {
    const fakeTasks = [
      { task_id: '1', description: 'Clean bathroom', is_done: false },
      { task_id: '2', description: 'Buy milk', is_done: false },
    ];
    mockOrder.mockResolvedValueOnce({ data: fakeTasks, error: null });

    const result = await loadTasks('room-123');
    expect(result).toEqual(fakeTasks);
    expect(mockFrom).toHaveBeenCalledWith('TASKS');
  });

  it('throws on error', async () => {
    mockOrder.mockResolvedValueOnce({ data: null, error: { message: 'DB error' } });
    await expect(loadTasks('room-123')).rejects.toEqual({ message: 'DB error' });
  });
});

describe('addTask', () => {
  it('inserts a task with correct fields', async () => {
    mockInsert.mockResolvedValueOnce({ error: null });
    await addTask('room-123', 'user-456', 'Clean kitchen');
    expect(mockFrom).toHaveBeenCalledWith('TASKS');
    expect(mockInsert).toHaveBeenCalledWith({
      room_id: 'room-123',
      user_id: 'user-456',
      description: 'Clean kitchen',
    });
  });

  it('throws if description is empty', async () => {
    await expect(addTask('room-123', 'user-456', '  ')).rejects.toThrow('Description is required');
  });

  it('throws on supabase error', async () => {
    mockInsert.mockResolvedValueOnce({ error: { message: 'Insert failed' } });
    await expect(addTask('room-123', 'user-456', 'Clean')).rejects.toEqual({ message: 'Insert failed' });
  });
});

describe('deleteTask', () => {
  it('deletes a task by id', async () => {
    mockEq.mockResolvedValueOnce({ error: null });
    await deleteTask('task-789');
    expect(mockFrom).toHaveBeenCalledWith('TASKS');
    expect(mockEq).toHaveBeenCalledWith('task_id', 'task-789');
  });
});

describe('addShoppingItem', () => {
  it('inserts an item with price', async () => {
    mockInsert.mockResolvedValueOnce({ error: null });
    await addShoppingItem('room-123', 'user-456', 'Milk', 3.99);
    expect(mockInsert).toHaveBeenCalledWith({
      room_id: 'room-123',
      added_by: 'user-456',
      item: 'Milk',
      item_price: 3.99,
    });
  });

  it('defaults price to 0', async () => {
    mockInsert.mockResolvedValueOnce({ error: null });
    await addShoppingItem('room-123', 'user-456', 'Eggs');
    expect(mockInsert).toHaveBeenCalledWith(
      expect.objectContaining({ item_price: 0 })
    );
  });

  it('throws if item name is empty', async () => {
    await expect(addShoppingItem('room-123', 'user-456', '')).rejects.toThrow('Item name is required');
  });
});

describe('toggleShoppingItem', () => {
  it('blocks temp items from being toggled', async () => {
    const result = await toggleShoppingItem('temp-1234567890', false);
    expect(result).toBe(false);
    expect(mockFrom).not.toHaveBeenCalled();
  });

  it('toggles a real item from false to true', async () => {
    mockEq.mockResolvedValueOnce({ error: null });
    const result = await toggleShoppingItem('item-real-id', false);
    expect(result).toBe(true);
    expect(mockUpdate).toHaveBeenCalledWith({ is_purchased: true });
  });

  it('toggles a real item from true to false', async () => {
    mockEq.mockResolvedValueOnce({ error: null });
    await toggleShoppingItem('item-real-id', true);
    expect(mockUpdate).toHaveBeenCalledWith({ is_purchased: false });
  });
});

describe('loadMembers', () => {
  it('fetches memberships for a room', async () => {
    const fakeMemberships = [
      { user_id: 'user-1' },
      { user_id: 'user-2' },
    ];
    mockEq.mockResolvedValueOnce({ data: fakeMemberships, error: null });

    const result = await loadMembers('room-123');
    expect(result).toEqual(fakeMemberships);
    expect(mockFrom).toHaveBeenCalledWith('MEMBERSHIP');
  });

  it('throws on error', async () => {
    mockEq.mockResolvedValueOnce({ data: null, error: { message: 'Not found' } });
    await expect(loadMembers('room-123')).rejects.toEqual({ message: 'Not found' });
  });
});
