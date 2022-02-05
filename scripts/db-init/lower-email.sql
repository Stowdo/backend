create or replace function lower_email() returns trigger as
$$
begin
    new.email = lower(new.email);
    return new;
end$$
LANGUAGE plpgsql;

create trigger lower_email before insert or update on auth_user
for each row execute procedure lower_email();