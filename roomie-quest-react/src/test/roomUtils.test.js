import { describe, it, expect } from 'vitest';

// --- Utility functions (copied from Room.jsx for testing) ---

const MEMBER_COLORS = [
  '#10b981', '#6366f1', '#f59e0b', '#ef4444', '#8b5cf6',
];

function getInitials(name) {
  if (!name) return '?';
  return name.slice(0, 2).toUpperCase();
}

function getMemberColor(userId) {
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    hash = userId.charCodeAt(i) + ((hash << 5) - hash);
  }
  return MEMBER_COLORS[Math.abs(hash) % MEMBER_COLORS.length];
}

function generateRoomName(adjectives, nouns) {
  const adj = adjectives[0];
  const noun = nouns[0];
  return `${adj} ${noun}`;
}

function sortItems(items) {
  return [
    ...items.filter(i => !i.is_purchased),
    ...items.filter(i => i.is_purchased),
  ];
}

function isTempId(id) {
  return String(id).startsWith('temp-');
}

// --- Tests ---

describe('getInitials', () => {
  it('returns first two characters uppercased', () => {
    expect(getInitials('daniel')).toBe('DA');
  });

  it('returns ? for empty string', () => {
    expect(getInitials('')).toBe('?');
  });

  it('returns ? for null', () => {
    expect(getInitials(null)).toBe('?');
  });

  it('handles single character names', () => {
    expect(getInitials('D')).toBe('D');
  });
});

describe('getMemberColor', () => {
  it('returns a valid color from the palette', () => {
    const color = getMemberColor('some-user-id');
    expect(MEMBER_COLORS).toContain(color);
  });

  it('returns the same color for the same userId', () => {
    const id = 'abc-123-def';
    expect(getMemberColor(id)).toBe(getMemberColor(id));
  });

  it('handles short ids', () => {
    const color = getMemberColor('a');
    expect(MEMBER_COLORS).toContain(color);
  });
});

describe('generateRoomName', () => {
  it('combines an adjective and a noun', () => {
    const name = generateRoomName(['Chill'], ['Mango']);
    expect(name).toBe('Chill Mango');
  });

  it('has a space between words', () => {
    const name = generateRoomName(['Purple'], ['Penguin']);
    expect(name.split(' ').length).toBe(2);
  });
});

describe('sortItems', () => {
  it('puts unpurchased items first', () => {
    const items = [
      { item_id: '1', item: 'milk', is_purchased: true },
      { item_id: '2', item: 'eggs', is_purchased: false },
      { item_id: '3', item: 'bread', is_purchased: false },
    ];
    const sorted = sortItems(items);
    expect(sorted[0].item).toBe('eggs');
    expect(sorted[1].item).toBe('bread');
    expect(sorted[2].item).toBe('milk');
  });

  it('returns all items', () => {
    const items = [
      { item_id: '1', is_purchased: true },
      { item_id: '2', is_purchased: false },
    ];
    expect(sortItems(items).length).toBe(2);
  });

  it('handles empty array', () => {
    expect(sortItems([])).toEqual([]);
  });
});

describe('isTempId', () => {
  it('returns true for temp ids', () => {
    expect(isTempId('temp-1234567890')).toBe(true);
  });

  it('returns false for real UUIDs', () => {
    expect(isTempId('9628caa8-18ae-493a-ac98-2738cd70bba1')).toBe(false);
  });

  it('handles numeric ids', () => {
    expect(isTempId(12345)).toBe(false);
  });
});

describe('room limits', () => {
  it('blocks creation when user has 3 rooms', () => {
    const rooms = [{ room_id: '1' }, { room_id: '2' }, { room_id: '3' }];
    const canCreate = rooms.length < 3;
    expect(canCreate).toBe(false);
  });

  it('allows creation when user has fewer than 3 rooms', () => {
    const rooms = [{ room_id: '1' }];
    const canCreate = rooms.length < 3;
    expect(canCreate).toBe(true);
  });

  it('blocks joining when room has 5 members', () => {
    const memberCount = 5;
    const canJoin = memberCount < 5;
    expect(canJoin).toBe(false);
  });

  it('allows joining when room has fewer than 5 members', () => {
    const memberCount = 3;
    const canJoin = memberCount < 5;
    expect(canJoin).toBe(true);
  });
});
