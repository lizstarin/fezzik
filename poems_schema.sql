drop table if exists poems;
create table poems (
  id integer primary key autoincrement,
  lyne text not null,
  author text not null,		 		
  title text not null,
  meter text not null
);