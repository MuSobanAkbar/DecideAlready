create table public.watch_later (
  user_id    uuid        not null references auth.users (id) on delete cascade,
  tmdb_id    integer     not null,
  title      text        not null,
  poster_path text,
  added_at   timestamptz not null default now(),
  primary key (user_id, tmdb_id)
);

alter table public.watch_later enable row level security;