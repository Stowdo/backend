create or replace function check_username() returns trigger as
$$
declare
    nb_row_with_username int;
begin
    select count(1) into nb_row_with_username
    from auth_user au
    where au.username = new.username;

    if nb_row_with_username >= 1 then
        raise exception 'This username is already used';
    end if;
    return new;
end$$
LANGUAGE plpgsql;

create trigger check_username before insert or update on auth_user
for each row execute procedure check_username();