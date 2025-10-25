create extension if not exists "uuid-ossp";

create table users (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  total_points int default 0
);

create table shopping_items (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  purchased boolean default false
);

create table tasks (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  completed boolean default false,
  points int default 10,
  shopping_item_id uuid references shopping_items(id)
);
