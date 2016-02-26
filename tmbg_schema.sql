drop table if exists tmbg;
create table tmbg (
  id integer primary key autoincrement,
  lyne text not null,		 		
  song_title text not null
);