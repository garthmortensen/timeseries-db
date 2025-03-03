-- ddl schema
create table cats (
    id serial primary key,
    name varchar(255) not null,
    age integer,
    loved boolean default true,
    created_at timestamp default current_timestamp
);

-- dml seed
insert into cats (name, age, loved) 
values 
    ('diesel', 4, true),
    ('ginger', 6, true);
