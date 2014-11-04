drop table if exists words;
create table words (
  id integer primary key autoincrement,
  word text not null,		 		
  pronunciation text not null
);